from flask import Flask, request, jsonify
from vectorize import vectorize_text
from chromadb import save_to_chromadb

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    text = file.read().decode('utf-8')
    vector = vectorize_text(text)
    
    if save_to_chromadb(vector):
        return jsonify({'message': 'File processed and saved successfully'}), 200
    else:
        return jsonify({'error': 'Failed to save to ChromaDB'}), 500

if __name__ == '__main__':
    app.run(debug=True)