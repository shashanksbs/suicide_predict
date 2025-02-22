from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import os
import json 

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyAn_9wz5q5etT5_Bgm_aEh4HgMXuzIrrUI")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

JSON_FILE = os.path.join(os.path.dirname(__file__), "info.json")

@app.route('/')
def home():
    return send_file('dashboard.html')

@app.route('/<page>')
def render_page(page):
    if page in ['form', 'i']:
        return send_file(f'{page}.html')
    return "Page not found", 404

@app.route('/predict', methods=['POST'])
def predict_puside():
    try:
        # Ensure you're getting the 'text_prompt' key correctly from the form
        user_input = request.form.get('text_prompt')  
        
        if not user_input:
            return jsonify({
                'status': 'error', 
                'message': 'No text prompt provided.'
            }), 400
        
        # Generate prediction using Gemini
        text_response = model.generate_content([f"Analyze the following text with providing a description: {user_input}. Include a risk assessment listing Occurring Suicide risks%, Not Occurring Suicide risks%, and Other Risk Factors%. Conclude with percentages only on the last line."])
        
        prediction = text_response.text
        
        return jsonify({
            'status': 'success', 
            'prediction': prediction
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)
