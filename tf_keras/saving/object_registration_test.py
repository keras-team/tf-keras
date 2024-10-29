# Copyright 2022 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for TF-Keras serializable object registration functionality."""

import tensorflow.compat.v2 as tf

import tf_keras as keras
from tf_keras.saving import object_registration
from tf_keras.saving import serialization_lib


class TestObjectRegistration(tf.test.TestCase):
    def test_custom_object_scope(self):
        def custom_fn():
            pass

        class CustomClass:
            pass

        def check_get_in_thread():
            with object_registration.custom_object_scope(
                {"CustomClass": CustomClass, "custom_fn": custom_fn}
            ):
                actual_custom_fn = keras.activations.get("custom_fn")
                self.assertEqual(actual_custom_fn, custom_fn)
                actual_custom_class = keras.regularizers.get("CustomClass")
                self.assertEqual(actual_custom_class.__class__, CustomClass)

            with object_registration.custom_object_scope(
                {"CustomClass": CustomClass, "custom_fn": custom_fn}
            ):
                actual_custom_fn = keras.activations.get("custom_fn")
                self.assertEqual(actual_custom_fn, custom_fn)
                actual_custom_class = keras.regularizers.get("CustomClass")
                self.assertEqual(actual_custom_class.__class__, CustomClass)
                checked_thread = self.checkedThread(check_get_in_thread)
                checked_thread.start()
                checked_thread.join()

    def test_serialize_custom_class_with_default_name(self):
        @object_registration.register_keras_serializable()
        class TestClass:
            def __init__(self, value):
                self._value = value

            def get_config(self):
                return {"value": self._value}

            @classmethod
            def from_config(cls, config):
                return cls(**config)

        serialized_name = "Custom>TestClass"
        inst = TestClass(value=10)
        class_name = object_registration._GLOBAL_CUSTOM_NAMES[TestClass]
        self.assertEqual(serialized_name, class_name)
        config = serialization_lib.serialize_keras_object(inst)
        if tf.__internal__.tf2.enabled():
            self.assertEqual(class_name, config["registered_name"])
        else:
            self.assertEqual(class_name, config["class_name"])
        new_inst = serialization_lib.deserialize_keras_object(config)
        self.assertIsNot(inst, new_inst)
        self.assertIsInstance(new_inst, TestClass)
        self.assertEqual(10, new_inst._value)

    def test_serialize_custom_class_with_custom_name(self):
        @object_registration.register_keras_serializable(
            "TestPackage", "CustomName"
        )
        class OtherTestClass:
            def __init__(self, val):
                self._val = val

            def get_config(self):
                return {"val": self._val}

            @classmethod
            def from_config(cls, config):
                return cls(**config)

        serialized_name = "TestPackage>CustomName"
        inst = OtherTestClass(val=5)
        class_name = object_registration._GLOBAL_CUSTOM_NAMES[OtherTestClass]
        self.assertEqual(serialized_name, class_name)
        fn_class_name = object_registration.get_registered_name(OtherTestClass)
        self.assertEqual(fn_class_name, class_name)

        cls = object_registration.get_registered_object(fn_class_name)
        self.assertEqual(OtherTestClass, cls)

        config = serialization_lib.serialize_keras_object(inst)
        if tf.__internal__.tf2.enabled():
            self.assertEqual(class_name, config["registered_name"])
        else:
            self.assertEqual(class_name, config["class_name"])
        new_inst = serialization_lib.deserialize_keras_object(config)
        self.assertIsNot(inst, new_inst)
        self.assertIsInstance(new_inst, OtherTestClass)
        self.assertEqual(5, new_inst._val)

    def test_serialize_custom_function(self):
        @object_registration.register_keras_serializable(
            package="Test", name="func"
        )
        def my_fn():
            return 42

        serialized_name = "Test>func"
        class_name = object_registration._GLOBAL_CUSTOM_NAMES[my_fn]
        self.assertEqual(serialized_name, class_name)
        fn_class_name = object_registration.get_registered_name(my_fn)
        self.assertEqual(fn_class_name, class_name)

        config = serialization_lib.serialize_keras_object(my_fn)
        if tf.__internal__.tf2.enabled():
            self.assertEqual(serialized_name, config["config"])
        else:
            self.assertEqual(serialized_name, config)
        fn = serialization_lib.deserialize_keras_object(config)
        self.assertEqual(42, fn())

        fn_2 = object_registration.get_registered_object(fn_class_name)
        self.assertEqual(42, fn_2())

    def test_serialize_custom_class_without_get_config_fails(self):
        with self.assertRaisesRegex(
            ValueError,
            "Cannot register a class that does not have a get_config.*",
        ):

            @object_registration.register_keras_serializable(
                "TestPackage", "TestClass"
            )
            class TestClass:
                def __init__(self, value):
                    self._value = value


if __name__ == "__main__":
    tf.test.main()
