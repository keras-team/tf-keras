workspace(name = "org_keras")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Needed by protobuf
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
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

http_archive(
    name = "com_google_protobuf",
    sha256 = "6b1040a5661cd5f6e610cbca9cfaa2a17d60e2bb545309bc1b278bb05be44bdd",
    strip_prefix = "protobuf-4.21.6",
    urls = ["https://files.pythonhosted.org/packages/0e/25/693cd589793e7ae429ef76ab08f74b7866d342fd079cc4c723141a9660d3/protobuf-4.21.6.tar.gz"],
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
