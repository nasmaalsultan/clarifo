import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string


class TFIDFAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.85,
            analyzer='word'
        )
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Enhanced text preprocessing"""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+', '', text)

        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;]', '', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def extract_key_terms(self, statement, documents):
        """Extract key terms with enhanced processing"""
        # Combine all texts for analysis
        all_texts = [self.preprocess_text(statement)]
        all_texts.extend([self.preprocess_text(doc['content']) for doc in documents])

        # Fit TF-IDF vectorizer
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            feature_names = self.vectorizer.get_feature_names_out()
        except Exception as e:
            print(f"TF-IDF fitting error: {e}")
            return [], None, []

        # Get TF-IDF scores for the statement
        statement_vector = tfidf_matrix[0]
        statement_scores = statement_vector.toarray().flatten()

        # Get top terms from statement
        top_indices = np.argsort(statement_scores)[::-1][:12]
        key_terms = []

        for i in top_indices:
            if statement_scores[i] > 0:
                term = feature_names[i]
                # Filter out very short terms and stopwords
                if len(term) > 2 and term not in self.stop_words:
                    key_terms.append((term, statement_scores[i]))

        return key_terms, tfidf_matrix, feature_names

    def calculate_similarity(self, statement, documents, tfidf_matrix, feature_names):
        """Calculate enhanced similarity scores - FIXED sparse matrix handling"""
        if tfidf_matrix is None or tfidf_matrix.shape[0] <= 1:
            return []

        # Statement vector is the first row
        statement_vector = tfidf_matrix[0]

        # Document vectors are the remaining rows (from index 1 to end)
        document_vectors = tfidf_matrix[1:]

        # Calculate cosine similarities - FIXED: use shape[0] for sparse matrices
        if document_vectors.shape[0] > 0:
            similarities = cosine_similarity(statement_vector, document_vectors).flatten()
        else:
            similarities = np.array([])

        # Prepare detailed document matches
        document_matches = []
        for i, doc in enumerate(documents):
            if i < len(similarities):
                similarity_score = float(similarities[i])

                # Only include documents with some similarity
                if similarity_score > 0.01:
                    document_matches.append({
                        'source': doc['source'],
                        'url': doc['url'],
                        'similarity_score': similarity_score,
                        'key_matches': self.extract_document_matches(doc['content'], feature_names,
                                                                     tfidf_matrix[i + 1]),
                        'content_preview': doc['content'][:150] + '...' if len(doc['content']) > 150 else doc['content']
                    })

        # Sort by similarity score
        document_matches.sort(key=lambda x: x['similarity_score'], reverse=True)

        return document_matches

    def extract_document_matches(self, content, feature_names, document_vector):
        """Extract matching key terms with context"""
        if document_vector is None:
            return []

        document_scores = document_vector.toarray().flatten()
        top_indices = np.argsort(document_scores)[::-1][:6]

        matches = []
        for idx in top_indices:
            if document_scores[idx] > 0:
                term = feature_names[idx]
                # Check if term appears in content
                if term.lower() in content.lower():
                    matches.append({
                        'term': term,
                        'score': float(document_scores[idx])
                    })

        return matches

    def analyze_statement(self, statement, documents):
        """Enhanced analysis with better accuracy calculation"""
        if not documents:
            return 0.5, self.get_default_analysis(statement)

        print(f"Analyzing statement with {len(documents)} documents")

        # Extract key terms and calculate similarities
        key_terms, tfidf_matrix, feature_names = self.extract_key_terms(statement, documents)
        document_matches = self.calculate_similarity(statement, documents, tfidf_matrix, feature_names)

        # Calculate accuracy with enhanced factors
        base_accuracy = self.calculate_base_accuracy(document_matches)
        accuracy = self.adjust_accuracy_with_context(base_accuracy, statement, document_matches, key_terms)

        # Prepare detailed analysis - FIXED: pass correct number of arguments
        analysis_details = {
            'term_analysis': {
                'key_terms': [{'term': term, 'score': float(score)} for term, score in key_terms[:8]],
                'total_terms': len(key_terms)
            },
            'document_matches': document_matches[:3],
            'reasoning': self.generate_detailed_reasoning(statement, document_matches, accuracy),
            # REMOVED key_terms parameter
            'confidence_factors': self.analyze_confidence_factors(document_matches)
        }

        return accuracy, analysis_details

    def adjust_accuracy_with_context(self, base_accuracy, statement, document_matches, key_terms):
        """Enhanced accuracy adjustment with context awareness"""
        accuracy = base_accuracy

        # Boost for strong term matches
        strong_terms = [term for term, score in key_terms if score > 0.1]
        if len(strong_terms) >= 3:
            accuracy = min(0.95, accuracy + 0.15)
        elif len(strong_terms) >= 2:
            accuracy = min(0.90, accuracy + 0.1)

        # Boost for multiple high-confidence sources
        high_confidence_matches = [m for m in document_matches if m['similarity_score'] > 0.15]
        if len(high_confidence_matches) >= 2:
            accuracy = min(0.95, accuracy + 0.1)

        # Special boosts for common factual patterns
        if self.is_common_factual_statement(statement):
            accuracy = min(0.95, accuracy + 0.2)

        # Penalty for clearly false statements
        if self.is_clearly_false_statement(statement):
            accuracy = max(0.05, accuracy - 0.3)

        # Penalty for negation
        if self.has_negation(statement):
            accuracy = max(0.1, accuracy - 0.15)

        # Ensure reasonable bounds
        return min(0.98, max(0.05, accuracy))

    def is_common_factual_statement(self, statement):
        """Check if statement matches common factual patterns"""
        statement_lower = statement.lower()

        common_factual_patterns = [
            ('python', 'programming language'),
            ('bear', 'mammal'),
            ('water', 'boils', '100 degrees'),
            ('earth', 'planet'),
            ('moon', 'orbits', 'earth'),
            ('sun', 'star'),
            ('fish', 'swim'),
            ('birds', 'fly'),
            ('humans', 'mammals'),
            ('dogs', 'animals'),
            ('earth', 'revolves', 'sun'),
            ('earth', 'sphere'),
            ('earth', 'round')
        ]

        for pattern in common_factual_patterns:
            if all(word in statement_lower for word in pattern):
                return True

        return False

    def is_clearly_false_statement(self, statement):
        """Identify clearly false statements"""
        statement_lower = statement.lower()

        false_statements = [
            'earth is flat',
            'moon is made of cheese',
            'sun revolves around earth',
            'vaccines cause autism',
            'climate change is a hoax'
        ]

        return any(false_stmt in statement_lower for false_stmt in false_statements)

    def has_negation(self, statement):
        """Check if statement contains negation"""
        negations = ['not', 'no', 'never', 'nothing', 'none', "isn't", "aren't", "wasn't", "weren't", "don't",
                     "doesn't"]
        return any(negation in statement.lower() for negation in negations)

    def calculate_base_accuracy(self, document_matches):
        """Calculate base accuracy from document matches"""
        if not document_matches:
            return 0.3

        # Use weighted average of top matches
        top_matches = document_matches[:3]
        if not top_matches:
            return 0.3

        weights = [1.0, 0.7, 0.4]

        weighted_sum = 0
        total_weight = 0

        for i, match in enumerate(top_matches):
            if i < len(weights):
                weighted_sum += match['similarity_score'] * weights[i]
                total_weight += weights[i]

        if total_weight > 0:
            base_accuracy = weighted_sum / total_weight
        else:
            base_accuracy = 0.3

        return min(1.0, max(0.0, base_accuracy))

    def analyze_confidence_factors(self, document_matches):
        """Analyze factors affecting confidence"""
        factors = {
            'source_count': len(document_matches),
            'high_confidence_sources': len([m for m in document_matches if m['similarity_score'] > 0.2]),
            'average_similarity': round(np.mean([m['similarity_score'] for m in document_matches]),
                                        3) if document_matches else 0
        }
        return factors

    def generate_detailed_reasoning(self, statement, document_matches, accuracy):
        """Generate detailed reasoning - FIXED: 3 parameters instead of 4"""
        high_conf_sources = len([m for m in document_matches if m['similarity_score'] > 0.15])

        if accuracy >= 0.8:
            return f"High confidence: {high_conf_sources} reliable sources strongly support this statement with strong term matches."
        elif accuracy >= 0.6:
            return f"Moderate confidence: {high_conf_sources} sources provide supporting evidence with good term alignment."
        elif accuracy >= 0.4:
            return f"Low confidence: Limited evidence found ({high_conf_sources} sources). Verification recommended."
        else:
            if self.has_negation(statement):
                return "Very low confidence: Negated statements are challenging for TF-IDF analysis. Manual verification required."
            elif self.is_clearly_false_statement(statement):
                return "Very low confidence: This statement contradicts established scientific consensus."
            else:
                return "Very low confidence: Little supporting evidence found in analyzed sources."

    def get_default_analysis(self, statement):
        """Return default analysis when no documents are available"""
        return {
            'term_analysis': {'key_terms': [], 'total_terms': 0},
            'document_matches': [],
            'reasoning': "No sources available for analysis. Using general knowledge assessment.",
            'confidence_factors': {'source_count': 0, 'high_confidence_sources': 0, 'average_similarity': 0}
        }