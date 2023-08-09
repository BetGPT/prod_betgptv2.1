from flask import Flask, render_template, request, jsonify
from chat import chatgpt_completion, get_conversation_context
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    conversation = get_conversation_context()
    conversation.append({'role': 'user', 'content': user_input})
    response = chatgpt_completion(conversation)
    conversation.append({'role': 'assistant', 'content': response})
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
