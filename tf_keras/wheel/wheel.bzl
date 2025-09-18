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

load("@bazel_skylib//rules:common_settings.bzl", "BuildSettingInfo")
load("@python_version_repo//:py_version.bzl", "HERMETIC_PYTHON_VERSION")
load("@rules_python//python:py_library.bzl", "py_library")
load("@tf_keras_wheel//:wheel.bzl", "WHEEL_VERSION")
load("@tf_keras_wheel_version_suffix//:wheel_version_suffix.bzl", "WHEEL_VERSION_SUFFIX")

def _get_full_wheel_name(
        wheel_version,
        is_nightly):
    wheel_name_template = "tf_keras{nightly_suffix}-{wheel_version}-py{major_python_version}-none-any.whl"
    python_version = HERMETIC_PYTHON_VERSION.replace(".", "")
    return wheel_name_template.format(
        major_python_version = python_version[0],
        wheel_version = wheel_version,
        nightly_suffix = "_nightly" if is_nightly else "",
    )

def _get_source_package_name(wheel_version, is_nightly):
    return "tf_keras{nightly_suffix}-{wheel_version}.tar.gz".format(
        wheel_version = wheel_version,
        nightly_suffix = "_nightly" if is_nightly else "",
    )

def _is_nightly_build():
    return WHEEL_VERSION_SUFFIX.startswith(".dev") and not "selfbuilt" in WHEEL_VERSION_SUFFIX

def _is_selfbuilt_build():
    return WHEEL_VERSION_SUFFIX.startswith(".dev") and "selfbuilt" in WHEEL_VERSION_SUFFIX

def _wheel_impl(ctx):
    executable = ctx.executable.wheel_binary
    output_path = ctx.attr.output_path[BuildSettingInfo].value
    is_nightly = _is_nightly_build()
    build_wheel_only = ctx.attr.build_wheel_only
    build_source_package_only = ctx.attr.build_source_package_only

    full_wheel_version = (WHEEL_VERSION + WHEEL_VERSION_SUFFIX)

    args = ctx.actions.args()
    if build_wheel_only:
        name = _get_full_wheel_name(
            wheel_version = full_wheel_version,
            is_nightly = is_nightly,
        )
        args.add("--build-wheel-only", "True")
    if build_source_package_only:
        name = _get_source_package_name(
            wheel_version = full_wheel_version,
            is_nightly = is_nightly,
        )
        args.add("--build-source-package-only", "True")
    output_file = ctx.actions.declare_file(output_path + "/" + name)

    # TODO(ybaturina): Make this directory name dynamic to avoid collisions.
    copied_whl_srcs_dir = ctx.actions.declare_directory("copied_whl_srcs")
    outputs = [copied_whl_srcs_dir, output_file]
    args.add("--whl_dir", output_file.path[:output_file.path.rfind("/")])
    args.add("--copied_whl_srcs_dir", copied_whl_srcs_dir.path)
    args.add("--version=%s" % full_wheel_version)
    py_src_dir_file = ctx.attr.py_src_dir.files.to_list()[0]
    args.add("--src_directory", py_src_dir_file.path)
    args.set_param_file_format("flag_per_line")
    args.use_param_file("@%s", use_always = False)
    ctx.actions.run(
        arguments = [args],
        inputs = depset([py_src_dir_file]),
        outputs = outputs,
        executable = executable,
        mnemonic = "BuildTfKerasWheel",
    )

    return [DefaultInfo(files = depset(direct = [output_file]))]

_wheel = rule(
    attrs = {
        "wheel_binary": attr.label(
            default = Label("//tf_keras/wheel:build_wheel_py"),
            executable = True,
            cfg = "exec",
        ),
        "build_wheel_only": attr.bool(mandatory = True, default = False),
        "build_source_package_only": attr.bool(mandatory = True, default = False),
        "py_src_dir": attr.label(
            mandatory = True,
            doc = "A target that outputs a directory containing Python source files.",
        ),
        "output_path": attr.label(default = Label("//tf_keras/wheel:output_path")),
    },
    implementation = _wheel_impl,
    executable = False,
)

def _tf_keras_wheel_sources_impl(ctx):
    executable = ctx.executable.wheel_binary
    is_nightly = _is_nightly_build()
    output_dir = ctx.actions.declare_directory("wheel_sources")
    outputs = [output_dir]
    srcs = []
    args = ctx.actions.args()
    args.add("--output_path", output_dir.path)
    if is_nightly:
        args.add("--nightly")
    args.add("--version=%s" % (WHEEL_VERSION + WHEEL_VERSION_SUFFIX))
    for src in ctx.attr.srcs:
        for f in src.files.to_list():
            srcs.append(f)
            args.add("--srcs=%s" % (f.path))

    args.set_param_file_format("flag_per_line")
    args.use_param_file("@%s", use_always = False)
    ctx.actions.run(
        arguments = [args],
        inputs = srcs,
        outputs = outputs,
        executable = executable,
        mnemonic = "GatherWheelSources",
    )

    return [DefaultInfo(files = depset(direct = outputs))]

_tf_keras_wheel_sources = rule(
    attrs = {
        "wheel_binary": attr.label(
            default = Label("//tf_keras/wheel:create_wheel_dir_py"),
            executable = True,
            cfg = "exec",
        ),
        "srcs": attr.label_list(allow_files = True),
    },
    implementation = _tf_keras_wheel_sources_impl,
    executable = False,
)

def wheel_sources(
        name,
        srcs = []):
    tf_keras_wheel_sources_name = name
    _tf_keras_wheel_sources(
        name = tf_keras_wheel_sources_name,
        srcs = srcs,
    )
    py_library(
        name = name + "_library",
        data = [":" + tf_keras_wheel_sources_name],
        imports = [tf_keras_wheel_sources_name],
        visibility = ["//visibility:public"],
    )

def tf_keras_wheel(
        name,
        py_src_dir = None):
    _wheel(
        name = name,
        build_wheel_only = True,
        build_source_package_only = False,
        py_src_dir = py_src_dir,
    )

def tf_keras_source_package(
        name,
        py_src_dir = None):
    _wheel(
        name = name,
        build_source_package_only = True,
        build_wheel_only = False,
        py_src_dir = py_src_dir,
    )

def _get_pypi_dep_for_release(is_true, is_false):
    is_nightly = _is_nightly_build()
    is_selfbuilt = _is_selfbuilt_build()
    if is_nightly or is_selfbuilt:
        return is_false
    else:
        return is_true

def get_pypi_tf_keras_wheel():
    is_nightly = _is_nightly_build()
    if is_nightly:
        return "@pypi_tf_keras_nightly//:whl"
    else:
        return "@pypi_tf_keras//:whl"

def get_pypi_tensorflow_pkg():
    return _get_pypi_dep_for_release(
        is_true = "@pypi_tensorflow//:pkg",
        is_false = "@pypi_tf_nightly//:pkg",
    )

def get_pypi_tensorflow_dep():
    return _get_pypi_dep_for_release(
        is_true = "@pypi//tensorflow",
        is_false = "@pypi//tf_nightly",
    )
