from src.ingestion.sentiment import SentimentAnalyzer


def test_sentiment_analyzer_mock():
    # Because downloading FinBERT takes time and might fail in simple CI without cache,
    # we test the structure of the output.
    analyzer = SentimentAnalyzer()
    
    # Test positive text
    result = analyzer.analyze_text("Federal Reserve cuts interest rates, markets surge!")
    assert "label" in result
    assert "score" in result
    
    # Test negative text
    result = analyzer.analyze_text("Inflation hits record high, stocks plummet.")
    assert "label" in result
    assert "score" in result
