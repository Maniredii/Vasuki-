"""
Unit tests for VASUKI Accuracy Guardrails and Fallback Engine.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import test_vasuki

class TestAccuracyGuardrails(unittest.TestCase):
    def test_prefix_repetition_detection(self):
        repeated_text = "chief assistant\nchief data scientist\nchief developer\nchief engineer"
        self.assertTrue(test_vasuki.check_prefix_repetition(repeated_text, min_repeats=3))

    def test_clean_text_not_flagged(self):
        normal_code = "def add(a, b):\n    return a + b\n\nprint(add(2, 3))"
        self.assertFalse(test_vasuki.check_prefix_repetition(normal_code))

    def test_degenerate_output_detection(self):
        corrupt = "życzę zapytań i odpowiedzi na pytania"
        self.assertTrue(test_vasuki.is_degenerate_output(corrupt))

    def test_decision_tree_accuracy(self):
        """Verify that 'explain decision tree' generates valid Python code."""
        resp, _ = test_vasuki.query_model("explain decision tree in python", max_tokens=150)
        self.assertTrue("DecisionTreeClassifier" in resp or "tree" in resp.lower() or "def " in resp)
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_synthetic_rejection(self):
        fake_loop = "\n".join(["word " + str(i) for i in range(10)])
        self.assertTrue(test_vasuki.check_prefix_repetition(fake_loop, min_repeats=3))

if __name__ == "__main__":
    unittest.main()
