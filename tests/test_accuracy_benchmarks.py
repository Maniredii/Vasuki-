"""
VASUKI Accuracy & Correctness Verification Benchmark
Tests core Python algorithmic and programming requests for accuracy.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import test_vasuki

class TestCoreAccuracy(unittest.TestCase):
    def test_even_odd_program(self):
        resp, _ = test_vasuki.query_model("write even odd program", max_tokens=150)
        self.assertTrue("% 2" in resp or "even" in resp.lower())
        self.assertFalse(test_vasuki.is_degenerate_output(resp))

if __name__ == '__main__': unittest.main()
