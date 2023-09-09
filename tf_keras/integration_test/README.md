# TF-Keras Integration Test

This package contains integration tests that ensure the correct interaction
between TF-Keras and other Tensorflow high level APIs, like dataset, TF function
and distribution strategy, etc.

There are a few guidelines for the tests under this package.

*. Only use the public TF API.
*. Test should focus on the end to end use case between TF-Keras and other TF high
   level API. Unit test will be a better place for behavior testing for the
   individual APIs.
