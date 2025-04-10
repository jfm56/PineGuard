import pytest
from app.risk_category import RiskCategory

def test_risk_category_values():
    assert RiskCategory.LOW.value == "low"
    assert RiskCategory.MODERATE.value == "moderate"
    assert RiskCategory.HIGH.value == "high"

def test_risk_category_comparison():
    assert RiskCategory.LOW != RiskCategory.MODERATE
    assert RiskCategory.MODERATE != RiskCategory.HIGH
    assert RiskCategory.LOW != RiskCategory.HIGH

def test_risk_category_string_representation():
    assert str(RiskCategory.LOW) == "RiskCategory.LOW"
    assert str(RiskCategory.MODERATE) == "RiskCategory.MODERATE"
    assert str(RiskCategory.HIGH) == "RiskCategory.HIGH"
