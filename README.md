# 🩺 AI Medical Assistant

A production-ready AI-powered Medical Assistant built using **Flask, LangChain, NVIDIA Nemotron 3 Ultra, Retrieval-Augmented Generation (RAG), FAISS, OCR, Voice AI, and Authentication**. The application helps users analyze medical reports, ask health-related questions, and receive intelligent, context-aware responses from trusted medical knowledge.

---

# 📖 About The Project

AI Medical Assistant is an intelligent healthcare platform that combines the power of **Large Language Models (LLMs)** with **Retrieval-Augmented Generation (RAG)** to provide accurate and context-aware medical assistance.

The application allows users to:

- 💬 Chat with an AI Medical Assistant
- 📄 Upload and analyze medical reports
- 🔍 Retrieve answers from medical documents using RAG
- 🎤 Interact using voice commands
- 📚 Store conversation history
- 👤 Manage personal health reports securely
- 📅 Track appointments and medication reminders

Unlike a standard chatbot, this assistant retrieves relevant medical information from a vector database before generating responses, making the answers more reliable and informative.

---

# 🚀 Getting Started

Follow these steps to set up the project on your local machine.

## Prerequisites

- Python 3.11+
- NVIDIA API Key
- Flask
- LangChain
- FAISS
- SQLite
- Tesseract OCR (for image analysis)
- Docker (Optional)

---

# 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Krishna270704/AI-Medical-assistant.git

cd Medical-assistant
```

---

### 2. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory.

Example:

```env
LLM_PROVIDER=nvidia

NVIDIA_API_KEY=YOUR_API_KEY

MODEL_NAME=nvidia/nemotron-3-ultra-550b-a55b

SECRET_KEY=your_secret_key

DATABASE_URL=sqlite:///medical.db
```

---

### 5. Add Medical Knowledge Base

(Optional but Recommended)

Place your medical PDFs, TXT, or Markdown files inside:

```
data/documents/
```

The application automatically creates FAISS embeddings during startup.

---

### 6. Install OCR

Install Tesseract OCR.

Windows users should add the installation path to the system PATH.

---

### 7. Run the Project

```bash
python run.py
```

Open your browser:

```
http://localhost:5000
```

---

# ✨ Features

## 🤖 AI Medical Chat

- NVIDIA Nemotron 3 Ultra
- Context-aware conversations
- LangChain integration
- Conversation memory
- Streaming responses

---

## 📚 Retrieval-Augmented Generation (RAG)

- Medical PDF ingestion
- FAISS Vector Database
- Semantic Search
- Source Attribution
- Knowledge Retrieval

---

## 📄 Medical Report Analysis

- Upload PDF
- Upload Images
- OCR Extraction
- AI Report Summary
- Medical Term Simplification
- Risk Detection
- Follow-up Recommendations

---

## 🎤 Voice Assistant

- Speech-to-Text
- Text-to-Speech
- Voice Chat
- English Support
- Hindi Support
- Hinglish Support

---

## 👤 User Management

- Secure Login
- Registration
- Profile Management
- Chat History
- Session Management

---

## 📅 Healthcare Dashboard

- Medical Reports
- Appointments
- Medication Reminders
- Health Insights
- Personal Dashboard

---

## 🔒 Security

- Secure Authentication
- Password Hashing
- CSRF Protection
- Secure File Upload
- Environment Variables
- Input Validation

---

# 🏗️ Tech Stack

### Backend

- Python
- Flask
- LangChain

### AI

- NVIDIA Nemotron 3 Ultra
- HuggingFace Embeddings
- FAISS

### OCR

- Tesseract OCR
- PyMuPDF
- Pillow

### Database

- SQLite
- SQLAlchemy

### Frontend

- HTML
- CSS
- JavaScript
- Bootstrap

### Deployment

- Docker
- Railway

---

# 📂 Project Structure

```
Medical-Assistant/

│── app/
│── auth/
│── chat/
│── rag/
│── ocr/
│── voice/
│── templates/
│── static/
│── uploads/
│── vectorstore/
│── database/
│── tests/
│── docs/

│── app.py
│── run.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── railway.json
│── README.md
│── .env.example
```

---

# 💻 Usage

1. Open the application in your browser.
2. Register or log in.
3. Ask medical questions using text or voice.
4. Upload a medical report for AI analysis.
5. Review extracted findings and recommendations.
6. Continue follow-up conversations with AI.
7. Manage reports, appointments, and reminders from the dashboard.

---

# 🐳 Docker Deployment

Build the Docker image

```bash
docker build -t medical-assistant .
```

Run the container

```bash
docker run -p 5000:5000 medical-assistant
```

---

# 🚀 Railway Deployment

1. Push the project to GitHub.
2. Connect your repository to Railway.
3. Configure environment variables:

```
NVIDIA_API_KEY

SECRET_KEY

DATABASE_URL
```

4. Deploy the application.

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Includes:

- Unit Tests
- Integration Tests
- OCR Tests
- RAG Tests
- Authentication Tests
- API Tests

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature/YourFeature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature/YourFeature
```

5. Open a Pull Request.

---

# 📬 Contact

**Krishna Rajput**

📧 Email: krishnarajput8362@gmail.com

🔗 GitHub: https://github.com/Krishna270704

🔗 LinkedIn: https://www.linkedin.com/in/krishna-104b6627a

---

# ⭐ Project Repository

https://github.com/Krishna270704/AI-Medical-assistant.git

---

## 🌟 If you found this project useful, don't forget to give it a Star on GitHub

## Deployment to Railway

1. Push this code to a GitHub repository.
2. Create a new project on [Railway](https://railway.app/).
3. Select **Deploy from GitHub repo** and choose your repository.
4. Add all the environment variables listed in .env.example in the Railway dashboard.
5. Railway will automatically detect the Procfile and use Gunicorn to serve the app.
6. The PORT will be automatically injected by Railway.
