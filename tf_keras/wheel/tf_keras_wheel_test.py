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

import argparse
import importlib
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--version",
    type=str,
    help="Wheel version.",
)
args = parser.parse_args()


def test_wheel(expected_version):
    packages_to_check = [
        "layers",
        "Input",
        "Sequential",
        "Model",
        "src.engine.input_layer",
        "__internal__",
        "experimental",
    ]
    failed_packages = []

    logging.info("Try to import packages at runtime...")
    import tf_keras  # pylint: disable=g-import-not-at-top

    for package_name in packages_to_check:
        try:
            if "." in package_name:
                # For nested modules like "src.engine.input_layer"
                full_module_path = f"tf_keras.{package_name}"
                importlib.import_module(full_module_path)
            else:
                # For direct submodules or attributes like "layers" or "Model"
                getattr(tf_keras, package_name)
        except (ImportError, AttributeError):
            logging.exception("error importing %s", package_name)
            failed_packages.append(package_name)

    if failed_packages:
        raise ImportError(
            "Failed to import"
            f" {len(failed_packages)}/{len(packages_to_check)} packages\n"
            f" {failed_packages}"
        )
    logging.info("Import of packages was successful.")

    actual_version = tf_keras.__version__
    if expected_version != actual_version:
        raise ValueError(
            "Incorrect version; expected "
            f"{expected_version} but received {actual_version}"
        )


if __name__ == "__main__":
    test_wheel(args.version)
