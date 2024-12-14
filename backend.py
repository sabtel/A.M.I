from flask import Flask, request, jsonify
import pandas as pd
from difflib import SequenceMatcher
from flask_cors import CORS  # Import CORS to handle cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the CSV file into a DataFrame
CSV_FILE_PATH = r"D:\my new file for analyze.csv"  # Update with your file path
data = pd.read_csv(CSV_FILE_PATH)

# Function to calculate similarity between two strings
def calculate_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route('/analyze', methods=['POST'])
def analyze_message():
    try:
        # Debug incoming data
        print("Request received:", request.json)

        # Get the message content
        message_content = request.json.get('message')
        if not message_content:
            return jsonify({'error': 'Message content is missing'}), 400

        # Ensure CSV file exists and has valid content
        if data.empty or 'message' not in data.columns or 'image name' not in data.columns:
            return jsonify({'error': 'CSV file is empty or missing required columns'}), 500

        # Calculate similarity and filter matches
        threshold = 0.7
        results = []
        for _, row in data.iterrows():
            similarity = calculate_similarity(message_content, row['message'])
            if similarity >= threshold:
                results.append({
                    'image_name': row['image name'],
                    'message': row['message'],
                    'similarity': round(similarity * 100, 2)
                })

        # Sort and return results
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return jsonify({'results': results, 'total_matches': len(results)})

    except Exception as e:
        print("Error during analysis:", str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
