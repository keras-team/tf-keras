workspace(name = "org_keras")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

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
    sha256 = "96ffcfd4a52bcb75d34b426f5a26d4e83a4dcf8f05bccf98e60d415a02ac6bca",
    strip_prefix = "xla-5a2c4befe808fbc894b55747d3c8955852a68ae6",
    urls = [
      "https://storage.googleapis.com/mirror.tensorflow.org/github.com/openxla/xla/archive/5a2c4befe808fbc894b55747d3c8955852a68ae6.tar.gz",
      "https://github.com/openxla/xla/archive/5a2c4befe808fbc894b55747d3c8955852a68ae6.tar.gz",
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
    sha256 = "bc283cdfcd526a52c3201279cda4bc298652efa898b10b4db0837dc51652756f",
    urls = [
        "https://storage.googleapis.com/mirror.tensorflow.org/github.com/bazelbuild/bazel-skylib/releases/download/1.7.1/bazel-skylib-1.7.1.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.7.1/bazel-skylib-1.7.1.tar.gz",
    ],
)

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

# Needed by protobuf
load("@xla//third_party/absl:workspace.bzl", absl = "repo")

absl()

# Needed by protobuf
http_archive(
    name = "rules_java",
    sha256 = "5449ed36d61269579dd9f4b0e532cd131840f285b389b3795ae8b4d717387dd8",
    urls = [
        "https://storage.googleapis.com/grpc-bazel-mirror/github.com/bazelbuild/rules_java/releases/download/8.7.0/rules_java-8.7.0.tar.gz",
        "https://github.com/bazelbuild/rules_java/releases/download/8.7.0/rules_java-8.7.0.tar.gz",
    ],
)

load("@rules_java//java:rules_java_deps.bzl", "rules_java_dependencies")

rules_java_dependencies()

maybe(
    tf_http_archive,
    name = "com_google_protobuf",
    patch_file = ["@xla//third_party/protobuf:protobuf.patch"],
    sha256 = "6e09bbc950ba60c3a7b30280210cd285af8d7d8ed5e0a6ed101c72aff22e8d88",
    strip_prefix = "protobuf-6.31.1",
    urls = tf_mirror_urls("https://github.com/protocolbuffers/protobuf/archive/refs/tags/v6.31.1.zip"),
    repo_mapping = {
        "@abseil-cpp": "@com_google_absl",
        "@protobuf_pip_deps": "@pypi",
    },
)

# ZLIB. Need by com_google_protobuf.
tf_http_archive(
    name = "zlib",
    build_file = "@com_google_protobuf//:third_party/zlib.BUILD",
    sha256 = "9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23",
    strip_prefix = "zlib-1.3.1",
    urls = tf_mirror_urls("https://zlib.net/fossils/zlib-1.3.1.tar.gz"),
)


load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
protobuf_deps()
