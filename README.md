# Mini Search Engine for Radiography PDFs

A LangChain-powered AI tool that lets you search through multiple radiography course PDFs and get improved, LLM-reviewed answers. It’s built for medical students who want fast, relevant answers — with sources.

---

## Features
- **Multi-PDF Search**: Upload multiple PDFs and extract page-level text with metadata.
- **RAG (Retrieval-Augmented Generation)**: Uses ChromaDB as vector store and OpenAI for answers.
- **Strict vs Loose Mode**:
  - *strict*: Focused on accurate, source-based responses.
  - *loose*: Allows more flexible responses based on a wider context.
- **LLM Answer Review**:
  - *enhanced*: The AI checks if its own answer actually answers the question and suggests improvements.

---

## Stack
- **Python 3.10**
- **LangChain**
- **OpenAI**
- **ChromaDB**
- **Streamlit (future UI)**
- **Fitz (PyMuPDF)** for PDF parsing
- **dotenv** for API key management

---

## How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/paschal-godwin/mini-search-engine.git
cd mini-search-engine
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your `.env` file**
```env
OPENAI_API_KEY=your_openai_key_here
```

5. **Run the app**
```bash
python main.py
```

---

## Example Use Case
> “Who is the father of radiography?”  
**Enhanced mode answer:** Wilhelm Conrad Röntgen, who discovered X-rays in 1895 — with reviewed suggestions and source references.

---

## Future Improvements
- Streamlit interface for upload and Q&A
- Option to upload new PDFs dynamically
- Add support for local embeddings (no OpenAI)

---

## License
This project is licensed under the Apache 2.0 License — free to use, modify, and distribute **with attribution to Paschal Godwin**

---

Built with love, fear, and late nights by Paschal.

