# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
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
"""Tests for confusion metrics."""

import json

import numpy as np
import tensorflow.compat.v2 as tf
from absl.testing import parameterized
from tensorflow.python.platform import tf_logging

from tf_keras import backend
from tf_keras import layers
from tf_keras import metrics
from tf_keras import models
from tf_keras.testing_infra import test_combinations
from tf_keras.testing_infra import test_utils
from tf_keras.utils import metrics_utils


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class FalsePositivesTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        fp_obj = metrics.FalsePositives(name="my_fp", thresholds=[0.4, 0.9])
        self.assertEqual(fp_obj.name, "my_fp")
        self.assertLen(fp_obj.variables, 1)
        self.assertEqual(fp_obj.thresholds, [0.4, 0.9])

        # Check save and restore config
        fp_obj2 = metrics.FalsePositives.from_config(fp_obj.get_config())
        self.assertEqual(fp_obj2.name, "my_fp")
        self.assertLen(fp_obj2.variables, 1)
        self.assertEqual(fp_obj2.thresholds, [0.4, 0.9])

    def test_unweighted(self):
        fp_obj = metrics.FalsePositives()
        self.evaluate(tf.compat.v1.variables_initializer(fp_obj.variables))

        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )

        update_op = fp_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = fp_obj.result()
        self.assertAllClose(7.0, result)

    def test_weighted(self):
        fp_obj = metrics.FalsePositives()
        self.evaluate(tf.compat.v1.variables_initializer(fp_obj.variables))
        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )
        sample_weight = tf.constant((1.0, 1.5, 2.0, 2.5))
        result = fp_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose(14.0, self.evaluate(result))

    def test_unweighted_with_thresholds(self):
        fp_obj = metrics.FalsePositives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(fp_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )

        update_op = fp_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = fp_obj.result()
        self.assertAllClose([7.0, 4.0, 2.0], result)

    def test_weighted_with_thresholds(self):
        fp_obj = metrics.FalsePositives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(fp_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )
        sample_weight = (
            (1.0, 2.0, 3.0, 5.0),
            (7.0, 11.0, 13.0, 17.0),
            (19.0, 23.0, 29.0, 31.0),
            (5.0, 15.0, 10.0, 0),
        )

        result = fp_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose([125.0, 42.0, 12.0], self.evaluate(result))

    def test_threshold_limit(self):
        with self.assertRaisesRegex(
            ValueError,
            r"Threshold values must be in \[0, 1\]. Received: \[-1, 2\]",
        ):
            metrics.FalsePositives(thresholds=[-1, 0.5, 2])

        with self.assertRaisesRegex(
            ValueError,
            r"Threshold values must be in \[0, 1\]. Received: \[None\]",
        ):
            metrics.FalsePositives(thresholds=[None])


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class FalseNegativesTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        fn_obj = metrics.FalseNegatives(name="my_fn", thresholds=[0.4, 0.9])
        self.assertEqual(fn_obj.name, "my_fn")
        self.assertLen(fn_obj.variables, 1)
        self.assertEqual(fn_obj.thresholds, [0.4, 0.9])

        # Check save and restore config
        fn_obj2 = metrics.FalseNegatives.from_config(fn_obj.get_config())
        self.assertEqual(fn_obj2.name, "my_fn")
        self.assertLen(fn_obj2.variables, 1)
        self.assertEqual(fn_obj2.thresholds, [0.4, 0.9])

    def test_unweighted(self):
        fn_obj = metrics.FalseNegatives()
        self.evaluate(tf.compat.v1.variables_initializer(fn_obj.variables))

        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )

        update_op = fn_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = fn_obj.result()
        self.assertAllClose(3.0, result)

    def test_weighted(self):
        fn_obj = metrics.FalseNegatives()
        self.evaluate(tf.compat.v1.variables_initializer(fn_obj.variables))
        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )
        sample_weight = tf.constant((1.0, 1.5, 2.0, 2.5))
        result = fn_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose(5.0, self.evaluate(result))

    def test_unweighted_with_thresholds(self):
        fn_obj = metrics.FalseNegatives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(fn_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )

        update_op = fn_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = fn_obj.result()
        self.assertAllClose([1.0, 4.0, 6.0], result)

    def test_weighted_with_thresholds(self):
        fn_obj = metrics.FalseNegatives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(fn_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )
        sample_weight = ((3.0,), (5.0,), (7.0,), (4.0,))

        result = fn_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose([4.0, 16.0, 23.0], self.evaluate(result))


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class TrueNegativesTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        tn_obj = metrics.TrueNegatives(name="my_tn", thresholds=[0.4, 0.9])
        self.assertEqual(tn_obj.name, "my_tn")
        self.assertLen(tn_obj.variables, 1)
        self.assertEqual(tn_obj.thresholds, [0.4, 0.9])

        # Check save and restore config
        tn_obj2 = metrics.TrueNegatives.from_config(tn_obj.get_config())
        self.assertEqual(tn_obj2.name, "my_tn")
        self.assertLen(tn_obj2.variables, 1)
        self.assertEqual(tn_obj2.thresholds, [0.4, 0.9])

    def test_unweighted(self):
        tn_obj = metrics.TrueNegatives()
        self.evaluate(tf.compat.v1.variables_initializer(tn_obj.variables))

        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )

        update_op = tn_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = tn_obj.result()
        self.assertAllClose(3.0, result)

    def test_weighted(self):
        tn_obj = metrics.TrueNegatives()
        self.evaluate(tf.compat.v1.variables_initializer(tn_obj.variables))
        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )
        sample_weight = tf.constant((1.0, 1.5, 2.0, 2.5))
        result = tn_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose(4.0, self.evaluate(result))

    def test_unweighted_with_thresholds(self):
        tn_obj = metrics.TrueNegatives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(tn_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )

        update_op = tn_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = tn_obj.result()
        self.assertAllClose([2.0, 5.0, 7.0], result)

    def test_weighted_with_thresholds(self):
        tn_obj = metrics.TrueNegatives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(tn_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )
        sample_weight = ((0.0, 2.0, 3.0, 5.0),)

        result = tn_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose([5.0, 15.0, 23.0], self.evaluate(result))


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class TruePositivesTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        tp_obj = metrics.TruePositives(name="my_tp", thresholds=[0.4, 0.9])
        self.assertEqual(tp_obj.name, "my_tp")
        self.assertLen(tp_obj.variables, 1)
        self.assertEqual(tp_obj.thresholds, [0.4, 0.9])

        # Check save and restore config
        tp_obj2 = metrics.TruePositives.from_config(tp_obj.get_config())
        self.assertEqual(tp_obj2.name, "my_tp")
        self.assertLen(tp_obj2.variables, 1)
        self.assertEqual(tp_obj2.thresholds, [0.4, 0.9])

    def test_unweighted(self):
        tp_obj = metrics.TruePositives()
        self.evaluate(tf.compat.v1.variables_initializer(tp_obj.variables))

        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )

        update_op = tp_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = tp_obj.result()
        self.assertAllClose(7.0, result)

    def test_weighted(self):
        tp_obj = metrics.TruePositives()
        self.evaluate(tf.compat.v1.variables_initializer(tp_obj.variables))
        y_true = tf.constant(
            ((0, 1, 0, 1, 0), (0, 0, 1, 1, 1), (1, 1, 1, 1, 0), (0, 0, 0, 0, 1))
        )
        y_pred = tf.constant(
            ((0, 0, 1, 1, 0), (1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 1, 1, 1, 1))
        )
        sample_weight = tf.constant((1.0, 1.5, 2.0, 2.5))
        result = tp_obj(y_true, y_pred, sample_weight=sample_weight)
        self.assertAllClose(12.0, self.evaluate(result))

    def test_unweighted_with_thresholds(self):
        tp_obj = metrics.TruePositives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(tp_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )

        update_op = tp_obj.update_state(y_true, y_pred)
        self.evaluate(update_op)
        result = tp_obj.result()
        self.assertAllClose([6.0, 3.0, 1.0], result)

    def test_weighted_with_thresholds(self):
        tp_obj = metrics.TruePositives(thresholds=[0.15, 0.5, 0.85])
        self.evaluate(tf.compat.v1.variables_initializer(tp_obj.variables))

        y_pred = tf.constant(
            (
                (0.9, 0.2, 0.8, 0.1),
                (0.2, 0.9, 0.7, 0.6),
                (0.1, 0.2, 0.4, 0.3),
                (0, 1, 0.7, 0.3),
            )
        )
        y_true = tf.constant(
            ((0, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1))
        )

        result = tp_obj(y_true, y_pred, sample_weight=37.0)
        self.assertAllClose([222.0, 111.0, 37.0], self.evaluate(result))


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class PrecisionTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        p_obj = metrics.Precision(
            name="my_precision", thresholds=[0.4, 0.9], top_k=15, class_id=12
        )
        self.assertEqual(p_obj.name, "my_precision")
        self.assertLen(p_obj.variables, 2)
        self.assertEqual(
            [v.name for v in p_obj.variables],
            ["true_positives:0", "false_positives:0"],
        )
        self.assertEqual(p_obj.thresholds, [0.4, 0.9])
        self.assertEqual(p_obj.top_k, 15)
        self.assertEqual(p_obj.class_id, 12)

        # Check save and restore config
        p_obj2 = metrics.Precision.from_config(p_obj.get_config())
        self.assertEqual(p_obj2.name, "my_precision")
        self.assertLen(p_obj2.variables, 2)
        self.assertEqual(p_obj2.thresholds, [0.4, 0.9])
        self.assertEqual(p_obj2.top_k, 15)
        self.assertEqual(p_obj2.class_id, 12)

    def test_value_is_idempotent(self):
        p_obj = metrics.Precision(thresholds=[0.3, 0.72])
        y_pred = tf.random.uniform(shape=(10, 3))
        y_true = tf.random.uniform(shape=(10, 3))
        update_op = p_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_precision = self.evaluate(p_obj.result())
        for _ in range(10):
            self.assertArrayNear(
                initial_precision, self.evaluate(p_obj.result()), 1e-3
            )

    def test_unweighted(self):
        p_obj = metrics.Precision()
        y_pred = tf.constant([1, 0, 1, 0], shape=(1, 4))
        y_true = tf.constant([0, 1, 1, 0], shape=(1, 4))
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))

    def test_unweighted_all_incorrect(self):
        p_obj = metrics.Precision(thresholds=[0.5])
        inputs = np.random.randint(0, 2, size=(100, 1))
        y_pred = tf.constant(inputs)
        y_true = tf.constant(1 - inputs)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(0, self.evaluate(result))

    def test_weighted(self):
        p_obj = metrics.Precision()
        y_pred = tf.constant([[1, 0, 1, 0], [1, 0, 1, 0]])
        y_true = tf.constant([[0, 1, 1, 0], [1, 0, 0, 1]])
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(
            y_true,
            y_pred,
            sample_weight=tf.constant([[1, 2, 3, 4], [4, 3, 2, 1]]),
        )
        weighted_tp = 3.0 + 4.0
        weighted_positives = (1.0 + 3.0) + (4.0 + 2.0)
        expected_precision = weighted_tp / weighted_positives
        self.assertAlmostEqual(expected_precision, self.evaluate(result))

    def test_div_by_zero(self):
        p_obj = metrics.Precision()
        y_pred = tf.constant([0, 0, 0, 0])
        y_true = tf.constant([0, 0, 0, 0])
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred)
        self.assertEqual(0, self.evaluate(result))

    def test_unweighted_with_threshold(self):
        p_obj = metrics.Precision(thresholds=[0.5, 0.7])
        y_pred = tf.constant([1, 0, 0.6, 0], shape=(1, 4))
        y_true = tf.constant([0, 1, 1, 0], shape=(1, 4))
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred)
        self.assertArrayNear([0.5, 0.0], self.evaluate(result), 0)

    def test_weighted_with_threshold(self):
        p_obj = metrics.Precision(thresholds=[0.5, 1.0])
        y_true = tf.constant([[0, 1], [1, 0]], shape=(2, 2))
        y_pred = tf.constant([[1, 0], [0.6, 0]], shape=(2, 2), dtype=tf.float32)
        weights = tf.constant([[4, 0], [3, 1]], shape=(2, 2), dtype=tf.float32)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred, sample_weight=weights)
        weighted_tp = 0 + 3.0
        weighted_positives = (0 + 3.0) + (4.0 + 0.0)
        expected_precision = weighted_tp / weighted_positives
        self.assertArrayNear(
            [expected_precision, 0], self.evaluate(result), 1e-3
        )

    def test_multiple_updates(self):
        p_obj = metrics.Precision(thresholds=[0.5, 1.0])
        y_true = tf.constant([[0, 1], [1, 0]], shape=(2, 2))
        y_pred = tf.constant([[1, 0], [0.6, 0]], shape=(2, 2), dtype=tf.float32)
        weights = tf.constant([[4, 0], [3, 1]], shape=(2, 2), dtype=tf.float32)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        update_op = p_obj.update_state(y_true, y_pred, sample_weight=weights)
        for _ in range(2):
            self.evaluate(update_op)

        weighted_tp = (0 + 3.0) + (0 + 3.0)
        weighted_positives = ((0 + 3.0) + (4.0 + 0.0)) + (
            (0 + 3.0) + (4.0 + 0.0)
        )
        expected_precision = weighted_tp / weighted_positives
        self.assertArrayNear(
            [expected_precision, 0], self.evaluate(p_obj.result()), 1e-3
        )

    def test_unweighted_top_k(self):
        p_obj = metrics.Precision(top_k=3)
        y_pred = tf.constant([0.2, 0.1, 0.5, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1.0 / 3, self.evaluate(result))

    def test_weighted_top_k(self):
        p_obj = metrics.Precision(top_k=3)
        y_pred1 = tf.constant([0.2, 0.1, 0.4, 0, 0.2], shape=(1, 5))
        y_true1 = tf.constant([0, 1, 1, 0, 1], shape=(1, 5))
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
        self.evaluate(
            p_obj(
                y_true1, y_pred1, sample_weight=tf.constant([[1, 4, 2, 3, 5]])
            )
        )

        y_pred2 = tf.constant([0.2, 0.6, 0.4, 0.2, 0.2], shape=(1, 5))
        y_true2 = tf.constant([1, 0, 1, 1, 1], shape=(1, 5))
        result = p_obj(y_true2, y_pred2, sample_weight=tf.constant(3))

        tp = (2 + 5) + (3 + 3)
        predicted_positives = (1 + 2 + 5) + (3 + 3 + 3)
        expected_precision = tp / predicted_positives
        self.assertAlmostEqual(expected_precision, self.evaluate(result))

    def test_unweighted_class_id(self):
        p_obj = metrics.Precision(class_id=2)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))

        y_pred = tf.constant([0.2, 0.1, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(p_obj.false_positives))

        y_pred = tf.constant([0.2, 0.1, 0, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(p_obj.false_positives))

        y_pred = tf.constant([0.2, 0.1, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 0, 0, 0], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(1, self.evaluate(p_obj.false_positives))

    def test_unweighted_top_k_and_class_id(self):
        p_obj = metrics.Precision(class_id=2, top_k=2)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))

        y_pred = tf.constant([0.2, 0.6, 0.3, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(p_obj.false_positives))

        y_pred = tf.constant([1, 1, 0.9, 1, 1], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(p_obj.false_positives))

    def test_unweighted_top_k_and_threshold(self):
        p_obj = metrics.Precision(thresholds=0.7, top_k=2)
        self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))

        y_pred = tf.constant([0.2, 0.8, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 1], shape=(1, 5))
        result = p_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(p_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(p_obj.false_positives))


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class RecallTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        r_obj = metrics.Recall(
            name="my_recall", thresholds=[0.4, 0.9], top_k=15, class_id=12
        )
        self.assertEqual(r_obj.name, "my_recall")
        self.assertLen(r_obj.variables, 2)
        self.assertEqual(
            [v.name for v in r_obj.variables],
            ["true_positives:0", "false_negatives:0"],
        )
        self.assertEqual(r_obj.thresholds, [0.4, 0.9])
        self.assertEqual(r_obj.top_k, 15)
        self.assertEqual(r_obj.class_id, 12)

        # Check save and restore config
        r_obj2 = metrics.Recall.from_config(r_obj.get_config())
        self.assertEqual(r_obj2.name, "my_recall")
        self.assertLen(r_obj2.variables, 2)
        self.assertEqual(r_obj2.thresholds, [0.4, 0.9])
        self.assertEqual(r_obj2.top_k, 15)
        self.assertEqual(r_obj2.class_id, 12)

    def test_value_is_idempotent(self):
        r_obj = metrics.Recall(thresholds=[0.3, 0.72])
        y_pred = tf.random.uniform(shape=(10, 3))
        y_true = tf.random.uniform(shape=(10, 3))
        update_op = r_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_recall = self.evaluate(r_obj.result())
        for _ in range(10):
            self.assertArrayNear(
                initial_recall, self.evaluate(r_obj.result()), 1e-3
            )

    def test_unweighted(self):
        r_obj = metrics.Recall()
        y_pred = tf.constant([1, 0, 1, 0], shape=(1, 4))
        y_true = tf.constant([0, 1, 1, 0], shape=(1, 4))
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))

    def test_unweighted_all_incorrect(self):
        r_obj = metrics.Recall(thresholds=[0.5])
        inputs = np.random.randint(0, 2, size=(100, 1))
        y_pred = tf.constant(inputs)
        y_true = tf.constant(1 - inputs)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0, self.evaluate(result))

    def test_weighted(self):
        r_obj = metrics.Recall()
        y_pred = tf.constant([[1, 0, 1, 0], [0, 1, 0, 1]])
        y_true = tf.constant([[0, 1, 1, 0], [1, 0, 0, 1]])
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(
            y_true,
            y_pred,
            sample_weight=tf.constant([[1, 2, 3, 4], [4, 3, 2, 1]]),
        )
        weighted_tp = 3.0 + 1.0
        weighted_t = (2.0 + 3.0) + (4.0 + 1.0)
        expected_recall = weighted_tp / weighted_t
        self.assertAlmostEqual(expected_recall, self.evaluate(result))

    def test_div_by_zero(self):
        r_obj = metrics.Recall()
        y_pred = tf.constant([0, 0, 0, 0])
        y_true = tf.constant([0, 0, 0, 0])
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred)
        self.assertEqual(0, self.evaluate(result))

    def test_unweighted_with_threshold(self):
        r_obj = metrics.Recall(thresholds=[0.5, 0.7])
        y_pred = tf.constant([1, 0, 0.6, 0], shape=(1, 4))
        y_true = tf.constant([0, 1, 1, 0], shape=(1, 4))
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred)
        self.assertArrayNear([0.5, 0.0], self.evaluate(result), 0)

    def test_weighted_with_threshold(self):
        r_obj = metrics.Recall(thresholds=[0.5, 1.0])
        y_true = tf.constant([[0, 1], [1, 0]], shape=(2, 2))
        y_pred = tf.constant([[1, 0], [0.6, 0]], shape=(2, 2), dtype=tf.float32)
        weights = tf.constant([[1, 4], [3, 2]], shape=(2, 2), dtype=tf.float32)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred, sample_weight=weights)
        weighted_tp = 0 + 3.0
        weighted_positives = (0 + 3.0) + (4.0 + 0.0)
        expected_recall = weighted_tp / weighted_positives
        self.assertArrayNear([expected_recall, 0], self.evaluate(result), 1e-3)

    def test_multiple_updates(self):
        r_obj = metrics.Recall(thresholds=[0.5, 1.0])
        y_true = tf.constant([[0, 1], [1, 0]], shape=(2, 2))
        y_pred = tf.constant([[1, 0], [0.6, 0]], shape=(2, 2), dtype=tf.float32)
        weights = tf.constant([[1, 4], [3, 2]], shape=(2, 2), dtype=tf.float32)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        update_op = r_obj.update_state(y_true, y_pred, sample_weight=weights)
        for _ in range(2):
            self.evaluate(update_op)

        weighted_tp = (0 + 3.0) + (0 + 3.0)
        weighted_positives = ((0 + 3.0) + (4.0 + 0.0)) + (
            (0 + 3.0) + (4.0 + 0.0)
        )
        expected_recall = weighted_tp / weighted_positives
        self.assertArrayNear(
            [expected_recall, 0], self.evaluate(r_obj.result()), 1e-3
        )

    def test_unweighted_top_k(self):
        r_obj = metrics.Recall(top_k=3)
        y_pred = tf.constant([0.2, 0.1, 0.5, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))

    def test_weighted_top_k(self):
        r_obj = metrics.Recall(top_k=3)
        y_pred1 = tf.constant([0.2, 0.1, 0.4, 0, 0.2], shape=(1, 5))
        y_true1 = tf.constant([0, 1, 1, 0, 1], shape=(1, 5))
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
        self.evaluate(
            r_obj(
                y_true1, y_pred1, sample_weight=tf.constant([[1, 4, 2, 3, 5]])
            )
        )

        y_pred2 = tf.constant([0.2, 0.6, 0.4, 0.2, 0.2], shape=(1, 5))
        y_true2 = tf.constant([1, 0, 1, 1, 1], shape=(1, 5))
        result = r_obj(y_true2, y_pred2, sample_weight=tf.constant(3))

        tp = (2 + 5) + (3 + 3)
        positives = (4 + 2 + 5) + (3 + 3 + 3 + 3)
        expected_recall = tp / positives
        self.assertAlmostEqual(expected_recall, self.evaluate(result))

    def test_unweighted_class_id(self):
        r_obj = metrics.Recall(class_id=2)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))

        y_pred = tf.constant([0.2, 0.1, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(r_obj.false_negatives))

        y_pred = tf.constant([0.2, 0.1, 0, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(1, self.evaluate(r_obj.false_negatives))

        y_pred = tf.constant([0.2, 0.1, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 0, 0, 0], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(1, self.evaluate(r_obj.false_negatives))

    def test_unweighted_top_k_and_class_id(self):
        r_obj = metrics.Recall(class_id=2, top_k=2)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))

        y_pred = tf.constant([0.2, 0.6, 0.3, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(0, self.evaluate(r_obj.false_negatives))

        y_pred = tf.constant([1, 1, 0.9, 1, 1], shape=(1, 5))
        y_true = tf.constant([0, 1, 1, 0, 0], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.5, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(1, self.evaluate(r_obj.false_negatives))

    def test_unweighted_top_k_and_threshold(self):
        r_obj = metrics.Recall(thresholds=0.7, top_k=2)
        self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))

        y_pred = tf.constant([0.2, 0.8, 0.6, 0, 0.2], shape=(1, 5))
        y_true = tf.constant([1, 1, 1, 0, 1], shape=(1, 5))
        result = r_obj(y_true, y_pred)
        self.assertAlmostEqual(0.25, self.evaluate(result))
        self.assertAlmostEqual(1, self.evaluate(r_obj.true_positives))
        self.assertAlmostEqual(3, self.evaluate(r_obj.false_negatives))


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class SensitivityAtSpecificityTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        s_obj = metrics.SensitivityAtSpecificity(
            0.4,
            num_thresholds=100,
            class_id=12,
            name="sensitivity_at_specificity_1",
        )
        self.assertEqual(s_obj.name, "sensitivity_at_specificity_1")
        self.assertLen(s_obj.variables, 4)
        self.assertEqual(s_obj.specificity, 0.4)
        self.assertEqual(s_obj.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

        # Check save and restore config
        s_obj2 = metrics.SensitivityAtSpecificity.from_config(
            s_obj.get_config()
        )
        self.assertEqual(s_obj2.name, "sensitivity_at_specificity_1")
        self.assertLen(s_obj2.variables, 4)
        self.assertEqual(s_obj2.specificity, 0.4)
        self.assertEqual(s_obj2.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

    def test_value_is_idempotent(self):
        s_obj = metrics.SensitivityAtSpecificity(0.7)
        y_pred = tf.random.uniform((10, 3), maxval=1, dtype=tf.float32, seed=1)
        y_true = tf.random.uniform((10, 3), maxval=2, dtype=tf.int64, seed=1)
        update_op = s_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_sensitivity = self.evaluate(s_obj.result())
        for _ in range(10):
            self.assertAlmostEqual(
                initial_sensitivity, self.evaluate(s_obj.result()), 1e-3
            )

    def test_unweighted_all_correct(self):
        with self.test_session():
            s_obj = metrics.SensitivityAtSpecificity(0.7)
            inputs = np.random.randint(0, 2, size=(100, 1))
            y_pred = tf.constant(inputs, dtype=tf.float32)
            y_true = tf.constant(inputs)
            self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
            result = s_obj(y_true, y_pred)
            self.assertAlmostEqual(1, self.evaluate(result))

    def test_unweighted_high_specificity(self):
        s_obj = metrics.SensitivityAtSpecificity(0.8)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.1, 0.45, 0.5, 0.8, 0.9]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.8, self.evaluate(result))

    def test_unweighted_low_specificity(self):
        s_obj = metrics.SensitivityAtSpecificity(0.4)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.6, self.evaluate(result))

    def test_unweighted_class_id(self):
        s_obj = metrics.SpecificityAtSensitivity(0.4, class_id=2)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]

        y_pred = tf.transpose([pred_values] * 3)
        y_true = tf.one_hot(label_values, depth=3)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.6, self.evaluate(result))

    @parameterized.parameters([tf.bool, tf.int32, tf.float32])
    def test_weighted(self, label_dtype):
        s_obj = metrics.SensitivityAtSpecificity(0.4)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        weight_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.cast(label_values, dtype=label_dtype)
        weights = tf.constant(weight_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred, sample_weight=weights)
        self.assertAlmostEqual(0.675, self.evaluate(result))

    def test_invalid_specificity(self):
        with self.assertRaisesRegex(
            ValueError, r"`specificity` must be in the range \[0, 1\]."
        ):
            metrics.SensitivityAtSpecificity(-1)

    def test_invalid_num_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 0"
        ):
            metrics.SensitivityAtSpecificity(0.4, num_thresholds=-1)


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class SpecificityAtSensitivityTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        s_obj = metrics.SpecificityAtSensitivity(
            0.4,
            num_thresholds=100,
            class_id=12,
            name="specificity_at_sensitivity_1",
        )
        self.assertEqual(s_obj.name, "specificity_at_sensitivity_1")
        self.assertLen(s_obj.variables, 4)
        self.assertEqual(s_obj.sensitivity, 0.4)
        self.assertEqual(s_obj.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

        # Check save and restore config
        s_obj2 = metrics.SpecificityAtSensitivity.from_config(
            s_obj.get_config()
        )
        self.assertEqual(s_obj2.name, "specificity_at_sensitivity_1")
        self.assertLen(s_obj2.variables, 4)
        self.assertEqual(s_obj2.sensitivity, 0.4)
        self.assertEqual(s_obj2.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

    def test_value_is_idempotent(self):
        s_obj = metrics.SpecificityAtSensitivity(0.7)
        y_pred = tf.random.uniform((10, 3), maxval=1, dtype=tf.float32, seed=1)
        y_true = tf.random.uniform((10, 3), maxval=2, dtype=tf.int64, seed=1)
        update_op = s_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_specificity = self.evaluate(s_obj.result())
        for _ in range(10):
            self.assertAlmostEqual(
                initial_specificity, self.evaluate(s_obj.result()), 1e-3
            )

    def test_unweighted_all_correct(self):
        s_obj = metrics.SpecificityAtSensitivity(0.7)
        inputs = np.random.randint(0, 2, size=(100, 1))
        y_pred = tf.constant(inputs, dtype=tf.float32)
        y_true = tf.constant(inputs)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))

    def test_unweighted_high_sensitivity(self):
        s_obj = metrics.SpecificityAtSensitivity(1.0)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.2, self.evaluate(result))

    def test_unweighted_low_sensitivity(self):
        s_obj = metrics.SpecificityAtSensitivity(0.4)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.6, self.evaluate(result))

    def test_unweighted_class_id(self):
        s_obj = metrics.SpecificityAtSensitivity(0.4, class_id=2)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]

        y_pred = tf.transpose([pred_values] * 3)
        y_true = tf.one_hot(label_values, depth=3)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(0.6, self.evaluate(result))

    @parameterized.parameters([tf.bool, tf.int32, tf.float32])
    def test_weighted(self, label_dtype):
        s_obj = metrics.SpecificityAtSensitivity(0.4)
        pred_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.01, 0.02, 0.25, 0.26, 0.26]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        weight_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.cast(label_values, dtype=label_dtype)
        weights = tf.constant(weight_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred, sample_weight=weights)
        self.assertAlmostEqual(0.4, self.evaluate(result))

    def test_invalid_sensitivity(self):
        with self.assertRaisesRegex(
            ValueError, r"`sensitivity` must be in the range \[0, 1\]."
        ):
            metrics.SpecificityAtSensitivity(-1)

    def test_invalid_num_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 0"
        ):
            metrics.SpecificityAtSensitivity(0.4, num_thresholds=-1)


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class PrecisionAtRecallTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        s_obj = metrics.PrecisionAtRecall(
            0.4, num_thresholds=100, class_id=12, name="precision_at_recall_1"
        )
        self.assertEqual(s_obj.name, "precision_at_recall_1")
        self.assertLen(s_obj.variables, 4)
        self.assertEqual(s_obj.recall, 0.4)
        self.assertEqual(s_obj.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

        # Check save and restore config
        s_obj2 = metrics.PrecisionAtRecall.from_config(s_obj.get_config())
        self.assertEqual(s_obj2.name, "precision_at_recall_1")
        self.assertLen(s_obj2.variables, 4)
        self.assertEqual(s_obj2.recall, 0.4)
        self.assertEqual(s_obj2.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

    def test_value_is_idempotent(self):
        s_obj = metrics.PrecisionAtRecall(0.7)
        y_pred = tf.random.uniform((10, 3), maxval=1, dtype=tf.float32, seed=1)
        y_true = tf.random.uniform((10, 3), maxval=2, dtype=tf.int64, seed=1)
        update_op = s_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_precision = self.evaluate(s_obj.result())
        for _ in range(10):
            self.assertAlmostEqual(
                initial_precision, self.evaluate(s_obj.result()), 1e-3
            )

    def test_unweighted_all_correct(self):
        s_obj = metrics.PrecisionAtRecall(0.7)
        inputs = np.random.randint(0, 2, size=(100, 1))
        y_pred = tf.constant(inputs, dtype=tf.float32)
        y_true = tf.constant(inputs)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))

    def test_unweighted_high_recall(self):
        s_obj = metrics.PrecisionAtRecall(0.8)
        pred_values = [0.0, 0.1, 0.2, 0.5, 0.6, 0.2, 0.5, 0.6, 0.8, 0.9]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # For 0.5 < decision threshold < 0.6.
        self.assertAlmostEqual(2.0 / 3, self.evaluate(result))

    def test_unweighted_low_recall(self):
        s_obj = metrics.PrecisionAtRecall(0.6)
        pred_values = [0.0, 0.1, 0.2, 0.5, 0.6, 0.2, 0.5, 0.6, 0.8, 0.9]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # For 0.2 < decision threshold < 0.5.
        self.assertAlmostEqual(0.75, self.evaluate(result))

    def test_unweighted_class_id(self):
        s_obj = metrics.PrecisionAtRecall(0.6, class_id=2)
        pred_values = [0.0, 0.1, 0.2, 0.5, 0.6, 0.2, 0.5, 0.6, 0.8, 0.9]
        label_values = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]

        y_pred = tf.transpose([pred_values] * 3)
        y_true = tf.one_hot(label_values, depth=3)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # For 0.2 < decision threshold < 0.5.
        self.assertAlmostEqual(0.75, self.evaluate(result))

    @parameterized.parameters([tf.bool, tf.int32, tf.float32])
    def test_weighted(self, label_dtype):
        s_obj = metrics.PrecisionAtRecall(7.0 / 8)
        pred_values = [0.0, 0.1, 0.2, 0.5, 0.6, 0.2, 0.5, 0.6, 0.8, 0.9]
        label_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        weight_values = [2, 1, 2, 1, 2, 1, 2, 2, 1, 2]

        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.cast(label_values, dtype=label_dtype)
        weights = tf.constant(weight_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred, sample_weight=weights)
        # For 0.0 < decision threshold < 0.2.
        self.assertAlmostEqual(0.7, self.evaluate(result))

    def test_invalid_sensitivity(self):
        with self.assertRaisesRegex(
            ValueError, r"`recall` must be in the range \[0, 1\]."
        ):
            metrics.PrecisionAtRecall(-1)

    def test_invalid_num_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 0"
        ):
            metrics.PrecisionAtRecall(0.4, num_thresholds=-1)


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class RecallAtPrecisionTest(tf.test.TestCase, parameterized.TestCase):
    def test_config(self):
        s_obj = metrics.RecallAtPrecision(
            0.4, num_thresholds=100, class_id=12, name="recall_at_precision_1"
        )
        self.assertEqual(s_obj.name, "recall_at_precision_1")
        self.assertLen(s_obj.variables, 4)
        self.assertEqual(s_obj.precision, 0.4)
        self.assertEqual(s_obj.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

        # Check save and restore config
        s_obj2 = metrics.RecallAtPrecision.from_config(s_obj.get_config())
        self.assertEqual(s_obj2.name, "recall_at_precision_1")
        self.assertLen(s_obj2.variables, 4)
        self.assertEqual(s_obj2.precision, 0.4)
        self.assertEqual(s_obj2.num_thresholds, 100)
        self.assertEqual(s_obj.class_id, 12)

    def test_value_is_idempotent(self):
        s_obj = metrics.RecallAtPrecision(0.7)
        y_pred = tf.random.uniform((10, 3), maxval=1, dtype=tf.float32, seed=1)
        y_true = tf.random.uniform((10, 3), maxval=2, dtype=tf.int64, seed=1)
        update_op = s_obj.update_state(y_true, y_pred)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))

        # Run several updates.
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_recall = self.evaluate(s_obj.result())
        for _ in range(10):
            self.assertAlmostEqual(
                initial_recall, self.evaluate(s_obj.result()), 1e-3
            )

    def test_unweighted_all_correct(self):
        s_obj = metrics.RecallAtPrecision(0.7)
        inputs = np.random.randint(0, 2, size=(100, 1))
        y_pred = tf.constant(inputs, dtype=tf.float32)
        y_true = tf.constant(inputs)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        self.assertAlmostEqual(1, self.evaluate(result))

    def test_unweighted_high_precision(self):
        s_obj = metrics.RecallAtPrecision(0.75)
        pred_values = [
            0.05,
            0.1,
            0.2,
            0.3,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.6,
            0.9,
            0.95,
        ]
        label_values = [0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1]
        # precisions: [1/2, 6/11, 1/2, 5/9, 5/8, 5/7, 2/3, 3/5, 3/5, 2/3, 1/2,
        # 1].
        # recalls:    [1,   1,    5/6, 5/6, 5/6, 5/6, 2/3, 1/2, 1/2, 1/3, 1/6,
        # 1/6].
        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # The precision 0.75 can be reached at thresholds 0.4<=t<0.45.
        self.assertAlmostEqual(0.5, self.evaluate(result))

    def test_unweighted_low_precision(self):
        s_obj = metrics.RecallAtPrecision(2.0 / 3)
        pred_values = [
            0.05,
            0.1,
            0.2,
            0.3,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.6,
            0.9,
            0.95,
        ]
        label_values = [0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1]
        # precisions: [1/2, 6/11, 1/2, 5/9, 5/8, 5/7, 2/3, 3/5, 3/5, 2/3, 1/2,
        # 1].
        # recalls:    [1,   1,    5/6, 5/6, 5/6, 5/6, 2/3, 1/2, 1/2, 1/3, 1/6,
        # 1/6].
        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # The precision 5/7 can be reached at thresholds 00.3<=t<0.35.
        self.assertAlmostEqual(5.0 / 6, self.evaluate(result))

    def test_unweighted_class_id(self):
        s_obj = metrics.RecallAtPrecision(2.0 / 3, class_id=2)
        pred_values = [
            0.05,
            0.1,
            0.2,
            0.3,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.6,
            0.9,
            0.95,
        ]
        label_values = [0, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 2]
        # precisions: [1/2, 6/11, 1/2, 5/9, 5/8, 5/7, 2/3, 3/5, 3/5, 2/3, 1/2,
        # 1].
        # recalls:    [1,   1,    5/6, 5/6, 5/6, 5/6, 2/3, 1/2, 1/2, 1/3, 1/6,
        # 1/6].
        y_pred = tf.transpose([pred_values] * 3)
        y_true = tf.one_hot(label_values, depth=3)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # The precision 5/7 can be reached at thresholds 00.3<=t<0.35.
        self.assertAlmostEqual(5.0 / 6, self.evaluate(result))

    @parameterized.parameters([tf.bool, tf.int32, tf.float32])
    def test_weighted(self, label_dtype):
        s_obj = metrics.RecallAtPrecision(0.75)
        pred_values = [0.1, 0.2, 0.3, 0.5, 0.6, 0.9, 0.9]
        label_values = [0, 1, 0, 0, 0, 1, 1]
        weight_values = [1, 2, 1, 2, 1, 2, 1]
        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.cast(label_values, dtype=label_dtype)
        weights = tf.constant(weight_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred, sample_weight=weights)
        self.assertAlmostEqual(0.6, self.evaluate(result))

    def test_unachievable_precision(self):
        s_obj = metrics.RecallAtPrecision(2.0 / 3)
        pred_values = [0.1, 0.2, 0.3, 0.9]
        label_values = [1, 1, 0, 0]
        y_pred = tf.constant(pred_values, dtype=tf.float32)
        y_true = tf.constant(label_values)
        self.evaluate(tf.compat.v1.variables_initializer(s_obj.variables))
        result = s_obj(y_true, y_pred)
        # The highest possible precision is 1/2 which is below the required
        # value, expect 0 recall.
        self.assertAlmostEqual(0, self.evaluate(result))

    def test_invalid_sensitivity(self):
        with self.assertRaisesRegex(
            ValueError, r"`precision` must be in the range \[0, 1\]."
        ):
            metrics.RecallAtPrecision(-1)

    def test_invalid_num_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 0"
        ):
            metrics.RecallAtPrecision(0.4, num_thresholds=-1)


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class AUCTest(tf.test.TestCase, parameterized.TestCase):
    def setup(self):
        self.num_thresholds = 3
        self.y_pred = tf.constant([0, 0.5, 0.3, 0.9], dtype=tf.float32)
        self.y_pred_multi_label = tf.constant(
            [[0.0, 0.4], [0.5, 0.7], [0.3, 0.2], [0.9, 0.3]], dtype=tf.float32
        )
        epsilon = 1e-12
        self.y_pred_logits = -tf.math.log(1.0 / (self.y_pred + epsilon) - 1.0)
        self.y_true = tf.constant([0, 0, 1, 1])
        self.y_true_multi_label = tf.constant([[0, 0], [1, 1], [1, 1], [1, 0]])
        self.sample_weight = [1, 2, 3, 4]

        # threshold values are [0 - 1e-7, 0.5, 1 + 1e-7]
        # y_pred when threshold = 0 - 1e-7  : [1, 1, 1, 1]
        # y_pred when threshold = 0.5       : [0, 0, 0, 1]
        # y_pred when threshold = 1 + 1e-7  : [0, 0, 0, 0]

        # without sample_weight:
        # tp = np.sum([[0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]], axis=1)
        # fp = np.sum([[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], axis=1)
        # fn = np.sum([[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]], axis=1)
        # tn = np.sum([[0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]], axis=1)

        # tp = [2, 1, 0], fp = [2, 0, 0], fn = [0, 1, 2], tn = [0, 2, 2]

        # with sample_weight:
        # tp = np.sum([[0, 0, 3, 4], [0, 0, 0, 4], [0, 0, 0, 0]], axis=1)
        # fp = np.sum([[1, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], axis=1)
        # fn = np.sum([[0, 0, 0, 0], [0, 0, 3, 0], [0, 0, 3, 4]], axis=1)
        # tn = np.sum([[0, 0, 0, 0], [1, 2, 0, 0], [1, 2, 0, 0]], axis=1)

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]

    def test_config(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=100,
            curve="PR",
            summation_method="majoring",
            name="auc_1",
            dtype=tf.float64,
            multi_label=True,
            num_labels=2,
            from_logits=True,
        )
        auc_obj.update_state(self.y_true_multi_label, self.y_pred_multi_label)
        self.assertEqual(auc_obj.name, "auc_1")
        self.assertEqual(auc_obj._dtype, tf.float64)
        self.assertLen(auc_obj.variables, 4)
        self.assertEqual(auc_obj.num_thresholds, 100)
        self.assertEqual(auc_obj.curve, metrics_utils.AUCCurve.PR)
        self.assertEqual(
            auc_obj.summation_method, metrics_utils.AUCSummationMethod.MAJORING
        )
        self.assertTrue(auc_obj.multi_label)
        self.assertEqual(auc_obj.num_labels, 2)
        self.assertTrue(auc_obj._from_logits)
        old_config = auc_obj.get_config()
        self.assertNotIn("thresholds", old_config)
        self.assertDictEqual(old_config, json.loads(json.dumps(old_config)))

        # Check save and restore config.
        auc_obj2 = metrics.AUC.from_config(auc_obj.get_config())
        auc_obj2.update_state(self.y_true_multi_label, self.y_pred_multi_label)
        self.assertEqual(auc_obj2.name, "auc_1")
        self.assertLen(auc_obj2.variables, 4)
        self.assertEqual(auc_obj2.num_thresholds, 100)
        self.assertEqual(auc_obj2.curve, metrics_utils.AUCCurve.PR)
        self.assertEqual(
            auc_obj2.summation_method, metrics_utils.AUCSummationMethod.MAJORING
        )
        self.assertTrue(auc_obj2.multi_label)
        self.assertEqual(auc_obj2.num_labels, 2)
        self.assertTrue(auc_obj2._from_logits)
        new_config = auc_obj2.get_config()
        self.assertNotIn("thresholds", new_config)
        self.assertDictEqual(old_config, new_config)
        self.assertAllClose(auc_obj.thresholds, auc_obj2.thresholds)

    def test_config_manual_thresholds(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=None,
            curve="PR",
            summation_method="majoring",
            name="auc_1",
            thresholds=[0.3, 0.5],
        )
        auc_obj.update_state(self.y_true, self.y_pred)
        self.assertEqual(auc_obj.name, "auc_1")
        self.assertLen(auc_obj.variables, 4)
        self.assertEqual(auc_obj.num_thresholds, 4)
        self.assertAllClose(auc_obj.thresholds, [0.0, 0.3, 0.5, 1.0])
        self.assertEqual(auc_obj.curve, metrics_utils.AUCCurve.PR)
        self.assertEqual(
            auc_obj.summation_method, metrics_utils.AUCSummationMethod.MAJORING
        )
        old_config = auc_obj.get_config()
        self.assertDictEqual(old_config, json.loads(json.dumps(old_config)))

        # Check save and restore config.
        auc_obj2 = metrics.AUC.from_config(auc_obj.get_config())
        auc_obj2.update_state(self.y_true, self.y_pred)
        self.assertEqual(auc_obj2.name, "auc_1")
        self.assertLen(auc_obj2.variables, 4)
        self.assertEqual(auc_obj2.num_thresholds, 4)
        self.assertEqual(auc_obj2.curve, metrics_utils.AUCCurve.PR)
        self.assertEqual(
            auc_obj2.summation_method, metrics_utils.AUCSummationMethod.MAJORING
        )
        new_config = auc_obj2.get_config()
        self.assertDictEqual(old_config, new_config)
        self.assertAllClose(auc_obj.thresholds, auc_obj2.thresholds)

    def test_value_is_idempotent(self):
        self.setup()
        auc_obj = metrics.AUC(num_thresholds=3)
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))

        # Run several updates.
        update_op = auc_obj.update_state(self.y_true, self.y_pred)
        for _ in range(10):
            self.evaluate(update_op)

        # Then verify idempotency.
        initial_auc = self.evaluate(auc_obj.result())
        for _ in range(10):
            self.assertAllClose(
                initial_auc, self.evaluate(auc_obj.result()), 1e-3
            )

    def test_unweighted_all_correct(self):
        self.setup()
        auc_obj = metrics.AUC()
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true, self.y_true)
        self.assertEqual(self.evaluate(result), 1)

    def test_unweighted(self):
        self.setup()
        auc_obj = metrics.AUC(num_thresholds=self.num_thresholds)
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true, self.y_pred)

        # tp = [2, 1, 0], fp = [2, 0, 0], fn = [0, 1, 2], tn = [0, 2, 2]
        # recall = [2/2, 1/(1+1), 0] = [1, 0.5, 0]
        # fp_rate = [2/2, 0, 0] = [1, 0, 0]
        # heights = [(1 + 0.5)/2, (0.5 + 0)/2] = [0.75, 0.25]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 0.75 * 1 + 0.25 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_unweighted_from_logits(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, from_logits=True
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true, self.y_pred_logits)

        # tp = [2, 1, 0], fp = [2, 0, 0], fn = [0, 1, 2], tn = [0, 2, 2]
        # recall = [2/2, 1/(1+1), 0] = [1, 0.5, 0]
        # fp_rate = [2/2, 0, 0] = [1, 0, 0]
        # heights = [(1 + 0.5)/2, (0.5 + 0)/2] = [0.75, 0.25]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 0.75 * 1 + 0.25 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_manual_thresholds(self):
        self.setup()
        # Verify that when specified, thresholds are used instead of
        # num_thresholds.
        auc_obj = metrics.AUC(num_thresholds=2, thresholds=[0.5])
        self.assertEqual(auc_obj.num_thresholds, 3)
        self.assertAllClose(auc_obj.thresholds, [0.0, 0.5, 1.0])
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true, self.y_pred)

        # tp = [2, 1, 0], fp = [2, 0, 0], fn = [0, 1, 2], tn = [0, 2, 2]
        # recall = [2/2, 1/(1+1), 0] = [1, 0.5, 0]
        # fp_rate = [2/2, 0, 0] = [1, 0, 0]
        # heights = [(1 + 0.5)/2, (0.5 + 0)/2] = [0.75, 0.25]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 0.75 * 1 + 0.25 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_roc_interpolation(self):
        self.setup()
        auc_obj = metrics.AUC(num_thresholds=self.num_thresholds)
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # recall = [7/7, 4/(4+3), 0] = [1, 0.571, 0]
        # fp_rate = [3/3, 0, 0] = [1, 0, 0]
        # heights = [(1 + 0.571)/2, (0.571 + 0)/2] = [0.7855, 0.2855]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 0.7855 * 1 + 0.2855 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_roc_majoring(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, summation_method="majoring"
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # recall = [7/7, 4/(4+3), 0] = [1, 0.571, 0]
        # fp_rate = [3/3, 0, 0] = [1, 0, 0]
        # heights = [max(1, 0.571), max(0.571, 0)] = [1, 0.571]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 1 * 1 + 0.571 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_roc_minoring(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, summation_method="minoring"
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # recall = [7/7, 4/(4+3), 0] = [1, 0.571, 0]
        # fp_rate = [3/3, 0, 0] = [1, 0, 0]
        # heights = [min(1, 0.571), min(0.571, 0)] = [0.571, 0]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 0.571 * 1 + 0 * 0
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_pr_majoring(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            curve="PR",
            summation_method="majoring",
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # precision = [7/(7+3), 4/4, 0] = [0.7, 1, 0]
        # recall = [7/7, 4/(4+3), 0] = [1, 0.571, 0]
        # heights = [max(0.7, 1), max(1, 0)] = [1, 1]
        # widths = [(1 - 0.571), (0.571 - 0)] = [0.429, 0.571]
        expected_result = 1 * 0.429 + 1 * 0.571
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_pr_minoring(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            curve="PR",
            summation_method="minoring",
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # precision = [7/(7+3), 4/4, 0] = [0.7, 1, 0]
        # recall = [7/7, 4/(4+3), 0] = [1, 0.571, 0]
        # heights = [min(0.7, 1), min(1, 0)] = [0.7, 0]
        # widths = [(1 - 0.571), (0.571 - 0)] = [0.429, 0.571]
        expected_result = 0.7 * 0.429 + 0 * 0.571
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_pr_interpolation(self):
        self.setup()
        auc_obj = metrics.AUC(num_thresholds=self.num_thresholds, curve="PR")
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # auc = (slope / Total Pos) * [dTP - intercept * log(Pb/Pa)]

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # P = tp + fp = [10, 4, 0]
        # dTP = [7-4, 4-0] = [3, 4]
        # dP = [10-4, 4-0] = [6, 4]
        # slope = dTP/dP = [0.5, 1]
        # intercept = (TPa+(slope*Pa) = [(4 - 0.5*4), (0 - 1*0)] = [2, 0]
        # (Pb/Pa) = (Pb/Pa) if Pb > 0 AND Pa > 0 else 1 = [10/4, 4/0] = [2.5, 1]
        # auc * TotalPos = [(0.5 * (3 + 2 * log(2.5))), (1 * (4 + 0))]
        #                = [2.416, 4]
        # auc = [2.416, 4]/(tp[1:]+fn[1:])
        expected_result = 2.416 / 7 + 4 / 7
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_prgain_majoring(self):
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            curve="PRGAIN",
            summation_method="majoring",
        )
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # scaling_facor (P/N) = 7/3
        # recall_gain = 1 - 7/3 [0/7, 3/4, 7/0] = [1, -3/4, -inf] -> [1, 0, 0]
        # precision_gain = 1 - 7/3 [3/7, 0/4, 0/0] = [0, 1, NaN] -> [0, 1, 1]
        # heights = [max(0, 1), max(1, 1)] = [1, 1]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 1 * 1 + 0 * 1
        self.assertAllClose(result, expected_result, 1e-3)

    def test_weighted_prgain_minoring(self):
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            curve="PRGAIN",
            summation_method="minoring",
        )
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # scaling_facor (P/N) = 7/3
        # recall_gain = 1 - 7/3 [0/7, 3/4, 7/0] = [1, -3/4, -inf] -> [1, 0, 0]
        # precision_gain = 1 - 7/3 [3/7, 0/4, 0/0] = [0, 1, NaN] -> [0, 1, 1]
        # heights = [min(0, 1), min(1, 1)] = [0, 1]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 1 * 0 + 0 * 1
        self.assertAllClose(result, expected_result, 1e-3)

    def test_weighted_prgain_interpolation(self):
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, curve="PRGAIN"
        )
        result = auc_obj(
            self.y_true, self.y_pred, sample_weight=self.sample_weight
        )

        # tp = [7, 4, 0], fp = [3, 0, 0], fn = [0, 3, 7], tn = [0, 3, 3]
        # scaling_facor (P/N) = 7/3
        # recall_gain = 1 - 7/3 [0/7, 3/4, 7/0] = [1, -3/4, -inf] -> [1, 0, 0]
        # precision_gain = 1 - 7/3 [3/7, 0/4, 0/0] = [0, 1, NaN] -> [0, 1, 1]
        # heights = [(0+1)/2, (1+1)/2] = [0.5, 1]
        # widths = [(1 - 0), (0 - 0)] = [1, 0]
        expected_result = 1 * 0.5 + 0 * 1
        self.assertAllClose(result, expected_result, 1e-3)

    def test_prgain_interpolation(self):
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, curve="PRGAIN"
        )

        y_true = np.array([0, 0, 0, 1, 0, 1, 0, 1, 1, 1])
        y_pred = np.array([0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.6, 0.6, 0.8, 0.9])
        result = auc_obj(y_true, y_pred)

        # tp = [5, 3, 0], fp = [5, 1, 0], fn = [0, 2, 5], tn = [0, 4, 4]
        # scaling_facor (P/N) = 5/5 = 1
        # recall_gain = 1 - [0/5, 2/3, 5/0] = [1, 1/3, -inf] -> [1, 1/3, 0]
        # precision_gain = 1 - [5/5, 1/3, 0/0] = [1, 1/3, NaN] -> [0, 2/3, 1]
        # heights = [(0+2/3)/2, (2/3+1)/2] = [0.333333, 0.833333]
        # widths = [(1 - 1/3), (1/3 - 0)] = [0.666666, 0.333333]
        expected_result = 0.666666 * 0.333333 + 0.333333 * 0.833333
        self.assertAllClose(result, expected_result, 1e-3)

    def test_invalid_num_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 1"
        ):
            metrics.AUC(num_thresholds=-1)

        with self.assertRaisesRegex(
            ValueError, "Argument `num_thresholds` must be an integer > 1."
        ):
            metrics.AUC(num_thresholds=1)

    def test_invalid_curve(self):
        with self.assertRaisesRegex(
            ValueError, 'Invalid AUC curve value: "Invalid".'
        ):
            metrics.AUC(curve="Invalid")

    def test_invalid_summation_method(self):
        with self.assertRaisesRegex(
            ValueError, 'Invalid AUC summation method value: "Invalid".'
        ):
            metrics.AUC(summation_method="Invalid")

    def test_extra_dims(self):
        try:
            from scipy import special

            self.setup()
            logits = special.expit(
                -np.array(
                    [
                        [[-10.0, 10.0, -10.0], [10.0, -10.0, 10.0]],
                        [[-12.0, 12.0, -12.0], [12.0, -12.0, 12.0]],
                    ],
                    dtype=np.float32,
                )
            )
            labels = np.array(
                [[[1, 0, 0], [1, 0, 0]], [[0, 1, 1], [0, 1, 1]]], dtype=np.int64
            )
            auc_obj = metrics.AUC()
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(labels, logits)
            self.assertEqual(self.evaluate(result), 0.5)
        except ImportError as e:
            tf_logging.warning(f"Cannot test special functions: {str(e)}")


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class MultiAUCTest(tf.test.TestCase, parameterized.TestCase):
    def setup(self):
        self.num_thresholds = 5
        self.y_pred = tf.constant(
            np.array([[0, 0.5, 0.3, 0.9], [0.1, 0.2, 0.3, 0.4]]).T,
            dtype=tf.float32,
        )

        epsilon = 1e-12
        self.y_pred_logits = -tf.math.log(1.0 / (self.y_pred + epsilon) - 1.0)

        self.y_true_good = tf.constant(np.array([[0, 0, 1, 1], [0, 0, 1, 1]]).T)
        self.y_true_bad = tf.constant(np.array([[0, 0, 1, 1], [1, 1, 0, 0]]).T)
        self.sample_weight = [1, 2, 3, 4]

        # threshold values are [0 - 1e-7, 0.25, 0.5, 0.75, 1 + 1e-7]
        # y_pred when threshold = 0 - 1e-7   : [[1, 1, 1, 1], [1, 1, 1, 1]]
        # y_pred when threshold = 0.25       : [[0, 1, 1, 1], [0, 0, 1, 1]]
        # y_pred when threshold = 0.5        : [[0, 0, 0, 1], [0, 0, 0, 0]]
        # y_pred when threshold = 0.75       : [[0, 0, 0, 1], [0, 0, 0, 0]]
        # y_pred when threshold = 1 + 1e-7   : [[0, 0, 0, 0], [0, 0, 0, 0]]

        # for y_true_good, over thresholds:
        # tp = [[2, 2, 1, 1, 0], [2, 2, 0, 0, 0]]
        # fp = [[2, 1, 0, 0 , 0], [2, 0, 0 ,0, 0]]
        # fn = [[0, 0, 1, 1, 2], [0, 0, 2, 2, 2]]
        # tn = [[0, 1, 2, 2, 2], [0, 2, 2, 2, 2]]

        # tpr = [[1, 1, 0.5, 0.5, 0], [1, 1, 0, 0, 0]]
        # fpr = [[1, 0.5, 0, 0, 0], [1, 0, 0, 0, 0]]

        # for y_true_bad:
        # tp = [[2, 2, 1, 1, 0], [2, 0, 0, 0, 0]]
        # fp = [[2, 1, 0, 0 , 0], [2, 2, 0 ,0, 0]]
        # fn = [[0, 0, 1, 1, 2], [0, 2, 2, 2, 2]]
        # tn = [[0, 1, 2, 2, 2], [0, 0, 2, 2, 2]]

        # tpr = [[1, 1, 0.5, 0.5, 0], [1, 0, 0, 0, 0]]
        # fpr = [[1, 0.5, 0, 0, 0], [1, 1, 0, 0, 0]]

        # for y_true_good with sample_weights:

        # tp = [[7, 7, 4, 4, 0], [7, 7, 0, 0, 0]]
        # fp = [[3, 2, 0, 0, 0], [3, 0, 0, 0, 0]]
        # fn = [[0, 0, 3, 3, 7], [0, 0, 7, 7, 7]]
        # tn = [[0, 1, 3, 3, 3], [0, 3, 3, 3, 3]]

        # tpr = [[1, 1,    0.57, 0.57, 0], [1, 1, 0, 0, 0]]
        # fpr = [[1, 0.67, 0,    0,    0], [1, 0, 0, 0, 0]]

    def test_value_is_idempotent(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(num_thresholds=5, multi_label=True)
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))

            # Run several updates.
            update_op = auc_obj.update_state(self.y_true_good, self.y_pred)
            for _ in range(10):
                self.evaluate(update_op)

            # Then verify idempotency.
            initial_auc = self.evaluate(auc_obj.result())
            for _ in range(10):
                self.assertAllClose(
                    initial_auc, self.evaluate(auc_obj.result()), 1e-3
                )

    def test_unweighted_all_correct(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(multi_label=True)
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(self.y_true_good, self.y_true_good)
            self.assertEqual(self.evaluate(result), 1)

    def test_unweighted_all_correct_flat(self):
        self.setup()
        auc_obj = metrics.AUC(multi_label=False)
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true_good, self.y_true_good)
        self.assertEqual(self.evaluate(result), 1)

    def test_unweighted(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds, multi_label=True
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(self.y_true_good, self.y_pred)

            # tpr = [[1, 1, 0.5, 0.5, 0], [1, 1, 0, 0, 0]]
            # fpr = [[1, 0.5, 0, 0, 0], [1, 0, 0, 0, 0]]
            expected_result = (0.875 + 1.0) / 2.0
            self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_unweighted_from_logits(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds,
                multi_label=True,
                from_logits=True,
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(self.y_true_good, self.y_pred_logits)

            # tpr = [[1, 1, 0.5, 0.5, 0], [1, 1, 0, 0, 0]]
            # fpr = [[1, 0.5, 0, 0, 0], [1, 0, 0, 0, 0]]
            expected_result = (0.875 + 1.0) / 2.0
            self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_sample_weight_flat(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, multi_label=False
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(
            self.y_true_good, self.y_pred, sample_weight=[1, 2, 3, 4]
        )

        # tpr = [1, 1, 0.2857, 0.2857, 0]
        # fpr = [1, 0.3333, 0, 0, 0]
        expected_result = 1.0 - (0.3333 * (1.0 - 0.2857) / 2.0)
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_full_sample_weight_flat(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, multi_label=False
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        sw = np.arange(4 * 2)
        sw = sw.reshape(4, 2)
        result = auc_obj(self.y_true_good, self.y_pred, sample_weight=sw)

        # tpr = [1, 1, 0.2727, 0.2727, 0]
        # fpr = [1, 0.3333, 0, 0, 0]
        expected_result = 1.0 - (0.3333 * (1.0 - 0.2727) / 2.0)
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_label_weights(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds,
                multi_label=True,
                label_weights=[0.75, 0.25],
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(self.y_true_good, self.y_pred)

            # tpr = [[1, 1, 0.5, 0.5, 0], [1, 1, 0, 0, 0]]
            # fpr = [[1, 0.5, 0, 0, 0], [1, 0, 0, 0, 0]]
            expected_result = (0.875 * 0.75 + 1.0 * 0.25) / (0.75 + 0.25)
            self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_label_weights_flat(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            multi_label=False,
            label_weights=[0.75, 0.25],
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true_good, self.y_pred)

        # tpr = [1, 1, 0.375, 0.375, 0]
        # fpr = [1, 0.375, 0, 0, 0]
        expected_result = 1.0 - ((1.0 - 0.375) * 0.375 / 2.0)
        self.assertAllClose(self.evaluate(result), expected_result, 1e-2)

    def test_unweighted_flat(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds, multi_label=False
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true_good, self.y_pred)

        # tp = [4, 4, 1, 1, 0]
        # fp = [4, 1, 0, 0, 0]
        # fn = [0, 0, 3, 3, 4]
        # tn = [0, 3, 4, 4, 4]

        # tpr = [1, 1, 0.25, 0.25, 0]
        # fpr = [1, 0.25, 0, 0, 0]
        expected_result = 1.0 - (3.0 / 32.0)
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_unweighted_flat_from_logits(self):
        self.setup()
        auc_obj = metrics.AUC(
            num_thresholds=self.num_thresholds,
            multi_label=False,
            from_logits=True,
        )
        self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
        result = auc_obj(self.y_true_good, self.y_pred_logits)

        # tp = [4, 4, 1, 1, 0]
        # fp = [4, 1, 0, 0, 0]
        # fn = [0, 0, 3, 3, 4]
        # tn = [0, 3, 4, 4, 4]

        # tpr = [1, 1, 0.25, 0.25, 0]
        # fpr = [1, 0.25, 0, 0, 0]
        expected_result = 1.0 - (3.0 / 32.0)
        self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_manual_thresholds(self):
        with self.test_session():
            self.setup()
            # Verify that when specified, thresholds are used instead of
            # num_thresholds.
            auc_obj = metrics.AUC(
                num_thresholds=2, thresholds=[0.5], multi_label=True
            )
            self.assertEqual(auc_obj.num_thresholds, 3)
            self.assertAllClose(auc_obj.thresholds, [0.0, 0.5, 1.0])
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(self.y_true_good, self.y_pred)

            # tp = [[2, 1, 0], [2, 0, 0]]
            # fp = [2, 0, 0], [2, 0, 0]]
            # fn = [[0, 1, 2], [0, 2, 2]]
            # tn = [[0, 2, 2], [0, 2, 2]]

            # tpr = [[1, 0.5, 0], [1, 0, 0]]
            # fpr = [[1, 0, 0], [1, 0, 0]]

            # auc by slice = [0.75, 0.5]
            expected_result = (0.75 + 0.5) / 2.0

            self.assertAllClose(self.evaluate(result), expected_result, 1e-3)

    def test_weighted_roc_interpolation(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds, multi_label=True
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            result = auc_obj(
                self.y_true_good, self.y_pred, sample_weight=self.sample_weight
            )

            # tpr = [[1, 1,    0.57, 0.57, 0], [1, 1, 0, 0, 0]]
            # fpr = [[1, 0.67, 0,    0,    0], [1, 0, 0, 0, 0]]
            expected_result = 1.0 - 0.5 * 0.43 * 0.67
            self.assertAllClose(self.evaluate(result), expected_result, 1e-1)

    def test_pr_interpolation_unweighted(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds, curve="PR", multi_label=True
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            good_result = auc_obj(self.y_true_good, self.y_pred)
            with self.subTest(name="good"):
                # PR AUCs are 0.917 and 1.0 respectively
                self.assertAllClose(
                    self.evaluate(good_result), (0.91667 + 1.0) / 2.0, 1e-1
                )
            bad_result = auc_obj(self.y_true_bad, self.y_pred)
            with self.subTest(name="bad"):
                # PR AUCs are 0.917 and 0.5 respectively
                self.assertAllClose(
                    self.evaluate(bad_result), (0.91667 + 0.5) / 2.0, 1e-1
                )

    def test_pr_interpolation(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds, curve="PR", multi_label=True
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            good_result = auc_obj(
                self.y_true_good, self.y_pred, sample_weight=self.sample_weight
            )
            # PR AUCs are 0.939 and 1.0 respectively
            self.assertAllClose(
                self.evaluate(good_result), (0.939 + 1.0) / 2.0, 1e-1
            )

    def test_keras_model_compiles(self):
        inputs = layers.Input(shape=(10,))
        output = layers.Dense(3, activation="sigmoid")(inputs)
        model = models.Model(inputs=inputs, outputs=output)
        model.compile(
            loss="binary_crossentropy", metrics=[metrics.AUC(multi_label=True)]
        )

    def test_reset_state(self):
        with self.test_session():
            self.setup()
            auc_obj = metrics.AUC(
                num_thresholds=self.num_thresholds, multi_label=True
            )
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            auc_obj(self.y_true_good, self.y_pred)
            auc_obj.reset_state()
            self.assertAllEqual(auc_obj.true_positives, np.zeros((5, 2)))


@test_combinations.generate(test_combinations.combine(mode=["eager"]))
class ThresholdsTest(tf.test.TestCase, parameterized.TestCase):
    @parameterized.parameters(
        [
            metrics.TruePositives(),
            metrics.TrueNegatives(),
            metrics.FalsePositives(),
            metrics.FalseNegatives(),
            metrics.Precision(),
            metrics.Recall(),
            metrics.SensitivityAtSpecificity(0.5),
            metrics.SpecificityAtSensitivity(0.5),
            metrics.PrecisionAtRecall(0.5),
            metrics.RecallAtPrecision(0.5),
            metrics.AUC(),
        ]
    )
    def test_with_default_thresholds(self, metric_obj):
        # By default, the thresholds will be evenly distributed if there are
        # more than 1. In case there is only 1 thresholds, then we expect
        # _thresholds_distributed_evenly to be false.
        expected = len(metric_obj.thresholds) > 1
        self.assertEqual(metric_obj._thresholds_distributed_evenly, expected)

    @parameterized.parameters(
        [
            metrics.TruePositives,
            metrics.TrueNegatives,
            metrics.FalsePositives,
            metrics.FalseNegatives,
            metrics.Precision,
            metrics.Recall,
        ]
    )
    def test_with_manual_thresholds(self, metric_cls):
        even_thresholds = [0.0, 0.25, 0.5, 0.75, 1.0]
        metric_obj = metric_cls(thresholds=even_thresholds)
        self.assertTrue(metric_obj._thresholds_distributed_evenly)

        uneven_thresholds = [0.0, 0.45, 1.0]
        metric_obj = metric_cls(thresholds=uneven_thresholds)
        self.assertFalse(metric_obj._thresholds_distributed_evenly)

    def test_manual_thresholds_auc(self):
        # The AUC metric handles manual thresholds input differently (it will
        # add 0.0 and 1.0 for user).
        even_thresholds = [0.25, 0.5, 0.75]
        auc = metrics.AUC(thresholds=even_thresholds)
        self.assertTrue(auc._thresholds_distributed_evenly)

        # Test for save model
        cloned = metrics.AUC.from_config(auc.get_config())
        self.assertTrue(cloned._thresholds_distributed_evenly)

        uneven_thresholds = [
            0.45,
        ]
        auc = metrics.AUC(thresholds=uneven_thresholds)
        self.assertFalse(auc._thresholds_distributed_evenly)

        cloned = metrics.AUC.from_config(auc.get_config())
        self.assertFalse(cloned._thresholds_distributed_evenly)

    @parameterized.parameters(
        [
            metrics.TruePositives,
            metrics.TrueNegatives,
            metrics.FalsePositives,
            metrics.FalseNegatives,
            metrics.Precision,
            metrics.Recall,
            metrics.AUC,
        ]
    )
    def test_even_thresholds_correctness(self, metric_cls):
        with tf.compat.forward_compatibility_horizon(2021, 6, 9):
            # make sure the old approach and new approach produce same result
            # for evenly distributed thresholds
            y_true = np.random.randint(2, size=(10,))
            y_pred = np.random.rand(10)

            even_thresholds = [0.0, 0.25, 0.5, 0.75, 1.0]
            if metric_cls == metrics.AUC:
                even_thresholds = even_thresholds[1:-1]
            metric_obj = metric_cls(thresholds=even_thresholds)
            metric_obj.update_state(y_true, y_pred)
            result1 = metric_obj.result()

            metric_obj2 = metric_cls(thresholds=even_thresholds)
            # Force to use the old approach
            metric_obj2._thresholds_distributed_evenly = False
            metric_obj2.update_state(y_true, y_pred)
            result2 = metric_obj2.result()

            self.assertAllClose(result1, result2)
            # Check all the variables are the same, eg tp, tn, fp, fn
            for v1, v2 in zip(metric_obj.variables, metric_obj2.variables):
                self.assertAllClose(v1, v2)

    @parameterized.parameters(
        [
            metrics.SensitivityAtSpecificity,
            metrics.SpecificityAtSensitivity,
            metrics.PrecisionAtRecall,
            metrics.RecallAtPrecision,
        ]
    )
    def test_even_thresholds_correctness_2(self, metric_cls):
        with tf.compat.forward_compatibility_horizon(2021, 6, 9):
            y_true = np.random.randint(2, size=(10,))
            y_pred = np.random.rand(10)

            metric_obj = metric_cls(0.5)
            metric_obj.update_state(y_true, y_pred)
            result1 = metric_obj.result()

            metric_obj2 = metric_cls(0.5)
            # Force to use the old approach
            metric_obj2._thresholds_distributed_evenly = False
            metric_obj2.update_state(y_true, y_pred)
            result2 = metric_obj2.result()

            self.assertAllClose(result1, result2)
            # Check all the variables are the same, eg tp, tn, fp, fn
            for v1, v2 in zip(metric_obj.variables, metric_obj2.variables):
                self.assertAllClose(v1, v2)


class BinaryTruePositives(metrics.Metric):
    def __init__(self, name="binary_true_positives", **kwargs):
        super().__init__(name=name, **kwargs)
        self.true_positives = self.add_weight(name="tp", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.bool)
        y_pred = tf.cast(y_pred, tf.bool)

        values = tf.logical_and(tf.equal(y_true, True), tf.equal(y_pred, True))
        values = tf.cast(values, self.dtype)
        if sample_weight is not None:
            sample_weight = tf.cast(sample_weight, dtype=self.dtype)
            sample_weight = tf.__internal__.ops.broadcast_weights(
                sample_weight, values
            )
            values = tf.multiply(values, sample_weight)
        self.true_positives.assign_add(tf.reduce_sum(values))

    def result(self):
        return self.true_positives


class BinaryTruePositivesViaControlFlow(metrics.Metric):
    def __init__(self, name="binary_true_positives", **kwargs):
        super().__init__(name=name, **kwargs)
        self.true_positives = self.add_weight(name="tp", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.bool)
        y_pred = tf.cast(y_pred, tf.bool)

        for i in range(len(y_true)):
            for j in range(len(y_true[i])):
                if y_true[i][j] and y_pred[i][j]:
                    if sample_weight is None:
                        self.true_positives.assign_add(1)
                    else:
                        self.true_positives.assign_add(sample_weight[i][0])

    def result(self):
        if tf.constant(True):
            return self.true_positives
        return 0.0


def _get_model(compile_metrics):
    model_layers = [
        layers.Dense(3, activation="relu", kernel_initializer="ones"),
        layers.Dense(1, activation="sigmoid", kernel_initializer="ones"),
    ]

    model = test_utils.get_model_from_layers(model_layers, input_shape=(4,))
    model.compile(
        loss="mae",
        metrics=compile_metrics,
        optimizer="rmsprop",
        run_eagerly=test_utils.should_run_eagerly(),
    )
    return model


@test_combinations.run_with_all_model_types
@test_combinations.run_all_keras_modes
class ResetStatesTest(test_combinations.TestCase):
    def test_reset_state_false_positives(self):
        fp_obj = metrics.FalsePositives()
        model = _get_model([fp_obj])
        x = np.ones((100, 4))
        y = np.zeros((100, 1))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(fp_obj.accumulator), 100.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(fp_obj.accumulator), 100.0)

    def test_reset_state_false_negatives(self):
        fn_obj = metrics.FalseNegatives()
        model = _get_model([fn_obj])
        x = np.zeros((100, 4))
        y = np.ones((100, 1))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(fn_obj.accumulator), 100.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(fn_obj.accumulator), 100.0)

    def test_reset_state_true_negatives(self):
        tn_obj = metrics.TrueNegatives()
        model = _get_model([tn_obj])
        x = np.zeros((100, 4))
        y = np.zeros((100, 1))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(tn_obj.accumulator), 100.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(tn_obj.accumulator), 100.0)

    def test_reset_state_true_positives(self):
        tp_obj = metrics.TruePositives()
        model = _get_model([tp_obj])
        x = np.ones((100, 4))
        y = np.ones((100, 1))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(tp_obj.accumulator), 100.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(tp_obj.accumulator), 100.0)

    def test_reset_state_precision(self):
        p_obj = metrics.Precision()
        model = _get_model([p_obj])
        x = np.concatenate((np.ones((50, 4)), np.ones((50, 4))))
        y = np.concatenate((np.ones((50, 1)), np.zeros((50, 1))))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(p_obj.true_positives), 50.0)
        self.assertEqual(self.evaluate(p_obj.false_positives), 50.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(p_obj.true_positives), 50.0)
        self.assertEqual(self.evaluate(p_obj.false_positives), 50.0)

    def test_precision_update_state_with_logits(self):
        p_obj = metrics.Precision()
        # Update state with logits (not in range (0, 1)) should not an raise
        # error.
        p_obj.update_state([-0.5, 0.5], [-2.0, 2.0])

    def test_reset_state_recall(self):
        r_obj = metrics.Recall()
        model = _get_model([r_obj])
        x = np.concatenate((np.ones((50, 4)), np.zeros((50, 4))))
        y = np.concatenate((np.ones((50, 1)), np.ones((50, 1))))
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(r_obj.true_positives), 50.0)
        self.assertEqual(self.evaluate(r_obj.false_negatives), 50.0)
        model.evaluate(x, y)
        self.assertEqual(self.evaluate(r_obj.true_positives), 50.0)
        self.assertEqual(self.evaluate(r_obj.false_negatives), 50.0)

    def test_reset_state_sensitivity_at_specificity(self):
        s_obj = metrics.SensitivityAtSpecificity(0.5, num_thresholds=1)
        model = _get_model([s_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(s_obj.true_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_negatives), 25.0)
            self.assertEqual(self.evaluate(s_obj.true_negatives), 25.0)

    def test_reset_state_specificity_at_sensitivity(self):
        s_obj = metrics.SpecificityAtSensitivity(0.5, num_thresholds=1)
        model = _get_model([s_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(s_obj.true_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_negatives), 25.0)
            self.assertEqual(self.evaluate(s_obj.true_negatives), 25.0)

    def test_reset_state_precision_at_recall(self):
        s_obj = metrics.PrecisionAtRecall(recall=0.5, num_thresholds=1)
        model = _get_model([s_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(s_obj.true_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_negatives), 25.0)
            self.assertEqual(self.evaluate(s_obj.true_negatives), 25.0)

    def test_reset_state_recall_at_precision(self):
        s_obj = metrics.RecallAtPrecision(precision=0.5, num_thresholds=1)
        model = _get_model([s_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(s_obj.true_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_positives), 25.0)
            self.assertEqual(self.evaluate(s_obj.false_negatives), 25.0)
            self.assertEqual(self.evaluate(s_obj.true_negatives), 25.0)

    def test_reset_state_auc(self):
        auc_obj = metrics.AUC(num_thresholds=3)
        model = _get_model([auc_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(auc_obj.true_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_negatives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.true_negatives[1]), 25.0)

    def test_reset_state_auc_from_logits(self):
        auc_obj = metrics.AUC(num_thresholds=3, from_logits=True)

        model_layers = [
            layers.Dense(1, kernel_initializer="ones", use_bias=False)
        ]
        model = test_utils.get_model_from_layers(model_layers, input_shape=(4,))
        model.compile(
            loss="mae",
            metrics=[auc_obj],
            optimizer="rmsprop",
            run_eagerly=test_utils.should_run_eagerly(),
        )

        x = np.concatenate(
            (
                np.ones((25, 4)),
                -np.ones((25, 4)),
                -np.ones((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(auc_obj.true_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_negatives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.true_negatives[1]), 25.0)

    def test_reset_state_auc_manual_thresholds(self):
        auc_obj = metrics.AUC(thresholds=[0.5])
        model = _get_model([auc_obj])
        x = np.concatenate(
            (
                np.ones((25, 4)),
                np.zeros((25, 4)),
                np.zeros((25, 4)),
                np.ones((25, 4)),
            )
        )
        y = np.concatenate(
            (
                np.ones((25, 1)),
                np.zeros((25, 1)),
                np.ones((25, 1)),
                np.zeros((25, 1)),
            )
        )

        for _ in range(2):
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(auc_obj.true_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_positives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.false_negatives[1]), 25.0)
            self.assertEqual(self.evaluate(auc_obj.true_negatives[1]), 25.0)

    def test_reset_state_mean_iou(self):
        m_obj = metrics.MeanIoU(num_classes=2)
        model = _get_model([m_obj])
        x = np.asarray(
            [[0, 0, 0, 0], [1, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1]],
            dtype=np.float32,
        )
        y = np.asarray([[0], [1], [1], [1]], dtype=np.float32)
        model.evaluate(x, y)
        self.assertArrayNear(self.evaluate(m_obj.total_cm)[0], [1, 0], 1e-1)
        self.assertArrayNear(self.evaluate(m_obj.total_cm)[1], [3, 0], 1e-1)
        model.evaluate(x, y)
        self.assertArrayNear(self.evaluate(m_obj.total_cm)[0], [1, 0], 1e-1)
        self.assertArrayNear(self.evaluate(m_obj.total_cm)[1], [3, 0], 1e-1)

    def test_reset_state_recall_float64(self):
        # Test case for GitHub issue 36790.
        try:
            backend.set_floatx("float64")
            r_obj = metrics.Recall()
            model = _get_model([r_obj])
            x = np.concatenate((np.ones((50, 4)), np.zeros((50, 4))))
            y = np.concatenate((np.ones((50, 1)), np.ones((50, 1))))
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(r_obj.true_positives), 50.0)
            self.assertEqual(self.evaluate(r_obj.false_negatives), 50.0)
            model.evaluate(x, y)
            self.assertEqual(self.evaluate(r_obj.true_positives), 50.0)
            self.assertEqual(self.evaluate(r_obj.false_negatives), 50.0)
        finally:
            backend.set_floatx("float32")

    def test_function_wrapped_reset_state(self):
        m = metrics.Mean(name="my_mean")

        # check reset_state in function.
        @tf.function
        def reset_in_fn():
            m.reset_state()
            m.update_state(100)

        for _ in range(5):
            reset_in_fn()
            if not tf.executing_eagerly():
                self.evaluate(
                    tf.compat.v1.get_default_graph().get_operations()[-1]
                )
        self.assertEqual(self.evaluate(m.count), 1)


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class MergeStateTest(test_combinations.TestCase):
    def test_merge_state_incompatible_metrics(self):
        with self.assertRaisesRegex(
            ValueError, "Metric .* is not compatible with .*"
        ):
            obj1 = metrics.FalsePositives()
            self.evaluate(tf.compat.v1.variables_initializer(obj1.variables))
            obj2 = metrics.Accuracy()
            self.evaluate(tf.compat.v1.variables_initializer(obj2.variables))
            self.evaluate(obj1.merge_state([obj2]))

    def test_merge_state_accuracy(self):
        a_objs = []
        for y_true, y_pred in zip(
            [[[1], [2]], [[3], [4]]], [[[0], [2]], [[3], [4]]]
        ):
            a_obj = metrics.Accuracy()
            a_objs.append(a_obj)
            self.evaluate(tf.compat.v1.variables_initializer(a_obj.variables))
            self.evaluate(a_obj.update_state(y_true, y_pred))
        self.evaluate(a_objs[0].merge_state(a_objs[1:]))
        self.assertEqual(self.evaluate(a_objs[0].total), 3.0)
        self.assertEqual(self.evaluate(a_objs[0].count), 4.0)
        self.assertEqual(self.evaluate(a_objs[0].result()), 0.75)

    def test_merge_state_false_positives(self):
        fp_objs = []
        for _ in range(4):
            fp_obj = metrics.FalsePositives()
            fp_objs.append(fp_obj)
            self.evaluate(tf.compat.v1.variables_initializer(fp_obj.variables))
            y_true = np.zeros((25, 1))
            y_pred = np.ones((25, 1))
            self.evaluate(fp_obj.update_state(y_true, y_pred))
        self.evaluate(fp_objs[0].merge_state(fp_objs[1:]))
        self.assertEqual(self.evaluate(fp_objs[0].accumulator), 100.0)

    def test_merge_state_false_negatives(self):
        fn_objs = []
        for _ in range(4):
            fn_obj = metrics.FalseNegatives()
            fn_objs.append(fn_obj)
            self.evaluate(tf.compat.v1.variables_initializer(fn_obj.variables))
            y_true = np.ones((25, 1))
            y_pred = np.zeros((25, 1))
            self.evaluate(fn_obj.update_state(y_true, y_pred))
        self.evaluate(fn_objs[0].merge_state(fn_objs[1:]))
        self.assertEqual(self.evaluate(fn_objs[0].accumulator), 100.0)

    def test_merge_state_true_negatives(self):
        tn_objs = []
        for _ in range(4):
            tn_obj = metrics.TrueNegatives()
            tn_objs.append(tn_obj)
            self.evaluate(tf.compat.v1.variables_initializer(tn_obj.variables))
            y_true = np.zeros((25, 1))
            y_pred = np.zeros((25, 1))
            self.evaluate(tn_obj.update_state(y_true, y_pred))
        self.evaluate(tn_objs[0].merge_state(tn_objs[1:]))
        self.assertEqual(self.evaluate(tn_objs[0].accumulator), 100.0)

    def test_merge_state_true_positives(self):
        tp_objs = []
        for _ in range(4):
            tp_obj = metrics.TruePositives()
            tp_objs.append(tp_obj)
            self.evaluate(tf.compat.v1.variables_initializer(tp_obj.variables))
            y_true = np.ones((25, 1))
            y_pred = np.ones((25, 1))
            self.evaluate(tp_obj.update_state(y_true, y_pred))
        self.evaluate(tp_objs[0].merge_state(tp_objs[1:]))
        self.assertEqual(self.evaluate(tp_objs[0].accumulator), 100.0)

    def test_merge_state_precision(self):
        p_objs = []
        for _ in range(5):
            p_obj = metrics.Precision()
            p_objs.append(p_obj)
            self.evaluate(tf.compat.v1.variables_initializer(p_obj.variables))
            y_true = np.concatenate((np.ones((10, 1)), np.zeros((10, 1))))
            y_pred = np.concatenate((np.ones((10, 1)), np.ones((10, 1))))
            self.evaluate(p_obj.update_state(y_true, y_pred))
        self.evaluate(p_objs[0].merge_state(p_objs[1:]))
        self.assertEqual(self.evaluate(p_objs[0].true_positives), 50.0)
        self.assertEqual(self.evaluate(p_objs[0].false_positives), 50.0)

    def test_merge_state_recall(self):
        r_objs = []
        for _ in range(5):
            r_obj = metrics.Recall()
            r_objs.append(r_obj)
            self.evaluate(tf.compat.v1.variables_initializer(r_obj.variables))
            y_true = np.concatenate((np.ones((10, 1)), np.ones((10, 1))))
            y_pred = np.concatenate((np.ones((10, 1)), np.zeros((10, 1))))
            self.evaluate(r_obj.update_state(y_true, y_pred))
        self.evaluate(r_objs[0].merge_state(r_objs[1:]))
        self.assertEqual(self.evaluate(r_objs[0].true_positives), 50.0)
        self.assertEqual(self.evaluate(r_objs[0].false_negatives), 50.0)

    def test_merge_state_sensitivity_at_specificity(self):
        sas_objs = []
        for _ in range(5):
            sas_obj = metrics.SensitivityAtSpecificity(0.5, num_thresholds=1)
            sas_objs.append(sas_obj)
            self.evaluate(tf.compat.v1.variables_initializer(sas_obj.variables))
            y_true = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                )
            )
            y_pred = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                )
            )
            self.evaluate(sas_obj.update_state(y_true, y_pred))
        self.evaluate(sas_objs[0].merge_state(sas_objs[1:]))
        self.assertEqual(self.evaluate(sas_objs[0].true_positives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].false_positives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].false_negatives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].true_negatives), 25.0)

    def test_merge_state_specificity_at_sensitivity(self):
        sas_objs = []
        for _ in range(5):
            sas_obj = metrics.SpecificityAtSensitivity(0.5, num_thresholds=1)
            sas_objs.append(sas_obj)
            self.evaluate(tf.compat.v1.variables_initializer(sas_obj.variables))
            y_true = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                )
            )
            y_pred = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                )
            )
            self.evaluate(sas_obj.update_state(y_true, y_pred))
        self.evaluate(sas_objs[0].merge_state(sas_objs[1:]))
        self.assertEqual(self.evaluate(sas_objs[0].true_positives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].false_positives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].false_negatives), 25.0)
        self.assertEqual(self.evaluate(sas_objs[0].true_negatives), 25.0)

    def test_merge_state_precision_at_recall(self):
        par_objs = []
        for _ in range(5):
            par_obj = metrics.PrecisionAtRecall(recall=0.5, num_thresholds=1)
            par_objs.append(par_obj)
            self.evaluate(tf.compat.v1.variables_initializer(par_obj.variables))
            y_true = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                )
            )
            y_pred = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                )
            )
            self.evaluate(par_obj.update_state(y_true, y_pred))
        self.evaluate(par_objs[0].merge_state(par_objs[1:]))
        self.assertEqual(self.evaluate(par_objs[0].true_positives), 25.0)
        self.assertEqual(self.evaluate(par_objs[0].false_positives), 25.0)
        self.assertEqual(self.evaluate(par_objs[0].false_negatives), 25.0)
        self.assertEqual(self.evaluate(par_objs[0].true_negatives), 25.0)

    def test_merge_state_recall_at_precision(self):
        rap_objs = []
        for _ in range(5):
            rap_obj = metrics.PrecisionAtRecall(recall=0.5, num_thresholds=1)
            rap_objs.append(rap_obj)
            self.evaluate(tf.compat.v1.variables_initializer(rap_obj.variables))
            y_true = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                )
            )
            y_pred = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                )
            )
            self.evaluate(rap_obj.update_state(y_true, y_pred))
        self.evaluate(rap_objs[0].merge_state(rap_objs[1:]))
        self.assertEqual(self.evaluate(rap_objs[0].true_positives), 25.0)
        self.assertEqual(self.evaluate(rap_objs[0].false_positives), 25.0)
        self.assertEqual(self.evaluate(rap_objs[0].false_negatives), 25.0)
        self.assertEqual(self.evaluate(rap_objs[0].true_negatives), 25.0)

    def test_merge_state_auc(self):
        auc_objs = []
        for _ in range(5):
            auc_obj = metrics.AUC(num_thresholds=3)
            auc_objs.append(auc_obj)
            self.evaluate(tf.compat.v1.variables_initializer(auc_obj.variables))
            y_true = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                )
            )
            y_pred = np.concatenate(
                (
                    np.ones((5, 1)),
                    np.zeros((5, 1)),
                    np.zeros((5, 1)),
                    np.ones((5, 1)),
                )
            )
            self.evaluate(auc_obj.update_state(y_true, y_pred))
        self.evaluate(auc_objs[0].merge_state(auc_objs[1:]))
        self.assertEqual(self.evaluate(auc_objs[0].true_positives[1]), 25.0)
        self.assertEqual(self.evaluate(auc_objs[0].false_positives[1]), 25.0)
        self.assertEqual(self.evaluate(auc_objs[0].false_negatives[1]), 25.0)
        self.assertEqual(self.evaluate(auc_objs[0].true_negatives[1]), 25.0)

    def test_merge_state_mean_iou(self):
        m_objs = []
        for y_true, y_pred in zip(
            [[0], [1], [1], [1]], [[0.5], [1.0], [1.0], [1.0]]
        ):
            m_obj = metrics.MeanIoU(num_classes=2)
            m_objs.append(m_obj)
            self.evaluate(tf.compat.v1.variables_initializer(m_obj.variables))
            self.evaluate(m_obj.update_state(y_true, y_pred))
        self.evaluate(m_objs[0].merge_state(m_objs[1:]))
        self.assertArrayNear(self.evaluate(m_objs[0].total_cm)[0], [1, 0], 1e-1)
        self.assertArrayNear(self.evaluate(m_objs[0].total_cm)[1], [0, 3], 1e-1)


if __name__ == "__main__":
    tf.test.main()
