# LLM Chatbot

A conversational chatbot built with **LangChain** and **LangGraph**, powered by Google's **Gemini API**. It remembers earlier messages in a conversation and has both a terminal version and a web interface built with **Streamlit**.

## Features
- Conversation memory within a chat session
- Terminal chatbot (`chatbot.py`)
- Web chat interface with a "New chat" button (`app.py`)
- Uses the free tier of the Gemini API

## Tech Stack
- Python 3.12
- LangChain and LangGraph
- Google Gemini (`langchain-google-genai`)
- Streamlit

## Setup

### 1. Clone the repository
```
git clone https://github.com/Hemal1125/LLM-Chatbot.git
cd LLM-Chatbot
```

### 2. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate
```
(On Mac/Linux, use `source venv/bin/activate`.)

### 3. Install the dependencies
```
pip install -r requirements.txt
```

### 4. Add your API key
Get a free key from [Google AI Studio](https://aistudio.google.com/api-keys), then create a file named `.env` in the project folder:
```
GOOGLE_API_KEY=your-key-here
```
Never share this file or upload it to GitHub. It is already listed in `.gitignore`.

## Usage

**Web interface:**
```
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

**Terminal version:**
```
python chatbot.py
```
Type `quit` to exit.

## Project Structure
```
LLM-Chatbot/
├── app.py             # Streamlit web interface
├── chatbot.py         # Terminal chatbot
├── requirements.txt   # Python dependencies
├── .env.example       # Template for the API key file
└── .gitignore         # Keeps secrets and the venv out of Git
```

## Future Improvements
- Streaming responses
- Chat with your own documents (RAG)
- Saving chat history to a database
- Deployment on Streamlit Community Cloud