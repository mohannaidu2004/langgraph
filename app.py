from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import uuid
import os
import sys

# Import your LangGraph agent
from agent_graph import create_agent_graph  # Replace with your actual file name

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize the agent
agent_app = create_agent_graph()

# Store conversation history (in production, use a database)
conversations = {}

@app.route('/')
def index():
    """Main page with chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and route through LangGraph agent"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get or create session ID
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            conversations[session_id] = []
        
        # Process through LangGraph agent
        result = agent_app.invoke({"input": user_input})
        
        # Extract relevant information from result
        response = {
            'message': result.get('result', 'No response generated'),
            'route_history': result.get('route_history', []),
            'timestamp': result.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            'session_id': session_id
        }
        
        # Store in conversation history
        conversations[session_id].append({
            'user_input': user_input,
            'agent_response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Agent processing error: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Get conversation history for current session"""
    session_id = session.get('session_id')
    if session_id and session_id in conversations:
        return jsonify(conversations[session_id])
    return jsonify([])

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history for current session"""
    session_id = session.get('session_id')
    if session_id and session_id in conversations:
        conversations[session_id] = []
    return jsonify({'message': 'History cleared'})

@app.route('/api/stats')
def get_stats():
    """Get agent statistics"""
    total_sessions = len(conversations)
    total_messages = sum(len(conv) for conv in conversations.values())
    
    return jsonify({
        'total_sessions': total_sessions,
        'total_messages': total_messages,
        'available_nodes': ['router', 'math', 'summarizer', 'translator', 'fallback', 'final']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)