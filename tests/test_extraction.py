import pytest
from src.pdf_extractor import extract_text_from_pdf
from src.topic_modeler import TopicModeler

def test_topic_modeler_initialization():
    # Simple test to ensure the class initializes properly (no missing imports/etc)
    modeler = TopicModeler(n_topics=2)
    assert modeler is not None

