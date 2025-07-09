# 🚀 LangGraph Flask Frontend with Mistral (via Ollama)

Build intelligent, real-time conversational agents using **LangGraph**, integrated with the **Mistral 7B model via Ollama**, all wrapped in a beautiful and responsive **Flask web frontend**.

---

## 📁 Project Structure

langgraph_flask_app/
├── app.py # Main Flask app (backend)
├── your_agent_file.py # LangGraph agent logic
├── templates/
│ └── index.html # Main chat interface
├── static/
│ ├── css/
│ │ └── style.css # Optional: styling
│ └── js/
│ └── app.js # Optional: frontend logic
├── requirements.txt # Project dependencies
└── README.md # Documentation (this file)

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Dependencies

Create `requirements.txt`:
```txt
Flask==2.3.3
langchain-community==0.0.38
langgraph==0.1.14
typing-extensions==4.8.0
Then install:

bash
Copy
Edit
pip install -r requirements.txt
2. 🧠 Prepare Your Agent
Save your agent code (from paste.txt) as your_agent_file.py.

Start Mistral via Ollama:

bash
Copy
Edit
ollama run mistral
3. 📥 Import Your Agent in Flask
In app.py, update:

python
Copy
Edit
from your_agent_file import create_agent_graph
4. 💻 Launch the Web App
Make sure templates/index.html exists.

Then run:

bash
Copy
Edit
python app.py
Visit 👉 http://localhost:5000

🌐 API Endpoints
Endpoint	Method	Description
/api/chat	POST	Send message to agent
/api/history	GET	Retrieve session conversation history
/api/clear	POST	Clear current session history
/api/stats	GET	Get agent usage statistics

✨ Features
🎨 Frontend
💬 Real-time Chat UI

📊 Visual routing of agent decisions

🧠 Session-aware interface

📱 Mobile responsive

⚠️ Friendly error handling

🧩 Backend
🔁 Stateless API with session handling

📈 Agent stats tracking

🧠 LangGraph-based logic routing

🔒 Graceful error recovery

🧪 Usage Examples
Use Case	Example Query
Math Solver	Calculate 15 + 25 * 3
Summarization	Summarize quantum computing
Language Translation	Translate 'Hello world' to French
General QA	What is the capital of France?

🎨 Customization
🖌️ UI
Edit templates/index.html and static/css/style.css

⚙️ Agent Behavior
Modify logic in your_agent_file.py

Add nodes/routes based on your needs

🧩 Extra Features
User authentication

File upload (PDF/QnA support)

Database-based history & analytics

Live socket-based chat (WebSockets)

🚑 Troubleshooting
Issue	Solution
ImportError	Check file name & path of agent module
Ollama not running	Run ollama run mistral before launch
Port 5000 in use	Change port in app.py
Template missing	Ensure templates/index.html exists

🚀 Production Deployment
For live environments:

Use gunicorn:

bash
Copy
Edit
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Add:

Logging

CSRF protection

SSL/HTTPS

Persistent DB

❤️ Credits
Powered by:

LangGraph

LangChain Community

Ollama

Mistral 7B

📬 Connect
For issues, suggestions, or collaborations — feel free to raise an issue or reach out!

🧠 Empowering non-linear intelligent workflows with intuitive UI — one agent at a time.
