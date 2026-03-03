# Topic Extractor / Extracteur de Sujets

A Python project to securely extract text from PDFs and detect main topics using the `turftopic` library.
*Un projet Python pour extraire le texte de fichiers PDF et détecter les sujets principaux à l'aide de la bibliothèque `turftopic`.*

## Project Structure / Structure du projet

- `src/pdf_extractor.py`: Handles reading and parsing PDF files using PyMuPDF.
- `src/topic_modeler.py`: Setup and run Semantic Signal Separation for topic modeling. (Configured with French stop words and n-grams).
- `src/main.py`: CLI entry point to run the pipeline.
- `data/raw/`: Place your raw PDFs here. (Ignored by git)
- `data/processed/`: Output directory if needed. (Ignored by git)

## Setup / Installation

1. Make sure you have Python 3 installed. / *Assurez-vous d'avoir Python 3 installé.*
2. Initialize and activate a virtual environment: / *Initialisez et activez un environnement virtuel :*
   - Windows: `python -m venv venv` then `.\venv\Scripts\activate`
   - Linux/Mac: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies: / *Installez les dépendances :*
   ```bash
   pip install -r requirements.txt
   ```

## Usage / Utilisation

Run the main pipeline using: / *Lancez le script principal avec :*

```bash
python src/main.py data/raw/sample.pdf
```

Optional arguments / *Arguments optionnels* :
- `--model`: HuggingFace sentence transformer model name (default: `paraphrase-multilingual-MiniLM-L12-v2`).
- `--topics`: Number of topics to extract (default: 5).

Example / *Exemple* :
```bash
python src/main.py --topics 3 data/raw/marche_normes.pdf
```

### Sample Output / Exemple de résultat

```text
Extracting text from data/raw/marche_normes.pdf...
Initializing Topic Modeler...
Fitting topic model on 13 document pages/chunks...

--- Extracted Topics ---
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Topic ID ┃ Highest Ranking                                                    ┃ Lowest Ranking                                              ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│        0 │ emploi, travail, plus, œuvre, 2005, marché, mais, au, ainsi, entre │ paris, le, droit, des, leur, être, la, il, ne, les          │
├──────────┼────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│        1 │ paris, ne, le, marché, des, droit, les, au, pas, par               │ emploi, comme, plus, ainsi, du, bien, ce, aussi, pour, mais │
├──────────┼────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│        2 │ marché, aussi, qu, comme, même, que, ainsi, ce, mais, qui          │ emploi, travail, paris, œuvre, le, au, les, être, se, il    │
└──────────┴────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

[Metrics] Finished in 6.29 seconds.
```
