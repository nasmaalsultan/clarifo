from flask import Flask, render_template, request, jsonify
from utils.tfidf_analyzer import TFIDFAnalyzer
from utils.web_scraper import WebScraper
import time
import traceback

app = Flask(__name__)

# Initialize components
tfidf_analyzer = TFIDFAnalyzer()
web_scraper = WebScraper()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_fact', methods=['POST'])
def check_fact():
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()

        if not statement:
            return jsonify({'error': 'Please enter a statement to check'}), 400

        print(f"Checking statement: {statement}")

        # Start timing
        start_time = time.time()

        # Step 1: Search for relevant sources
        print("Searching for relevant sources...")
        sources = web_scraper.search_sources(statement)

        # Step 2: Scrape content from sources
        print("Scraping content from sources...")
        documents = []
        successful_scrapes = 0

        for source in sources:
            if successful_scrapes >= 3:  # Limit to 3 successful scrapes for speed
                break

            content = web_scraper.scrape_content(source['url'])
            if content and len(content) > 100:
                documents.append({
                    'source': source['name'],
                    'url': source['url'],
                    'content': content,
                    'relevance': source.get('relevance', 0.5)
                })
                successful_scrapes += 1
                print(f"Successfully scraped content from {source['name']}")

        print(f"Successfully collected {len(documents)} documents for analysis")

        # Step 3: Analyze with TF-IDF
        print("Analyzing with TF-IDF...")
        if documents:
            accuracy, analysis_details = tfidf_analyzer.analyze_statement(statement, documents)
            print(f"TF-IDF analysis completed with accuracy: {accuracy}")
        else:
            accuracy = 0.4  # Conservative default when scraping fails
            analysis_details = {
                'term_analysis': {'key_terms': [], 'total_terms': 0},
                'document_matches': [],
                'reasoning': "Unable to retrieve sufficient source content for analysis.",
                'confidence_factors': {'source_count': 0, 'high_confidence_sources': 0, 'average_similarity': 0}
            }
            print("Using fallback analysis due to scraping issues")

        # Calculate processing time
        processing_time = round(time.time() - start_time, 2)

        # Prepare response
        response = {
            'accuracy': accuracy,
            'processing_time': processing_time,
            'sources_analyzed': len(documents),
            'analysis_details': analysis_details,
            'sources': [{
                'name': doc['source'],
                'url': doc['url'],
                'confidence': min(0.95, doc.get('relevance', 0.5) * accuracy)
            } for doc in documents],
            'complexity': analyze_complexity(statement)
        }

        print(f"Analysis complete. Final accuracy: {accuracy}")
        return jsonify(response)

    except Exception as e:
        print(f"Error in fact checking: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify(
            {'error': 'An error occurred during analysis. Please try a different statement or try again later.'}), 500

def analyze_complexity(statement):
    """Analyze statement complexity"""
    words = statement.split()
    word_count = len(words)

    negations = ['not', 'no', 'never', 'nothing', 'none']
    has_negation = any(negation in statement.lower() for negation in negations)

    if has_negation or word_count > 20:
        return "High"
    elif word_count > 12:
        return "Medium"
    else:
        return "Low"


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')