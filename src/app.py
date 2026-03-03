import os
import sys
import tempfile
from flask import Flask, request, jsonify

# Ensure the root directory is in sys.path when running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_extractor import extract_text_from_pdf
from src.topic_modeler import TopicModeler

app = Flask(__name__)

# Initialize the topic modeler globally so it is loaded once when the server starts
print("Loading model... this may take a moment.")
modeler = TopicModeler(model_name="paraphrase-multilingual-MiniLM-L12-v2", n_topics=5)
print("Model loaded.")

@app.route('/extract_topics', methods=['POST'])
def extract_topics():
    if 'pdf' not in request.files:
        return jsonify({"error": "No 'pdf' file provided in the request"}), 400
        
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.pdf'):
        # Save to a temporary file because our extractor expects a file path
        fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        try:
            os.close(fd)
            file.save(temp_path)
            
            # Extract text
            documents = extract_text_from_pdf(temp_path)
            if not documents:
                return jsonify({"error": "No text found in the PDF or extraction failed"}), 400
                
            # Fit model and get topics
            topics = modeler.fit_and_get_topics(documents)
            
            # Format the response
            results = []
            for topic_id, top_words in topics:
                theme_words = [word for word, score in top_words[:3]]
                theme = " / ".join(theme_words).title()
                
                # Format the top words for the JSON response
                words = [{"word": word, "score": float(score)} for word, score in top_words]
                
                results.append({
                    "topic_id": topic_id,
                    "theme": theme,
                    "top_words": words
                })
                
            return jsonify({
                "status": "success",
                "document_chunks": len(documents),
                "topics": results
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        return jsonify({"error": "Invalid file format, please upload a PDF"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
