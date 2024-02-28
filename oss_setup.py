# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
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
"""Setup script for the TF-Keras pip package."""

import os

import setuptools

DESCRIPTION = """TF-Keras is a deep learning API written in Python,
running on top of the machine learning platform TensorFlow.

It was developed with a focus on enabling fast experimentation and
providing a delightful developer experience.
The purpose of TF-Keras is to give an *unfair advantage* to any developer
looking to ship ML-powered apps.
"""

with open(os.path.abspath(__file__)) as f:
    contents = f.read()
    if contents.count("{PACKAGE}") > 1 or contents.count("{VERSION}") > 1:
        raise ValueError(
            "You must fill the 'PACKAGE' and 'VERSION' "
            "tags before running setup.py. If you are trying to "
            "build a fresh package, you should be using "
            "`pip_build.py` instead of `setup.py`."
        )

# pin version to that of tensorflow or tf_nightly.
version = "{{VERSION}}".lower()
if "nightly" in "{{PACKAGE}}":
    base_version = version.split(".dev")[0]  # 2.17.0.dev2024021419
    install_requires = [f"tf-nightly~={base_version}.dev"]
elif "rc" in version:
    base_version = version.split("rc")[0]  # 2.16.0rc0
    install_requires = [f"tensorflow~={base_version}rc"]
else:
    install_requires = ["tensorflow~={{VERSION}}"]

setuptools.setup(
    name="{{PACKAGE}}",
    # Version strings with `-` characters are semver compatible,
    # but incompatible with pip. For pip, we will remove all `-`` characters.
    version="{{VERSION}}",
    description="Deep learning for humans.",
    long_description=DESCRIPTION,
    url="https://keras.io/",
    download_url="https://github.com/keras-team/tf-keras/tags",
    author="Keras team",
    author_email="keras-users@googlegroups.com",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    # Supported Python versions
    python_requires=">=3.9",
    # PyPI package information.
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="Apache 2.0",
    keywords=["keras", "tensorflow", "machine learning", "deep learning"],
)
