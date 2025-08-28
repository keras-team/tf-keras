workspace(name = "org_keras")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Toolchains for ML projects hermetic builds.
# Details: https://github.com/google-ml-infra/rules_ml_toolchain
http_archive(
    name = "rules_ml_toolchain",
    sha256 = "59d7eb36a02cbe3c2e2fa67fda5e8f1ab7e274bc4773bbd207c51fe199e11c19",
    strip_prefix = "rules_ml_toolchain-ffd9e3d7b84e43c2686c803cb08ce790ffd58baa",
    urls = [
        "https://github.com/google-ml-infra/rules_ml_toolchain/archive/ffd9e3d7b84e43c2686c803cb08ce790ffd58baa.tar.gz",
    ],
)

load(
    "@rules_ml_toolchain//cc/deps:cc_toolchain_deps.bzl",
    "cc_toolchain_deps",
)

cc_toolchain_deps()

register_toolchains("@rules_ml_toolchain//cc:linux_x86_64_linux_x86_64")

register_toolchains("@rules_ml_toolchain//cc:linux_x86_64_linux_x86_64_cuda")

http_archive(
    name = "xla",
    sha256 = "5b20a5fd981a23a5dea092f13f9279b5c2e8005b509ac141fb65f22a42ad35a9",
    strip_prefix = "xla-32b7537aee5a1e9145a6e11fc258347c41d6f5f8",
    urls = [
      "https://storage.googleapis.com/mirror.tensorflow.org/github.com/openxla/xla/archive/32b7537aee5a1e9145a6e11fc258347c41d6f5f8.tar.gz",
      "https://github.com/openxla/xla/archive/32b7537aee5a1e9145a6e11fc258347c41d6f5f8.tar.gz",
      ],
)

load("@xla//third_party:repo.bzl", "tf_http_archive", "tf_mirror_urls")

# Initialize hermetic Python
load("@xla//third_party/py:python_init_rules.bzl", "python_init_rules")

python_init_rules()

load("@xla//third_party/py:python_init_repositories.bzl", "python_init_repositories")

python_init_repositories(
    requirements = {
        "3.9": "//:requirements_lock_3_9.txt",
    },
    local_wheel_workspaces = ["//:WORKSPACE"],
    local_wheel_dist_folder = "dist",
    local_wheel_inclusion_list = [
        "tf_keras*",
        "tf_nightly*",
        "tf-keras*",
        "tf-nightly*",
        "tensorflow*",
        "keras*",
    ],
)

load("@xla//third_party/py:python_init_toolchains.bzl", "python_init_toolchains")

python_init_toolchains()

load("@xla//third_party/py:python_init_pip.bzl", "python_init_pip")

python_init_pip()

load("@pypi//:requirements.bzl", "install_deps")

install_deps()

load("//:tf_keras_python_wheel.bzl", "tf_keras_python_wheel_repository")

tf_keras_python_wheel_repository(
    name = "tf_keras_wheel",
    version_key = "__version__",
    version_source = "//tf_keras:__init__.py",
)

load(
    "@xla//third_party/py:python_wheel.bzl",
    "python_wheel_version_suffix_repository",
)

python_wheel_version_suffix_repository(
    name = "tf_keras_wheel_version_suffix",
)

load(
    "@rules_ml_toolchain//gpu/cuda:cuda_json_init_repository.bzl",
    "cuda_json_init_repository",
)

cuda_json_init_repository()

load(
    "@cuda_redist_json//:distributions.bzl",
    "CUDA_REDISTRIBUTIONS",
    "CUDNN_REDISTRIBUTIONS",
)
load(
    "@rules_ml_toolchain//gpu/cuda:cuda_redist_init_repositories.bzl",
    "cuda_redist_init_repositories",
    "cudnn_redist_init_repository",
)

cuda_redist_init_repositories(
    cuda_redistributions = CUDA_REDISTRIBUTIONS,
)

cudnn_redist_init_repository(
    cudnn_redistributions = CUDNN_REDISTRIBUTIONS,
)

load(
    "@rules_ml_toolchain//gpu/cuda:cuda_configure.bzl",
    "cuda_configure",
)

cuda_configure(name = "local_config_cuda")

# Needed by protobuf
http_archive(
    name = "bazel_skylib",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
    ],
    sha256 = "74d544d96f4a5bb630d465ca8bbcfe231e3594e5aae57e1edbf17a6eb3ca2506",
)
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()

# Needed by protobuf
http_archive(
    name = "six_archive",
    build_file = "//third_party:six.BUILD",
    sha256 = "1e61c37477a1626458e36f7b1d82aa5c9b094fa4802892072e49de9c60c4c926",
    strip_prefix = "six-1.16.0",
    urls = ["https://pypi.python.org/packages/source/s/six/six-1.16.0.tar.gz"],
)

bind(
    name = "six",
    actual = "@six_archive//:six",
)

tf_http_archive(
    name = "com_google_protobuf",
    patch_file = ["@xla//third_party/protobuf:protobuf.patch"],
    sha256 = "f645e6e42745ce922ca5388b1883ca583bafe4366cc74cf35c3c9299005136e2",
    strip_prefix = "protobuf-5.28.3",
    urls = tf_mirror_urls("https://github.com/protocolbuffers/protobuf/archive/refs/tags/v5.28.3.zip"),
)

# ZLIB. Need by com_google_protobuf.
http_archive(
    name = "zlib",
    build_file = "@com_google_protobuf//:third_party/zlib.BUILD",
    sha256 = "b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30",
    strip_prefix = "zlib-1.2.13",
    urls = [
      "https://storage.googleapis.com/mirror.tensorflow.org/zlib.net/zlib-1.2.13.tar.gz",
      "https://zlib.net/zlib-1.2.13.tar.gz",
      ],
)


load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
protobuf_deps()
