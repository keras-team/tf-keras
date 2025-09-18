# Description:
#   Contains TF-Keras protobufs

load("@com_google_protobuf//bazel:proto_library.bzl", "proto_library")
load("@com_google_protobuf//bazel:py_proto_library.bzl", "py_proto_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],  # Apache 2.0
)

py_proto_library(
    name = "saved_metadata_proto_py_pb2",
    deps = [":saved_metadata_proto"],
)

py_proto_library(
    name = "projector_config_proto_py_pb2",
    deps = [":projector_config_proto"],
)

py_proto_library(
    name = "versions_proto_py_pb2",
    deps = [":versions_proto"],
)

proto_library(
    name = "versions_proto",
    srcs = ["versions.proto"],
)

proto_library(
    name = "projector_config_proto",
    srcs = ["projector_config.proto"],
)

proto_library(
    name = "saved_metadata_proto",
    srcs = ["saved_metadata.proto"],
    deps = [":versions_proto"],
)
