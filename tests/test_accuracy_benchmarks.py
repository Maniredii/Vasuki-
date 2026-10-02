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
    def test_even_odd_function(self):
        resp, _ = test_vasuki.query_model("write a python function to check even or odd", max_tokens=150)
        self.assertTrue("def " in resp and "% 2" in resp)
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_palindrome_function(self):
        resp, _ = test_vasuki.query_model("write a function to check if a string is palindrome", max_tokens=150)
        self.assertTrue("def " in resp and ("[::-1]" in resp or "reversed" in resp))
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_factorial_function(self):
        resp, _ = test_vasuki.query_model("write a function to calculate factorial of a number", max_tokens=150)
        self.assertTrue("def " in resp and ("factorial" in resp or "fact" in resp))
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_binary_search_implementation(self):
        resp, _ = test_vasuki.query_model("write binary search in python", max_tokens=150)
        self.assertTrue("def " in resp and ("mid" in resp or "// 2" in resp))
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_stack_class(self):
        resp, _ = test_vasuki.query_model("write a Python class Stack with push and pop", max_tokens=150)
        self.assertTrue("class " in resp and "push" in resp and "pop" in resp)
        self.assertFalse(test_vasuki.is_degenerate_output(resp))
    def test_prime_number_check(self):
        resp, _ = test_vasuki.query_model("write a function to check if a number is prime", max_tokens=150)
        self.assertTrue("def " in resp and ("% i" in resp or "is_prime" in resp))
        self.assertFalse(test_vasuki.is_degenerate_output(resp))

if __name__ == '__main__': unittest.main()
