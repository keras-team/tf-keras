# Copyright 2026 The TensorFlow Authors. All Rights Reserved.
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
"""Tests for the guarded HDF5 accessors."""

import os

import numpy as np
import tensorflow.compat.v2 as tf

from tf_keras.saving import h5_utils

try:
    import h5py
except ImportError:
    h5py = None


class SafeH5AccessTest(tf.test.TestCase):
    def _path(self, name):
        return os.path.join(self.get_temp_dir(), name)

    def test_reads_a_regular_dataset(self):
        path = self._path("plain.h5")
        with h5py.File(path, "w") as f:
            f.create_group("g").create_dataset("d", data=np.arange(4))

        with h5py.File(path, "r") as f:
            self.assertAllEqual(
                np.asarray(h5_utils.safe_get_h5_dataset(f["g"], "d")),
                np.arange(4),
            )
            # A `/`-separated path resolves through the parent group.
            self.assertAllEqual(
                np.asarray(h5_utils.safe_get_h5_dataset(f, "g/d")),
                np.arange(4),
            )
            self.assertIsInstance(
                h5_utils.safe_get_h5_group(f, "g"), h5py.Group
            )

    def test_rejects_external_storage_dataset(self):
        # An external dataset stores its bytes in another file on the host, so
        # reading it would disclose that file's contents.
        secret = self._path("secret.bin")
        with open(secret, "wb") as f:
            f.write(b"S" * 32)
        path = self._path("external.h5")
        with h5py.File(path, "w") as f:
            f.create_dataset(
                "d",
                shape=(4,),
                dtype="float64",
                external=[(secret, 0, h5py.h5f.UNLIMITED)],
            )

        with h5py.File(path, "r") as f:
            with self.assertRaisesRegex(ValueError, "external Dataset"):
                h5_utils.safe_get_h5_dataset(f, "d")

    def test_rejects_external_and_soft_links(self):
        other = self._path("other.h5")
        with h5py.File(other, "w") as f:
            f.create_dataset("d", data=np.arange(4))
            f.create_group("g")
        path = self._path("linked.h5")
        with h5py.File(path, "w") as f:
            f["ext_dataset"] = h5py.ExternalLink(other, "d")
            f["ext_group"] = h5py.ExternalLink(other, "g")
            f.create_dataset("real", data=np.arange(4))
            f["soft_dataset"] = h5py.SoftLink("/real")

        with h5py.File(path, "r") as f:
            with self.assertRaisesRegex(ValueError, "ExternalLink"):
                h5_utils.safe_get_h5_dataset(f, "ext_dataset")
            with self.assertRaisesRegex(ValueError, "SoftLink"):
                h5_utils.safe_get_h5_dataset(f, "soft_dataset")
            with self.assertRaisesRegex(ValueError, "ExternalLink"):
                h5_utils.safe_get_h5_group(f, "ext_group")

    def test_rejects_virtual_dataset(self):
        source = self._path("source.h5")
        with h5py.File(source, "w") as f:
            f.create_dataset("d", data=np.arange(4, dtype="float64"))
        path = self._path("virtual.h5")
        layout = h5py.VirtualLayout(shape=(4,), dtype="float64")
        layout[:] = h5py.VirtualSource(source, "d", shape=(4,))
        with h5py.File(path, "w") as f:
            f.create_virtual_dataset("d", layout)

        with h5py.File(path, "r") as f:
            with self.assertRaisesRegex(ValueError, "virtual Dataset"):
                h5_utils.safe_get_h5_dataset(f, "d")

    def test_rejects_shape_bomb(self):
        # A tiny file can declare a dataset far larger than it stores, which
        # would force an enormous allocation when read.
        path = self._path("bomb.h5")
        with h5py.File(path, "w") as f:
            f.create_dataset(
                "d", shape=(10**11,), dtype="float64", compression="gzip"
            )

        with h5py.File(path, "r") as f:
            with self.assertRaisesRegex(ValueError, "storing only"):
                h5_utils.safe_get_h5_dataset(f, "d")

    def test_accepts_dataset_below_the_bomb_floor(self):
        # The bomb guard has a 4 GiB floor, so ordinary weights are unaffected
        # no matter how well they compress.
        path = self._path("large.h5")
        with h5py.File(path, "w") as f:
            f.create_dataset(
                "d", data=np.zeros(1024, dtype="float64"), compression="gzip"
            )

        with h5py.File(path, "r") as f:
            self.assertEqual(
                h5_utils.safe_get_h5_dataset(f, "d").shape, (1024,)
            )

    def test_raises_for_missing_and_wrong_type(self):
        path = self._path("shapes.h5")
        with h5py.File(path, "w") as f:
            f.create_group("g").create_dataset("d", data=np.arange(4))

        with h5py.File(path, "r") as f:
            with self.assertRaises(KeyError):
                h5_utils.safe_get_h5_dataset(f, "nope")
            with self.assertRaises(KeyError):
                h5_utils.safe_get_h5_group(f, "nope")
            with self.assertRaisesRegex(ValueError, "expected Dataset"):
                h5_utils.safe_get_h5_dataset(f, "g")
            with self.assertRaisesRegex(ValueError, "expected Group"):
                h5_utils.safe_get_h5_group(f, "g/d")


if __name__ == "__main__":
    if h5py is not None:
        tf.test.main()
