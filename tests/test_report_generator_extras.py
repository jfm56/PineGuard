import pytest
from app.nlp.report_generator import pipeline, Sentence, SequenceTagger, ReportGenerator


def test_pipeline_summarization():
    summarizer = pipeline('summarization')
    result = summarizer('test')
    assert isinstance(result, list)
    assert result[0].get('summary_text', None) == ''


def test_pipeline_generation():
    generator = pipeline('text-generation')
    result = generator('test')
    assert isinstance(result, list)
    assert result[0].get('generated_text', None) == ''


def test_sentence_and_sequence_tagger():
    # Sentence should be instantiable without error
    s = Sentence('hello world')
    assert isinstance(s, Sentence)
    # SequenceTagger.load should return None
    assert SequenceTagger.load('dummy') is None


def test_load_templates_keys():
    gen = ReportGenerator()
    templates = gen._load_templates()
    expected = {'very_high', 'high', 'moderate', 'low', 'very_low'}
    assert set(templates.keys()) == expected


def test_enhance_report_with_nlp(monkeypatch):
    # Create fake Doc with ents
    class FakeEnt:
        def __init__(self):
            self.text = 'Entity'
            self.label_ = 'LABEL'
    class FakeDoc:
        def __init__(self):
            self.ents = [FakeEnt()]
    gen = ReportGenerator()
    gen.nlp = lambda text: FakeDoc()
    # Override generator to return custom analysis
    gen.generator = lambda text, **kwargs: [{'generated_text': 'ExtraAnalysis'}]
    base = 'BaseReport'
    data = {'temperature': 20}
    enhanced = gen._enhance_report(base, data, {})
    assert base in enhanced
    assert 'Detailed Analysis:' in enhanced
    assert 'ExtraAnalysis' in enhanced
