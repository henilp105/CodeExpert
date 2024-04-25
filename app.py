import streamlit as st
from pymongo import MongoClient
from gridfs import GridFS
import time
import markdown2

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://21bce095:Abcdxyz@cluster0.jlybbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["db_test"]
fs = GridFS(db)

def markdown_to_text(markdown_string):
    html_content = markdown2.markdown(markdown_string)
    return html_content

def upload_zip(file, prompt):
    file_data = file.read()
        
    # Save the file data to GridFS with metadata
    object_id = fs.put(file_data, filename=file.name, prompt=prompt, flag="False")
    time.sleep(30)

    # Check if flag is true for the uploaded file
    uploaded_file = fs.find_one({"_id": object_id, "flag": "True"})
    while not uploaded_file:
        time.sleep(10)
        uploaded_file = fs.find_one({"_id": object_id, "flag": "True"})

    st.success(markdown_to_text(uploaded_file.response))

def main():
    st.title("CodeExpert")

    uploaded_file = st.file_uploader("Upload a Zip File", type="zip")
    prompt = st.text_input("Enter a prompt")

    if st.button("Upload"):
        if uploaded_file is not None and prompt:
            with st.spinner("Storing files..."):
                upload_zip(uploaded_file, prompt)

if __name__ == "__main__":
    main()