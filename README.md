# 🚀🧠 Mini AI Search Engine for PDFs

A mini AI-powered search engine that lets you upload multiple PDFs (like Radiography materials) and ask natural language questions. Choose how the AI answers: strictly from the source, loosely, or with enhanced flexibility.

## 📽️ Demo Preview

https://x.com/PaschalUchennaG/status/1910488444179972602

## 📦 Features

- Upload multiple PDF files
- Ask questions in natural language
- Three response modes:
  - Strict (source-based)
  - Loose (flexible)
  - Enhanced (LLM-reviewed)
- Source highlighting
- Simple UI via Streamlit

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/paschal-godwin/mini-search-engine.git
cd mini-search-engine
```

### 2. Install Dependencies

Make sure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```

### 3. Add Your OpenAI API Key

Create a .env file in the root of the project and add your OpenAI key:

```env
OPENAI_API_KEY=your-openai-key-here
```

### 4. Run the App

```bash
streamlit run main.py
```

---

## 🧰 Tech Stack

- Streamlit
- LangChain
- ChromaDB
- OpenAI Embeddings
- Python 3.10+

---

## 📄 License

This project is licensed under the Apache 2.0 License.

✅ Free to use  
🙏 Please give credit if you build on it or share it publicly.

---

## ✍🏽 Author

**Paschal Godwin**  
Training LLMs by day, reading X-rays by night.  
Twitter/X: @PaschalUchennaG  
GitHub: https://github.com/paschal-godwin

---

Built with love, fear, and late nights ☕.