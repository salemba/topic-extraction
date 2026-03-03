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
        # Add an extensive list of residual stopwords and noise seen in French PDFs
        extra_stops = [
            'aussi', 'bien', 'cette', 'comme', 'dont', 'entre', 'les', 'leur', 
            'plus', 'sans', 'sous', 'vers', 'être', 'avoir', 'mais', 'ainsi', 
            'par', 'que', 'qui', 'dans', 'des', 'sur', 'pour', 'est', 'pas', 
            'une', 'avec', 'ces', 'aux', 'sont', 'ont', 'fait', 'faire', 'peut',
            'très', 'deux', 'tout', 'tous', 'toute', 'toutes', 'celui', 'ceux',
            'elle', 'elles', 'ils', 'nous', 'vous', 'quand', 'quel', 'quelle',
            'quelles', 'quels', 'parce', 'alors', 'donc', 'toujours', 'jamais'
        ]
        french_stop_words.extend(extra_stops)
        french_stop_words = list(set(french_stop_words)) # deduplicate
        
        vectorizer = CountVectorizer(
            stop_words=french_stop_words,
            ngram_range=(1, 2), # Allow bigrams for more context
            min_df=2, # Ignore terms that appear only once
            max_df=0.85, # HIGHEST IMPACT: Ignore terms that appear in >85% of documents (corpus-specific stop words)
            token_pattern=r'\b[a-zA-ZÀ-ÿ]{3,}\b' # Only keep words with 3 or more letters
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
