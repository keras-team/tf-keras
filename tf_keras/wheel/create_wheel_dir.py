# Copyright 2025 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Creates `src` directory for the TF-Keras package.

The steps are as follows:

1. Copy the TF-Keras codebase to it (to `<args.output_path>/tf_keras/src`)
  and rewrite internal imports so that they refer to `keras.src` rather than
  just `keras`.
2. Copy protobuf files to `<args.output_path>/tf_keras/protobuf`.
3. Also copy `setup.py` to the build directory.
"""

import argparse
import os
import pathlib
import shutil

PACKAGE_NAME = "tf_keras"
SRC_DIRNAME = "src"

parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
parser.add_argument(
    "--output_path",
    default=None,
    required=True,
    help="Path to which the output wheel should be written. Required.",
)
parser.add_argument(
    "--nightly",
    action="store_true",
    help="Whether this is for the `tf-keras-nightly` package.",
)
parser.add_argument(
    "--version",
    type=str,
    help="Wheel version.",
)
parser.add_argument(
    "--srcs", help="source files for the wheel", action="append"
)
args = parser.parse_args()


def convert_keras_imports(src_file, dst_file):
    def _convert_line(line):
        if (
            "import tf_keras.protobuf" in line
            or "from tf_keras.protobuf" in line
        ):
            return line
        # Imports starting from `root_name`.
        if line.strip() == f"import {PACKAGE_NAME}":
            line = line.replace(
                f"import {PACKAGE_NAME}",
                f"import {PACKAGE_NAME}.{SRC_DIRNAME} as {PACKAGE_NAME}",
            )
            return line

        line = line.replace(
            f"import {PACKAGE_NAME}.",
            f"import {PACKAGE_NAME}.{SRC_DIRNAME}.",
        )
        line = line.replace(
            f"from {PACKAGE_NAME}.",
            f"from {PACKAGE_NAME}.{SRC_DIRNAME}.",
        )
        line = line.replace(
            f"from {PACKAGE_NAME} import",
            f"from {PACKAGE_NAME}.{SRC_DIRNAME} import",
        )
        # Convert `import tf_keras as keras` into `import tf_keras.src as keras`
        line = line.replace(
            f"import {PACKAGE_NAME} as ",
            f"import {PACKAGE_NAME}.{SRC_DIRNAME} as ",
        )
        # A way to catch LazyLoader calls. Hacky.
        line = line.replace(
            'globals(), "tf_keras.', 'globals(), "tf_keras.src.'
        )
        return line

    with open(src_file) as f:
        contents = f.read()
    lines = contents.split("\n")
    in_string = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('"""') or line.strip().endswith('"""'):
            if line.count('"') % 2 == 1:
                in_string = not in_string
        else:
            line = _convert_line(line)
        new_lines.append(line)

    with open(dst_file, "w") as f:
        f.write("\n".join(new_lines) + "\n")
    os.chmod(dst_file, 0o644)


def copy_file(
    src_file: str,
    dst_dir: str,
) -> None:
    tf_keras_ind = src_file.rfind(f"{PACKAGE_NAME}/")
    if f"{PACKAGE_NAME}/protobuf" in src_file:
        dst_file = os.path.join(dst_dir, src_file[tf_keras_ind:])
        dest_dir_path = os.path.join(
            dst_dir, os.path.dirname(src_file[tf_keras_ind:])
        )
    else:
        dst_file = os.path.join(
            dst_dir, src_file[tf_keras_ind + len(PACKAGE_NAME) + 1 :]
        )
        dest_dir_path = os.path.join(
            dst_dir,
            os.path.dirname(src_file[tf_keras_ind + len(PACKAGE_NAME) + 1 :]),
        )
    os.makedirs(dest_dir_path, exist_ok=True)
    if src_file.endswith(".py") and not src_file.endswith("_pb2.py"):
        # Convert imports from `tf_keras.xyz` to `tf_keras.src.xyz`.
        convert_keras_imports(src_file, dst_file)
    else:
        shutil.copy(src_file, dest_dir_path)
        os.chmod(dst_file, 0o644)


def prepare_srcs(
    deps: list[str], srcs_dir: str, is_nightly: bool, version: str
) -> None:
    """Filter the sources and copy them to the destination directory.

    Args:
      deps: a list of paths to files.
      srcs_dir: target directory where files are copied to.
    """

    for file in deps:
        if (
            f"{PACKAGE_NAME}/" in file
            and f"{PACKAGE_NAME}/api/" not in file
            and f"{PACKAGE_NAME}/tools/" not in file
            and f"{PACKAGE_NAME}/integration_test" not in file
            and f"{PACKAGE_NAME}/wheel/" not in file
            and not file.endswith("_test.py")
        ):
            dst_dir = (
                os.path.join(srcs_dir)
                if f"{PACKAGE_NAME}/protobuf" in file
                else os.path.join(srcs_dir, PACKAGE_NAME, SRC_DIRNAME)
            )
            copy_file(file, dst_dir)

        if file.endswith("oss_setup.py"):
            # Insert {{PACKAGE}} and {{VERSION}} strings in setup.py
            if is_nightly:
                package = PACKAGE_NAME + "-nightly"
            else:
                package = PACKAGE_NAME
            with open(file) as f:
                setup_contents = f.read()
            with open(os.path.join(srcs_dir, "setup.py"), "w") as f:
                setup_contents = setup_contents.replace("{{VERSION}}", version)
                setup_contents = setup_contents.replace("{{PACKAGE}}", package)
                f.write(setup_contents)


def create_wheel_dir(source_files, destination_path, is_nightly, version):
    # Copy sources (`tf_keras/` directory and setup files) to build directory
    prepare_srcs(source_files, destination_path, is_nightly, version)

    # Add blank __init__.py file at package root
    # to make the package directory importable.
    with open(os.path.join(destination_path, PACKAGE_NAME, "__init__.py"), "w"):
        pass
    # Add blank __init__.py file in protobuf dir.
    with open(
        os.path.join(destination_path, PACKAGE_NAME, "protobuf", "__init__.py"),
        "w",
    ):
        pass


if __name__ == "__main__":
    os.makedirs(args.output_path, exist_ok=True)
    create_wheel_dir(
        source_files=args.srcs,
        destination_path=pathlib.Path(args.output_path),
        is_nightly=args.nightly,
        version=args.version,
    )
