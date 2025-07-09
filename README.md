# Agent_Task_LangGraph_Mistral

# LangGraph Flask Frontend

## Project Structure

```
langgraph_flask_app/
├── app.py                 # Main Flask application
├── your_agent_file.py     # Your LangGraph agent code (paste.txt content)
├── templates/
│   └── index.html        # HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Optional: separate CSS file
│   └── js/
│       └── app.js        # Optional: separate JavaScript file
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

### 1. Install Dependencies

Create a `requirements.txt` file:

```txt
Flask==2.3.3
langchain-community==0.0.38
langgraph==0.1.14
typing-extensions==4.8.0
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Agent File

1. Save your LangGraph agent code (from paste.txt) as `your_agent_file.py` in the same directory as `app.py`
2. Make sure Ollama is running with the Mistral model:
   ```bash
   ollama run mistral
   ```

### 3. Update Import Path

In `app.py`, update the import line:
```python
from your_agent_file import create_agent_graph  # Replace with your actual file name
```

### 4. Create Templates Directory

Create a `templates` directory and save the HTML template as `templates/index.html`

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Features

### Frontend Features
- **Modern Chat Interface**: Clean, responsive design with smooth animations
- **Real-time Communication**: Instant message exchange with the LangGraph agent
- **Route Visualization**: Shows which nodes your query was routed through
- **Session Management**: Maintains conversation history per session
- **Mobile Responsive**: Works well on desktop and mobile devices
- **Error Handling**: Graceful error messages for failed requests

### Backend Features
- **RESTful API**: Clean API endpoints for chat, history, and stats
- **Session Management**: Tracks conversations per user session
- **Error Handling**: Comprehensive error handling for agent failures
- **Statistics**: Tracks usage statistics across sessions
- **History Management**: Stores and retrieves conversation history

## API Endpoints

### POST /api/chat
Send a message to the LangGraph agent
- **Request**: `{"message": "your question here"}`
- **Response**: `{"message": "agent response", "route_history": [], "timestamp": "..."}`

### GET /api/history
Get conversation history for current session
- **Response**: Array of conversation objects

### POST /api/clear
Clear conversation history for current session
- **Response**: `{"message": "History cleared"}`

### GET /api/stats
Get agent statistics
- **Response**: `{"total_sessions": 0, "total_messages": 0, "available_nodes": []}`

## Usage Examples

The interface supports various types of queries that will be automatically routed to the appropriate agent:

1. **Math Problems**: "Calculate 15 + 25 * 3"
2. **Summarization**: "Summarize quantum computing"
3. **Translation**: "Translate 'Hello world' to French"
4. **General Questions**: "What is the capital of France?"

## Customization

### Styling
- Modify the CSS in the `<style>` section of `index.html`
- Or create separate CSS files in `static/css/`

### Agent Configuration
- Modify the routing logic in your agent file
- Add new node types and update the frontend accordingly
- Adjust the LLM model or parameters in the agent configuration

### Additional Features
- Add authentication/authorization
- Implement database storage for conversation history
- Add file upload capabilities
- Implement real-time notifications

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure your agent file is named correctly and in the same directory
2. **Ollama Connection**: Ensure Ollama is running and the Mistral model is available
3. **Port Already in Use**: Change the port in `app.py` if 5000 is already in use
4. **Template Not Found**: Ensure the `templates` directory exists and contains `index.html`

### Debug Mode
The Flask app runs in debug mode by default. Turn off for production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (gunicorn, uWSGI)
- Setting up proper logging
- Using a database for conversation storage
- Implementing proper session management
- Adding security headers and CSRF protection
- Setting up SSL/TLS certificates

Example with gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
