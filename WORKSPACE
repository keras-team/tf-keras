workspace(name = "org_keras")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

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

http_archive(
    name = "rules_python",
    sha256 = "8c8fe44ef0a9afc256d1e75ad5f448bb59b81aba149b8958f02f7b3a98f5d9b4",
    strip_prefix = "rules_python-0.13.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.13.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python3_10",
    python_version = "3.10",
    ignore_root_user_error = True,
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

http_archive(
    name = "com_google_protobuf",
    sha256 = "f645e6e42745ce922ca5388b1883ca583bafe4366cc74cf35c3c9299005136e2",
    strip_prefix = "protobuf-5.28.3",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v5.28.3.zip"],
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
