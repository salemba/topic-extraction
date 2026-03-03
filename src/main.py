import argparse
import sys
import os

# Ensure the root directory is in sys.path when running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.pdf_extractor import extract_text_from_pdf
from src.topic_modeler import TopicModeler

def main():
    parser = argparse.ArgumentParser(description="Extract topics from a French PDF.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("--model", type=str, default="paraphrase-multilingual-MiniLM-L12-v2", 
                        help="SentenceTransformer model name")
    parser.add_argument("--topics", type=int, default=5, 
                        help="Number of topics to extract")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: File '{args.pdf_path}' not found.")
        sys.exit(1)

    import time
    start_time = time.time()
    
    print(f"Extracting text from {args.pdf_path}...")
    documents = extract_text_from_pdf(args.pdf_path)
    
    if not documents:
        print("No text found in the PDF or an error occurred during extraction.")
        sys.exit(1)
        
    print("Initializing Topic Modeler...")
    modeler = TopicModeler(model_name=args.model, n_topics=args.topics)
    
    topics = modeler.fit_and_get_topics(documents)
    
    print("\n--- Extracted Topics ---")
    modeler.print_topics()
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n[Metrics] Finished in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
