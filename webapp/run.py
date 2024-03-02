from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from gridfs import GridFS
import os
import threading
import time
from bson.objectid import ObjectId
import markdown2
from bs4 import BeautifulSoup

app = Flask(__name__)

def markdown_to_text(markdown_string):
    # html_content = markdown2.markdown(markdown_string)
    # Convert HTML to plain text by removing HTML tags
    html_content = markdown2.markdown(markdown_string)
    return html_content

@app.route('/')
def index():
    return render_template('index.html')

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://21bce095:Abcdxyz@cluster0.jlybbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["db_test"]
fs = GridFS(db)

# Modify the upload_file function to introduce a 30-second delay
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    prompt = request.form['prompt']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Read file contents
        file_data = file.read()
        
        # Save the file data to GridFS with metadata
        object_id = fs.put(file_data, filename=file.filename, prompt=prompt, flag="False")
       
        # Introduce a 30-second delay
        time.sleep(30)
        
        # Check if flag is true for the uploaded file
        uploaded_file = fs.find_one({"_id": object_id, "flag": "True"})
        # print(uploaded_file)
        while not uploaded_file:
            time.sleep(10)
            uploaded_file = fs.find_one({"_id": object_id, "flag": "True"})
            # print(uploaded_file)
        # print(uploaded_file)

        
        # return uploaded_file.response
        return render_template('index.html',message=markdown_to_text(uploaded_file.response))

# Start the flag checking thread before running the Flask app
if __name__ == '__main__':
    # start_flag_check_thread()
    app.run(debug=True)