"""Tests for the autoresearch framework."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest


class TestEvaluate:
    """Test the evaluation function with known inputs."""

    def test_perfect_prediction(self):
        from autoresearch.prepare import evaluate
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        metrics = evaluate(y_true, y_pred)
        assert abs(metrics["val_r2"] - 1.0) < 1e-6
        assert abs(metrics["val_mae"] - 0.0) < 1e-6
        assert abs(metrics["val_rmse"] - 0.0) < 1e-6

    def test_mean_prediction_r2_zero(self):
        from autoresearch.prepare import evaluate
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.full(5, 3.0)  # predict mean
        metrics = evaluate(y_true, y_pred)
        assert abs(metrics["val_r2"] - 0.0) < 1e-6

    def test_improvement_calculation(self):
        from autoresearch.prepare import evaluate, BASELINE_R2
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        metrics = evaluate(y_true, y_pred)
        assert abs(metrics["val_r2_improvement"] - (1.0 - BASELINE_R2)) < 1e-6

    def test_metrics_keys(self):
        from autoresearch.prepare import evaluate
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.2, 2.8])
        metrics = evaluate(y_true, y_pred)
        expected_keys = {"val_r2", "val_r2_improvement", "val_mae", "val_rmse", "val_spearman"}
        assert set(metrics.keys()) == expected_keys


class TestBaselinePredict:
    """Test the M9 baseline prediction."""

    def test_baseline_coefficients(self):
        from autoresearch.prepare import baseline_predict, M9_INTERCEPT, M9_SLOPE
        import pandas as pd

        df = pd.DataFrame({"tuntutan_years": [0.0, 1.0, 5.0, 10.0]})
        pred = baseline_predict(df)
        expected = M9_INTERCEPT + M9_SLOPE * df["tuntutan_years"].values
        np.testing.assert_array_almost_equal(pred, expected)

    def test_baseline_shape(self):
        from autoresearch.prepare import baseline_predict
        import pandas as pd

        df = pd.DataFrame({"tuntutan_years": [1.0, 2.0, 3.0]})
        pred = baseline_predict(df)
        assert pred.shape == (3,)


class TestConstants:
    """Test that key constants are set correctly."""

    def test_baseline_r2(self):
        from autoresearch.prepare import BASELINE_R2
        assert BASELINE_R2 == 0.600

    def test_time_budget(self):
        from autoresearch.prepare import TIME_BUDGET
        assert TIME_BUDGET == 60

    def test_random_seed(self):
        from autoresearch.prepare import RANDOM_SEED
        assert RANDOM_SEED == 42

    def test_m9_coefficients(self):
        from autoresearch.prepare import M9_INTERCEPT, M9_SLOPE
        assert M9_INTERCEPT == 0.49
        assert M9_SLOPE == 0.63


class TestPertimbanganExtraction:
    """Test the pertimbangan text extraction from fields.py."""

    def test_basic_extraction(self):
        from src.parser.fields import extract_pertimbangan_text
        text = (
            "Duduk perkara: Terdakwa melakukan korupsi. "
            "Menimbang, bahwa alasan-alasan kasasi yang diajukan "
            "oleh pemohon kasasi dapat dibenarkan. "
            "Bahwa Terdakwa terbukti secara sah dan meyakinkan bersalah "
            "melakukan tindak pidana korupsi sebagaimana dakwaan primair. "
            "Pertimbangan hakim telah memperhatikan hal-hal yang memberatkan "
            "dan hal-hal yang meringankan. Terdakwa menyesali perbuatannya "
            "dan berjanji tidak akan mengulangi. " * 5 +
            "M E N G A D I L I: "
            "Menjatuhkan pidana penjara selama 4 tahun"
        )
        result = extract_pertimbangan_text(text)
        assert result is not None
        assert "alasan-alasan kasasi" in result.lower()
        assert "mengadili" not in result.lower()

    def test_pertimbangan_hukum_header(self):
        from src.parser.fields import extract_pertimbangan_text
        text = (
            "Identitas terdakwa: JOHN DOE "
            "PERTIMBANGAN HUKUM "
            "Menimbang bahwa berdasarkan fakta-fakta hukum, terdakwa telah "
            "terbukti melakukan tindak pidana korupsi secara bersama-sama. "
            "Hal ini dibuktikan dengan keterangan saksi dan dokumen yang sah. "
            "Majelis hakim mempertimbangkan bahwa perbuatan terdakwa " * 5 +
            "M E N G A D I L I: "
            "Menjatuhkan pidana"
        )
        result = extract_pertimbangan_text(text)
        assert result is not None
        assert "pertimbangan hukum" in result.lower()

    def test_too_short_returns_none(self):
        from src.parser.fields import extract_pertimbangan_text
        text = (
            "Menimbang, bahwa singkat. "
            "M E N G A D I L I: "
            "Menjatuhkan pidana"
        )
        result = extract_pertimbangan_text(text)
        assert result is None

    def test_no_mengadili_returns_none(self):
        from src.parser.fields import extract_pertimbangan_text
        text = "Menimbang, bahwa terdakwa bersalah " * 20
        result = extract_pertimbangan_text(text)
        assert result is None

    def test_empty_returns_none(self):
        from src.parser.fields import extract_pertimbangan_text
        assert extract_pertimbangan_text("") is None
        assert extract_pertimbangan_text(None) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
