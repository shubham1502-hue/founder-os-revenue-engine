from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from revenue_leak import load_revenue_data


def test_load_revenue_data_rejects_missing_columns(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(
        "lead_id,source,created_at,demo_booked,demo_attended,revenue,sales_rep\n"
        "1,Organic,2025-01-08,1,1,5000,Neha\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as exc:
        load_revenue_data(path)

    message = str(exc.value)
    assert "missing required columns: converted" in message
    assert str(path) in message


def test_load_revenue_data_accepts_sample_schema():
    df = load_revenue_data(ROOT / "data" / "raw_data.csv")

    assert len(df) > 0
    assert {"demo_booked", "demo_attended", "converted", "revenue"}.issubset(df.columns)
