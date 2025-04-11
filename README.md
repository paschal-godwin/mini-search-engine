# 🔍 Mini AI Search Engine for PDFs

An AI-powered Streamlit app that lets you upload multiple PDFs (e.g. Radiography lecture notes or any course material), ask questions in natural language, and get answers with source references.

Built to support different reasoning styles using **LangChain**, **OpenAI**, and **ChromaDB**, this app offers 3 powerful answer modes:

- ✅ **Strict** — answers strictly from retrieved content  
- 🌀 **Loose** — uses flexible context matching with MMR  
- 🤖 **Enhanced** — lets the LLM refine, validate, and rephrase the response

---

## 📽️ Demo

🎥 [Watch the demo on Twitter](https://x.com/PaschalUchennaG/status/1910488444179972602)

---

## ✨ Features

- 📂 Upload and parse **multiple PDFs**
- ❓ Ask **natural language** questions
- 🔀 Choose answer mode:
  - **Strict** – context-only answers
  - **Loose** – fuzzy flexible answers using MMR
  - **Enhanced** – smart LLM-reviewed response
- 📌 Returns answers with **source references**
- 🧠 Caches stored PDFs + lets you upload new ones
- 🧼 Clear/reset mode and live toggling between reasoning styles

---

## 🛠️ Tech Stack

- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [OpenAI API](https://openai.com/)
- [Streamlit](https://streamlit.io/)
- Python 3.10+

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Add your OpenAI API key
Create a .env file:

env
Copy
Edit
OPENAI_API_KEY=your-openai-key
4. Run the app
bash
Copy
Edit
streamlit run main.py
🧪 Example Use Cases
📚 Radiography students studying for exams

🧠 Summarizing large technical PDF content

📄 Quick search and QA over any academic or textbook materials

👨‍💻 Author
Paschal Godwin
📍 Twitter/X: @PaschalUchennaG

📄 License
Licensed under the Apache 2.0 License.
✅ Free to use
🙏 Just give credit if you build on it or share it publicly.

💬 Feedback & Contributions
Open to feedback, suggestions, and collaborations. Feel free to create issues or fork the repo!

yaml
Copy
Edit

---

### ✅ Next Step:
1. Copy that into your `README.md`
2. Save, commit, and push:
```bash
git add README.md
git commit -m "Updated README with demo, Streamlit, and features"
git push

Built with love, fear, and late nights by Paschal.

