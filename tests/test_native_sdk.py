"""
Unit test verifying native vasuki Python SDK package imports and functions.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import vasuki

class TestVasukiSDK(unittest.TestCase):
    def test_version(self):
        self.assertTrue(vasuki.__version__.startswith("1."))

    def test_author(self):
        self.assertEqual(vasuki.__author__, "Manideep Reddy Eevuri")

    def test_callable_exports(self):
        self.assertTrue(callable(vasuki.generate))
        self.assertTrue(callable(vasuki.ask))
        self.assertTrue(callable(vasuki.chat))

if __name__ == "__main__":
    unittest.main()
