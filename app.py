import os
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, origins=["https://itamartati.github.io", "http://localhost:5173"])

@app.route('/gemini-generate-intro', methods=['POST'])
def gemini_generate_intro():
    data = request.get_json()

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not provided'}), 500

    request_body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
            headers={'Content-Type': 'application/json'},
            json=request_body
        )

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to gemini generate intro'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500

@app.route('/chatgpt-generate-intro', methods=['POST'])
def chatgpt_generate_intro():
    data = request.get_json()

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    openai_api_key = os.getenv('CHATGPT_API_KEY')
    if not openai_api_key:
        return jsonify({'error': 'API key not provided'}), 500

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    request_body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            response_json = response.json()
            intro_text = response_json.get('choices', [])[0].get('message', {}).get('content', 'No content')
            return jsonify({'intro': intro_text}), 200
        else:
            return jsonify({'error': f"Failed to generate intro with ChatGPT: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500
    
@app.route('/claude-generate-intro', methods=['POST'])
def claude_generate_intro():
    data = request.get_json()

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    claude_api_key = os.getenv('CLAUDE_API_KEY')
    if not claude_api_key:
        return jsonify({'error': 'API key not provided'}), 500

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": claude_api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    request_body = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            response_json = response.json()
            intro_text = response_json.get('completion', 'No content')
            return jsonify({'intro': intro_text}), 200
        else:
            return jsonify({'error': f"Failed to generate intro with Claude: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500

@app.route('/huggingface-generate-intro', methods=['POST'])
def huggingface_generate_intro():
    data = request.get_json()

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not huggingface_api_key:
        return jsonify({'error': 'API key not provided'}), 500

    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}",
        "Content-Type": "application/json"
    }
    request_body = {
        "inputs": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            response_json = response.json()
            intro_text = response_json[0].get('generated_text', 'No content')
            return jsonify({'intro': intro_text}), 200
        else:
            return jsonify({'error': f"Failed to generate intro with Hugging Face: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)