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
"""Guarded accessors for datasets and groups inside an HDF5 file.

A saved model is untrusted data, so reading one must not let the file drive
reads of the host filesystem or force an unbounded allocation. HDF5 offers
several ways to do exactly that, none of which a model file has any reason to
use: external storage (a dataset whose raw bytes live in a separate file),
external and soft links (an object that resolves elsewhere), virtual datasets
(a dataset mapped from other files), and datasets whose declared shape is far
larger than the bytes actually stored.

These helpers mirror `safe_get_h5_dataset` / `safe_get_h5_group` in Keras 3
(`keras/src/saving/saving_lib.py`), which is where the same guards landed for
CVE-2026-1669.
"""

import math

try:
    import h5py
except ImportError:
    h5py = None


# Guard against HDF5 "shape bomb" datasets: a dataset can declare an enormous
# shape while storing almost nothing on disk (e.g. chunked + gzip-compressed
# with only a fill value), which forces a huge allocation when it is read into
# memory (CWE-789 / CWE-409). For datasets whose declared in-memory size is
# above this floor, we require it to stay within `_H5_DATASET_MAX_EXPANSION` of
# the bytes actually stored on disk. Weights written by TF-Keras are dense and
# uncompressed, so they satisfy this; shape/decompression bombs, which store
# next to nothing, do not.
_H5_DATASET_BOMB_FLOOR_BYTES = 1 << 32  # 4 GiB
_H5_DATASET_MAX_EXPANSION = 1000


def safe_get_h5_group(parent, name):
    """Retrieves a Group within a given Group, rejecting unsafe links.

    Args:
        parent: the parent `h5py.Group`.
        name: the name of the Group to retrieve. May be a `/`-separated path.

    Returns:
        The child `h5py.Group`.

    Raises:
        ValueError: if any path component resolves through an external or soft
            link, or is not a Group.
        KeyError: if the path does not exist.
    """
    current = parent
    for name_part in name.split("/"):
        if not name_part:
            raise ValueError(f"Invalid path in H5 file: {name}")

        # Also handles the case when the group is an empty dict initially.
        if name_part not in current:
            raise KeyError(name)

        if isinstance(current, dict):
            group_type = None
        else:
            group_type = current.get(
                name_part, default=None, getclass=True, getlink=True
            )

        if group_type in (h5py.ExternalLink, h5py.SoftLink):
            raise ValueError(f"Not allowed: H5 file with {group_type.__name__}")

        current = current[name_part]
        if not isinstance(current, h5py.Group):
            raise ValueError(
                f"Invalid H5 file, expected Group but received {type(current)}"
            )

    return current


def safe_get_h5_dataset(group, name):
    """Retrieves a Dataset within a given Group, rejecting unsafe datasets.

    Args:
        group: the parent `h5py.Group`.
        name: the name of the Dataset to retrieve. May be a `/`-separated path.

    Returns:
        The child `h5py.Dataset`.

    Raises:
        ValueError: if the dataset resolves through an external or soft link,
            uses external or virtual storage, or declares a shape far larger
            than the bytes stored on disk.
        KeyError: if the path does not exist.
    """
    if "/" in name:
        # Separate the dataset name from its parent group.
        group_name, name = name.rsplit("/", 1)
        group = safe_get_h5_group(group, group_name)

    # Also handles the case when the group is an empty dict initially.
    if name not in group:
        raise KeyError(name)

    dataset_type = group.get(name, default=None, getclass=True, getlink=True)
    if dataset_type in (h5py.ExternalLink, h5py.SoftLink):
        raise ValueError(f"Not allowed: H5 file with {dataset_type.__name__}")

    dataset = group[name]
    if not isinstance(dataset, h5py.Dataset):
        raise ValueError(
            f"Invalid H5 file, expected Dataset, received {type(dataset)}"
        )
    if dataset.external:
        raise ValueError(
            f"Not allowed: H5 file with external Dataset: {dataset.external}"
        )
    if dataset.is_virtual:
        raise ValueError("Not allowed: H5 file with virtual Dataset")
    declared_bytes = math.prod(dataset.shape) * dataset.dtype.itemsize
    stored_bytes = dataset.id.get_storage_size()
    if (
        declared_bytes > _H5_DATASET_BOMB_FLOOR_BYTES
        and declared_bytes > _H5_DATASET_MAX_EXPANSION * stored_bytes
    ):
        raise ValueError(
            "Not allowed: H5 file with a Dataset declaring "
            f"{declared_bytes} bytes but storing only {stored_bytes} bytes"
        )
    return dataset
