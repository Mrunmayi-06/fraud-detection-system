# app.py - Main Flask API
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import uuid
from datetime import datetime
import os
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api.log'),
        logging.StreamHandler()
    ]
)

# Load system prompt
PROMPT_FILE = 'system_prompt.txt'
if not os.path.exists(PROMPT_FILE):
    logging.error(f"System prompt file '{PROMPT_FILE}' not found!")
    exit(1)

with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

logging.info("System prompt loaded successfully")

OLLAMA_API = 'http://localhost:11434/api/generate'


def analyze_with_ollama(user_input):
    try:
        logging.info(f"Analyzing input (length: {len(user_input)} chars)")

        response = requests.post(
            OLLAMA_API,
            json={
                "model": "phi3",
                "prompt": SYSTEM_PROMPT + "\n\nUser Input:\n" + user_input,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 512
                }
            },
            timeout=300
        )

        if response.status_code == 200:
            result = response.json()
            content = result["response"]

            logging.info("Response received from Ollama")

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse JSON: {e}")
                    return {
                        "error": "Failed to parse JSON response",
                        "raw_content": content[:500]
                    }
        else:
            logging.error(f"Ollama API error: {response.status_code}")
            return {"error": f"Ollama API error: {response.status_code}"}

    except requests.exceptions.Timeout:
        logging.error("Request timeout")
        return {"error": "Request timeout - analysis took too long"}
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return {"error": str(e)}


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        data = request.json
        user_input = data.get('input', '')
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        # Analyze with Ollama
        result = analyze_with_ollama(user_input)
        
        # Log the analysis
        if 'error' not in result:
            risk_score = result.get('risk_assessment', {}).get('risk_score', 'N/A')
            risk_tier = result.get('risk_assessment', {}).get('risk_tier', 'N/A')
            logging.info(f"Analysis complete - Score: {risk_score}, Tier: {risk_tier}")
        
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"Error in /api/analyze: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    ollama_status = check_ollama_status()
    return jsonify({
        'status': 'healthy' if ollama_status else 'degraded',
        'ollama_running': ollama_status,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get system statistics"""
    try:
        log_file = 'logs/api.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                total_analyses = sum(1 for line in lines if 'Analysis complete' in line)
        else:
            total_analyses = 0
        
        return jsonify({
            'total_analyses': total_analyses,
            'uptime': 'N/A',  # Would need to track start time
            'system_version': 'AMDGFD-TIS v3.0'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def check_ollama_status():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == '__main__':
    print("=" * 60)
    print(" GenAI Fraud Detection API - Starting...")
    print("=" * 60)
    print()
    print(" Checking Ollama status...")
    
    if check_ollama_status():
        print(" Ollama is running")
    else:
        print(" Ollama is not running!")
        print("Please start Ollama with: ollama serve")
        print()
        exit(1)
    
    print()
    print(" System Ready")
    print(" API will be available at: http://localhost:5000")
    print(" Health check: http://localhost:5000/api/health")
    print(" Statistics: http://localhost:5000/api/stats")
    print()
    print("Press CTRL+C to stop")
    print("=" * 60)
    print()
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)