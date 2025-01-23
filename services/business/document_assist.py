import services.requesters.google_cloud_storage as gs
import os
import vertexai
import json
import logging
from vertexai.generative_models import GenerativeModel, Part
from mimetypes import guess_type
import services.requesters.consume_backlog_api as backlog_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_file_content(bucket_name, file_path):
    """
    Retrieves the content of a file from Google Cloud Storage and processes it based on its MIME type.

    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        file_path (str): The path to the file within the bucket.

    Returns:
        str or Part: The processed content of the file. The type of the return value depends on the MIME type of the file.

    Raises:
        Exception: If there is an error reading the file.
    """
    try:
        # Read the binary data from the specified bucket and file path
        data = gs.read_binary(bucket_name, file_path)
        
        # Guess the MIME type of the file
        mime_type, _ = guess_type(file_path)
        
        # Process the file content based on its MIME type
        if mime_type == "application/pdf":
            return Part.from_data(data, mime_type=mime_type)
        elif mime_type == "application/json":
            json_data = json.loads(data)
            return json.dumps(json_data, indent=2)
        elif mime_type in ["application/xml", "text/xml"]:
            return data.decode('utf-8')
        elif mime_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            # Currently not processing Word documents
            return None
        elif mime_type in ["image/png", "image/jpeg", "image/gif"]:
            return Part.from_data(data, mime_type=mime_type)
        else:
            # Default case for other text-based files
            return data.decode('utf-8')
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise

def configure_model():
    
    system_instructions = """
        Tu es un assistant Business Analyst, ton rôle est d'expliquer les besoins métiers, les besoins utilisateurs et les éléments techniques de façon claire et concise.
    """
    # model_name = "gemini-1.5-flash-001"
    # region = "europe-west1"
    model_name = "gemini-2.0-flash-exp"
    region = "us-central1"
    
    project_id = os.getenv('PROJECT_NAME')


    # Initialize Vertex AI
    vertexai.init(project=project_id, location=region)
    return GenerativeModel(
        model_name, 
        system_instruction=system_instructions)

def extract_bucket_and_blob(file_path):
    if file_path.startswith("gs://"):
        return file_path[5:].split("/", 1)
    return os.getenv("BUCKET_NAME"), file_path

def prepare_contents(file_paths, prompt=None, chat_history=None):
    
    contents = []

    if file_paths :
        
        file_paths_array = file_paths.split(";")

        for file_path in file_paths_array :
            
            bucket_name, blob_name = extract_bucket_and_blob(file_path.strip())
            contents.append(os.path.basename(blob_name))
            contents.append(get_file_content(bucket_name, blob_name))

    if chat_history:
        contents.append(json.dumps(chat_history))
    if prompt:
        contents.append(prompt)
    return contents

def access_file(file_path, prompt):
    try:
        model = configure_model()
        # bucket_name, blob_name = extract_bucket_and_blob(file_path)
        contents = prepare_contents(file_path, prompt=prompt)
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        logger.error(f"Error in access_file: {e}")
        return {"error": f"An error occurred: {e}"}

def chat_with_llm(file_paths, chat_history, user_message):
    
    """
    Chats with a Large Language Model (LLM), optionally including a PDF context.

    Args:
        project_id: The Google Cloud project ID.
        bucket_name: The name of the Google Cloud Storage bucket (if using a PDF).
        file_path: The path to the PDF file within the bucket (can be "" or None if no PDF).
        chat_history: A list of dictionaries representing the chat history. Each dictionary should have "role" (user, assistant) and "content" keys.
        user_message: The current user's message.

    Returns:
        A dictionary containing:
        - "history": The updated chat history.
        - "message": The assistant's response.
        - "error": An error message if something went wrong, or None if successful.

    """

    try:

        contents = prepare_contents(file_paths, chat_history=chat_history)

        contents.append(user_message)

        model = configure_model()
        response = model.generate_content(contents)

        assistant_message = {
            "role": "assistant",
            "content": response.text
        }

        chat_history.append({"role": "user", "content": user_message})
        chat_history.append(assistant_message)

        return {
            "history": chat_history,
            "message": assistant_message,
            "error": None,
        }

    except Exception as e:
        logger.error(f"An error occurred in chat_with_llm: {e}")
        return {"error": f"An error occurred: {e}"}
