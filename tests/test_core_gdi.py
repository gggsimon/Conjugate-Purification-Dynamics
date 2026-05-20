"""
GDI核心指标计算模块 - 单元测试
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from code.core_gdi_calc import (
    detect_language,
    calc_diversity_b,
    calc_specificity_a,
    calc_gdi,
    batch_calc,
    np_mean,
    np_std
)


class TestDetectLanguage(unittest.TestCase):

    def test_chinese_text(self):
        result = detect_language("这是一个中文测试句子")
        self.assertEqual(result, 'chinese')

    def test_english_text(self):
        result = detect_language("This is an English test sentence")
        self.assertEqual(result, 'english')

    def test_empty_text(self):
        result = detect_language("")
        self.assertEqual(result, 'unknown')

    def test_mixed_text_chinese_dominant(self):
        result = detect_language("这是中文 mixed with some English words")
        # 中英文混合文本，检测结果取决于实现策略
        self.assertIn(result, ['chinese', 'english'])
      
    def test_mixed_text_english_dominant(self):
        result = detect_language("Mostly English text with a few 中文字")
        self.assertEqual(result, 'english')


class TestDiversityB(unittest.TestCase):

    def test_chinese_diversity(self):
        text = "人工智能正在深刻改变我们的生活方式和生产方式"
        B = calc_diversity_b(text, lang='chinese')
        self.assertGreater(B, 0.0)
        self.assertLessEqual(B, 1.0)

    def test_english_diversity(self):
        text = "the quick brown fox jumps over the lazy dog"
        B = calc_diversity_b(text, lang='english')
        self.assertGreater(B, 0.0)
        self.assertLessEqual(B, 1.0)

    def test_short_text_returns_zero(self):
        B = calc_diversity_b("ab", lang='english')
        self.assertEqual(B, 0.0)

    def test_empty_text_returns_zero(self):
        B = calc_diversity_b("", lang='english')
        self.assertEqual(B, 0.0)

    def test_repeated_text_low_diversity(self):
        text = "the the the the the the the the"
        B = calc_diversity_b(text, lang='english')
        self.assertLess(B, 0.5)

    def test_diverse_text_high_diversity(self):
        words = "apple banana cherry date elderberry fig grape hazelnut"
        B = calc_diversity_b(words, lang='english')
        self.assertGreater(B, 0.5)

    def test_auto_detect_chinese(self):
        text = "今天天气很好适合出去散步"
        B = calc_diversity_b(text, lang='auto')
        self.assertGreater(B, 0.0)

    def test_auto_detect_english(self):
        text = "the weather is nice today for a walk"
        B = calc_diversity_b(text, lang='auto')
        self.assertGreater(B, 0.0)


class TestSpecificityA(unittest.TestCase):

    def test_chinese_specificity(self):
        text = "人工智能正在深刻改变我们的生活方式和生产方式"
        A = calc_specificity_a(text, lang='chinese')
        self.assertGreater(A, 0.0)
        self.assertLessEqual(A, 1.0)

    def test_english_specificity(self):
        text = "the quick brown fox jumps over the lazy dog"
        A = calc_specificity_a(text, lang='english')
        self.assertGreater(A, 0.0)
        self.assertLessEqual(A, 1.0)

    def test_empty_text_returns_zero(self):
        A = calc_specificity_a("", lang='english')
        self.assertEqual(A, 0.0)

    def test_uniform_text_high_specificity(self):
        text = "alpha beta gamma delta epsilon zeta eta theta"
        A = calc_specificity_a(text, lang='english')
        self.assertGreater(A, 0.5)

    def test_repeated_text_low_specificity(self):
        text = "the the the the the the the the the the"
        A = calc_specificity_a(text, lang='english')
        self.assertLess(A, 0.5)


class TestGDI(unittest.TestCase):

    def test_gdi_returns_three_values(self):
        text = "人工智能正在深刻改变我们的生活方式"
        result = calc_gdi(text, lang='chinese')
        self.assertEqual(len(result), 3)
        B, A, GDI = result
        self.assertGreater(B, 0.0)
        self.assertGreater(A, 0.0)
        self.assertGreater(GDI, 0.0)

    def test_gdi_formula(self):
        text = "the quick brown fox jumps over the lazy dog"
        B, A, GDI = calc_gdi(text, lang='english')
        expected_gdi = round(A**2 + B**2, 4)
        self.assertAlmostEqual(GDI, expected_gdi, places=4)

    def test_gdi_empty_text(self):
        B, A, GDI = calc_gdi("", lang='english')
        self.assertEqual(B, 0.0)
        self.assertEqual(A, 0.0)
        self.assertEqual(GDI, 0.0)

    def test_gdi_known_values(self):
        text = "人工智能正在深刻改变我们的生活方式和生产方式"
        B, A, GDI = calc_gdi(text, lang='chinese')
        self.assertGreater(GDI, 0.0)
        self.assertLessEqual(GDI, 2.0)


class TestBatchCalc(unittest.TestCase):

    def test_batch_single_text(self):
        results = batch_calc(["hello world"], lang='english')
        self.assertEqual(len(results), 6)

    def test_batch_multiple_texts(self):
        texts = [
            "the quick brown fox",
            "hello world foo bar",
            "python is great"
        ]
        results = batch_calc(texts, lang='english')
        self.assertEqual(len(results), 6)
        self.assertGreater(results[0], 0.0)

    def test_batch_empty_list(self):
        results = batch_calc([], lang='english')
        self.assertEqual(results, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    def test_batch_with_empty_strings(self):
        texts = ["hello world", "", "  ", "foo bar"]
        results = batch_calc(texts, lang='english')
        self.assertEqual(len(results), 6)


class TestHelperFunctions(unittest.TestCase):

    def test_np_mean(self):
        self.assertEqual(np_mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(np_mean([10]), 10.0)

    def test_np_std(self):
        std = np_std([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertAlmostEqual(std, 2.0, places=1)

    def test_np_std_zero_variance(self):
        std = np_std([5, 5, 5, 5])
        self.assertAlmostEqual(std, 0.0, places=5)


if __name__ == '__main__':
    unittest.main()
