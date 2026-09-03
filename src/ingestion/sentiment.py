import logging
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Epoch 20: NLP Sentiment Analysis
    Uses a pre-trained FinBERT model to extract sentiment from financial news/tweets.
    """
    def __init__(self, model_name: str = "ProsusAI/finbert"):
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not installed. Running in mock mode.")
            self.nlp = None
        else:
            logger.info(f"Loading {model_name} for Sentiment Analysis...")
            # Initialize HuggingFace pipeline for sentiment analysis
            self.nlp = pipeline("sentiment-analysis", model=model_name)
            
    def analyze_text(self, text: str) -> dict:
        """
        Analyzes the text and returns a sentiment score between -1.0 (Negative) and 1.0 (Positive)
        """
        if self.nlp is None:
            # Mock behavior
            return {"label": "neutral", "score": 0.0, "raw": []}
            
        try:
            result = self.nlp(text)[0]
            label = result['label'].lower()
            confidence = result['score']
            
            # Convert to -1.0 to 1.0 scale
            if label == 'positive':
                score = confidence
            elif label == 'negative':
                score = -confidence
            else:
                score = 0.0
                
            return {
                "label": label,
                "score": score,
                "raw": result
            }
        except Exception as e:
            logger.error(f"Failed to analyze text: {e}")
            return {"label": "neutral", "score": 0.0, "raw": []}
