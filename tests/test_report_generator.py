import pytest
from app.nlp.report_generator import ReportGenerator


def test_analyze_risk_factors():
    gen = ReportGenerator()
    data = {
        'temperature': 31,
        'humidity': 25,
        'wind_speed': 25,
        'vegetation_density': 0.8
    }
    factors = gen._analyze_risk_factors(data)
    assert 'high temperature' in factors
    assert 'low humidity' in factors
    assert 'high wind speed' in factors
    assert 'dense vegetation' in factors
    assert len(factors) == 4


def test_generate_recommendations_high():
    gen = ReportGenerator()
    risk_level = 'high'
    factors = ['high temperature', 'low humidity']
    recs = gen._generate_recommendations(risk_level, factors, {})
    rec_lines = recs.splitlines()
    # Default high-level recommendations
    assert "- Implement immediate fire prevention measures" in rec_lines
    assert "- Increase monitoring frequency" in rec_lines
    assert "- Alert local fire authorities" in rec_lines
    # Factor-specific recommendations
    assert "- Monitor weather conditions closely" in rec_lines
    assert "- Consider controlled humidification measures" in rec_lines


def test_enhance_report_and_summary():
    gen = ReportGenerator()
    base = "Base report"
    data = {'temperature': 20, 'humidity': 50, 'wind_speed': 10}
    enhanced = gen._enhance_report(base, data, {})
    assert enhanced.startswith("Base report")
    assert "Detailed Analysis:" in enhanced
    summary = gen._generate_summary(enhanced)
    assert summary == ""


def test_generate_risk_report_full():
    gen = ReportGenerator()
    data = {
        'risk_category': 'High',
        'temperature': 35,
        'humidity': 25,
        'wind_speed': 25,
        'vegetation_density': 0.9
    }
    report = gen.generate_risk_report(data, 'TestLoc', {})
    # Ensure structure
    assert 'summary' in report
    assert 'full_report' in report
    assert 'risk_factors' in report
    assert 'recommendations' in report
    # Risk factors extracted correctly
    assert report['risk_factors'] == [
        'high temperature',
        'low humidity',
        'high wind speed',
        'dense vegetation'
    ]
    # full_report includes location and recommendations header
    assert 'TestLoc' in report['full_report']
    assert 'Recommendations:' in report['full_report']
    # summary stub is empty
    assert report['summary'] == ""
    # recommendations include high-level recs
    assert "- Implement immediate fire prevention measures" in report['recommendations']


def test_generate_risk_report_low():
    gen = ReportGenerator()
    data = {
        'risk_category': 'Low',
        'temperature': 20,
        'humidity': 50,
        'wind_speed': 10
    }
    report = gen.generate_risk_report(data, 'Loc', {})
    # No risk factors
    assert report['risk_factors'] == []
    # recommendations should be empty
    assert report['recommendations'] == ""
