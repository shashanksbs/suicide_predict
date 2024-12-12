from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyBkpsEV_aHCMnP24fz3UQeYNC4LkB8ICGY")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/')
def index():
    return send_file('i.html')

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
        text_response = model.generate_content([f"Analyze the following text without providing a description: {user_input}. Include a risk assessment listing Occurring Puside risks%, Not Occurring Puside risks%, and Other Risk Factors%. Conclude with percentages only on the last line."])
        
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
