"""
Unit tests verifying VASUKI Knowledge Engine and REPL context isolation.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from vasuki.knowledge import resolve_knowledge, normalize_concept_query
import test_vasuki

class TestKnowledgeEngine(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_concept_query("what is python"), "python")
        self.assertEqual(normalize_concept_query("what is a tuple in python?"), "tuple")
        self.assertEqual(normalize_concept_query("explain list in python"), "list")

    def test_python_concept_resolution(self):
        ans = resolve_knowledge("what is python")
        self.assertIsNotNone(ans)
        self.assertTrue("interpreted" in ans.lower() or "high-level" in ans.lower())

    def test_tuple_concept_resolution(self):
        ans = resolve_knowledge("what is tuple")
        self.assertIsNotNone(ans)
        self.assertTrue("immutable" in ans.lower() and "ordered" in ans.lower())

    def test_list_vs_tuple_resolution(self):
        ans = resolve_knowledge("difference between list and tuple")
        self.assertIsNotNone(ans)
        self.assertTrue("mutable" in ans.lower() and "immutable" in ans.lower())

    def test_query_model_dispatches_knowledge(self):
        resp, dur = test_vasuki.query_model("what is tuple")
        self.assertTrue("immutable" in resp.lower())
        self.assertFalse("Loading model..." in resp)
        self.assertFalse("▄▄" in resp)

if __name__ == "__main__":
    unittest.main()
