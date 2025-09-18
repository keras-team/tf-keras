load("@local_config_cuda//cuda:build_defs.bzl", "if_cuda")
load("@python_version_repo//:py_version.bzl", "REQUIREMENTS")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load(
    "@xla//third_party/py:py_import.bzl",
    "py_import",
)

exports_files(["oss_setup.py"])

compile_pip_requirements(
    name = "requirements",
    extra_args = [
        "--allow-unsafe",
        "--build-isolation",
        "--rebuild",
    ],
    generate_hashes = True,
    requirements_in = "requirements.in",
    requirements_txt = REQUIREMENTS,
)

py_import(
    name = "tf_nightly_with_deps",
    wheel = "@pypi//tf_nightly:whl",
    wheel_deps = if_cuda([
        "@pypi_nvidia_cublas_cu12//:pkg",
        "@pypi_nvidia_cuda_cupti_cu12//:pkg",
        "@pypi_nvidia_cuda_nvcc_cu12//:pkg",
        "@pypi_nvidia_cuda_nvrtc_cu12//:pkg",
        "@pypi_nvidia_cuda_runtime_cu12//:pkg",
        "@pypi_nvidia_cudnn_cu12//:pkg",
        "@pypi_nvidia_cufft_cu12//:pkg",
        "@pypi_nvidia_curand_cu12//:pkg",
        "@pypi_nvidia_cusolver_cu12//:pkg",
        "@pypi_nvidia_cusparse_cu12//:pkg",
        "@pypi_nvidia_nccl_cu12//:pkg",
        "@pypi_nvidia_nvjitlink_cu12//:pkg",
    ]),
    deps = [
        "@pypi_absl_py//:pkg",
        "@pypi_astunparse//:pkg",
        "@pypi_flatbuffers//:pkg",
        "@pypi_gast//:pkg",
        "@pypi_ml_dtypes//:pkg",
        "@pypi_numpy//:pkg",
        "@pypi_opt_einsum//:pkg",
        "@pypi_packaging//:pkg",
        "@pypi_protobuf//:pkg",
        "@pypi_requests//:pkg",
        "@pypi_tensorboard//:pkg",
        "@pypi_termcolor//:pkg",
        "@pypi_typing_extensions//:pkg",
        "@pypi_wrapt//:pkg",
    ],
)
