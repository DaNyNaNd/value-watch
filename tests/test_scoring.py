import unittest

from value_watch.scoring import score


def financials():
    years = range(2019, 2024)
    return {"revenue": dict(zip(years, (100, 110, 120, 130, 140))),
            "eps": dict(zip(years, (1, 1.1, 1.2, 1.3, 1.4))),
            "fcf": dict(zip(years, (30, 35, 40, 45, 50))),
            "net_income": {2023: 20}, "equity": {2022: 100, 2023: 120}, "debt": {2023: 100}}


class ScoreTests(unittest.TestCase):
    def test_review_when_scorecard_conditions_pass(self):
        result = score({"peRatio": 20, "marketCap": 1000}, financials())
        self.assertEqual((result.label, result.value_points, result.quality_points), ("Review", 2, 5))

    def test_missing_required_data_is_not_zero(self):
        result = score({}, {})
        self.assertEqual(result.label, "Insufficient data")
        self.assertTrue(all(check.passed is None for check in result.checks))
