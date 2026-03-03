from turftopic import SemanticSignalSeparation
from sentence_transformers import SentenceTransformer

class TopicModeler:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2", n_topics: int = 5):
        """
        Initializes the topic modeler with a multilingual sentence transformer.
        
        Args:
            model_name: The SentenceTransformer model to use.
            n_topics: Number of topics to extract.
        """
        self.encoder = SentenceTransformer(model_name)
        
        # Use CountVectorizer with French stop words and n-grams to get better topics
        from sklearn.feature_extraction.text import CountVectorizer
        from stop_words import get_stop_words
        
        french_stop_words = get_stop_words('fr')
        # Add a few more common terms that might appear in PDF parsing
        french_stop_words.extend(['aussi', 'bien', 'cette', 'comme', 'dont', 'entre', 'les', 'leur', 'plus', 'sans', 'sous', 'vers', 'être', 'avoir'])
        
        vectorizer = CountVectorizer(
            stop_words=french_stop_words,
            ngram_range=(1, 2), # Allow bigrams for more context
            min_df=2 # Ignore terms that appear only once
        )

        # Using SemanticSignalSeparation which works well out of the box
        self.model = SemanticSignalSeparation(
            n_components=n_topics,
            encoder=self.encoder,
            vectorizer=vectorizer
        )
        
    def fit_and_get_topics(self, documents: list[str]) -> list:
        """
        Fits the topic model on the provided documents and returns the topics.
        
        Args:
            documents: List of text documents.
            
        Returns:
            The topic descriptions.
        """
        print(f"Fitting topic model on {len(documents)} document pages/chunks...")
        self.model.fit(documents)
        
        # model.print_topics() outputs to console, but we might want to return them
        # turftopic models usually provide way to get topic words
        topic_info = self.model.get_topics()
        return topic_info
        
    def print_topics(self):
        """Prints the topics found"""
        self.model.print_topics()
