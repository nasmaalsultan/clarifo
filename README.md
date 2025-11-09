# Clarifo

Clarifo is a fact-checking web app that verifies statements using TF-IDF and data from credible sources like Wikipedia and Britannica. An explorative NLP project promoting critical thinking and digital literacy. Find Clarifo on Instagram: @checkwithclarifo

NOTICE: Clarifo is still under development in order to improve its accuracy

---

## Features

- Automated Web Scraping — Collects information from credible sources like Wikipedia, Britannica, and National Geographic using BeautifulSoup.
- TF-IDF Analysis — Uses scikit-learn to calculate text similarity and derive a confidence score.
- Dynamic UI — Built with HTML, CSS, and JavaScript for real-time fact-checking results.
- Complexity Detection — Estimates statement complexity (Low, Medium, High) based on structure and negation.
- Term Extraction — Displays the most relevant key terms contributing to the analysis.
- Fallback Logic — Simulated content and conservative accuracy when scraping fails (ensures reliable performance).

--

## Project Structure

Clarifo/
│
├── app.py # Flask app entry point
├── requirements.txt # Dependencies
├── setup_nltk.py # Script to set up NLTK resources
│
├── templates/
│ └── index.html # Main web interface
│
├── static/
│ ├── style.css # Frontend styling
│ └── script.js # Client-side logic
│
└── utils/
├── tfidf_analyzer.py # TF-IDF text analysis logic
└── web_scraper.py # Web scraping and content retrieval

---

## How It Works

1. **User Input** — The user enters a statement to verify.  
2. **Web Search & Scraping** — The system retrieves relevant sources from Wikipedia and other reference sites.  
3. **TF-IDF Analysis** — The statement and source documents are vectorized and compared using cosine similarity.  
4. **Confidence Calculation** — A confidence score (0–100%) is derived from semantic overlap and contextual factors.  
5. **Result Display** — Key terms, analyzed sources, processing time, and statement complexity are shown interactively.  

---

## Installation and Setup

1. Clone the Repo
```bash
git clone https://github.com/yourusername/Clarifo.git
cd Clarifo

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt

4. Setup NLTK
python setup_nltk.py

5. Run the App
python app.py

---

## Example Usage

<img width="1446" height="736" alt="image" src="https://github.com/user-attachments/assets/61d96ce5-8375-4647-a6af-61668d3515be" />
<img width="1448" height="749" alt="image" src="https://github.com/user-attachments/assets/e5371b75-9dc6-45b0-b765-03a8a5c00532" />


---

## What I Learned

Through building Clarifo, I learned to:
- Integrate NLP techniques like TF-IDF with real-world web data.
- Use BeautifulSoup and Requests for dynamic content scraping.
- Handle text preprocessing, stopword removal, and similarity computation.
- Design a full-stack Flask web app with asynchronous client-server interaction.
- Manage error handling, fallback logic, and ensure robustness against scraping failures.
- Visualize analytical results with dynamic front-end components.
- Balance computational performance with real-time user experience.

But more importantly, Clarifo taught me how how understanding language at a computational level can help address challenges like misinformation and digital literacy.
