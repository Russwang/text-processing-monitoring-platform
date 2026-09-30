import unittest
from vowelcount import count_vowels

class TestVowelCount(unittest.TestCase):
    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("world"), 1)
        self.assertEqual(count_vowels(""), 0)
        self.assertEqual(count_vowels("AEIOU"), 5)
        self.assertEqual(count_vowels("12345"), 0)

if __name__ == "__main__":
    unittest.main()
