# MOZAHID Anti RAG 🚀
## FIRST METHOD
A premium Retrieval-Augmented Generation (RAG) application that allows you to upload Excel or CSV files and ask questions about your data using DeepSeek (via OpenRouter) and the FAISS vector database.
<img width="1644" height="919" alt="image" src="https://github.com/user-attachments/assets/b2fedb49-d037-407f-aedb-efff6697e3b8" />

## ✨ Features
- **High-Quality Inference**: Powered by **DeepSeek** (via OpenRouter) for accurate, context-aware answers.
- **Local Vector Search**: Uses **FAISS** for efficient similarity search across your data.
- **Excel & CSV Ingestion**: Converts spreadsheets into searchable context chunks.
- **Glassmorphic UI**: A modern, professional React interface.
- **Data Privacy**: Local embedding generation ensures minimal data exposure.

## 🛠️ Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [LangChain](https://www.langchain.com/), [FAISS](https://github.com/facebookresearch/faiss), [Pandas](https://pandas.pydata.org/)
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence-Transformers)
- **LLM**: [DeepSeek](https://www.deepseek.com/) via [OpenRouter](https://openrouter.ai/)
- **Frontend**: [React](https://react.dev/), [Vite](https://vitejs.dev/), [Axios](https://axios-http.com/)

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js**: v18+ 
- **Python**: v3.10+
- **OpenRouter API Key**: Get it from [OpenRouter](https://openrouter.ai/keys)

### 2. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OpenRouter key:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
4. Start the server:
   ```bash
   python main.py
   ```

### 3. Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

---

## 📖 How to Use
1. **Upload**: Drop your `.xlsx`, `.xls`, or `.csv` file into the upload zone in the sidebar.
2. **Indexing**: The app will process your data and create a local vector index (FAISS).
3. **Ask**: Once the status shows "Active", ask questions like:
   - *"What is the total revenue listed in the 'Sales' sheet?"*
   - *"Who are the top 5 performers based on the data?"*
   - *"Summarize the trends for Q1."*

---

## 🏗️ Architecture
1. **Ingestion**: `Pandas` reads the uploaded Excel/CSV file. Each row is converted into a structured text document.
2. **Indexing**: `SentenceTransformers` generates 384-dimensional embeddings for each row.
3. **Retrieval**: When a query is made, `FAISS` calculates cosine similarity to find the most relevant context.
4. **Generation**: Relevant chunks are formatted into a prompt and sent to **DeepSeek** for the final answer.

## SECOND METHOD 
<img width="1631" height="952" alt="image" src="https://github.com/user-attachments/assets/f397f017-c5be-47f4-9977-b541f4f675e1" />

<img width="425" height="645" alt="image" src="https://github.com/user-attachments/assets/e8091d5e-de5f-453e-a2a7-917a83c9668c" />
<img width="1112" height="676" alt="image" src="https://github.com/user-attachments/assets/aa3f0bf8-8994-432b-9048-2ec6a4e8d7de" />


