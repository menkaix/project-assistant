import services.requesters.google_cloud_storage as gs
import os
import vertexai
import json
from vertexai.generative_models import GenerativeModel, Part

def access_pdf(path_in_bucket, history, prompt):

    # TODO(developer): Update and un-comment below lines
    project_id = os.getenv('PROJECT_NAME')

    vertexai.init(project=project_id, location="europe-west1")

    model = GenerativeModel("gemini-1.5-flash-001")
    if path_in_bucket != "":
        data = gs.read_binary(os.getenv("BUCKET_NAME"), path_in_bucket)
        pdf_file = Part.from_data(data, mime_type="application/pdf")
        if history :
            contents = [pdf_file, json.dumps(history), prompt]
        else:
            contents = [pdf_file, prompt]
    else:
        if history :
            contents = [json.dumps(history), prompt]
        else:
            contents = [prompt]
    

    response = model.generate_content(contents)

    return response.text

def chat_with_llm(path_in_bucket, chat_history, user_message):
    """
    Chats with a Large Language Model (LLM), optionally including a PDF context.

    Args:
        project_id: The Google Cloud project ID.
        bucket_name: The name of the Google Cloud Storage bucket (if using a PDF).
        path_in_bucket: The path to the PDF file within the bucket (can be "" or None if no PDF).
        chat_history: A list of dictionaries representing the chat history. Each dictionary should have "role" (user, assistant) and "content" keys.
        user_message: The current user's message.

    Returns:
        A dictionary containing:
        - "history": The updated chat history.
        - "message": The assistant's response.
        - "error": An error message if something went wrong, or None if successful.

    """
    try:

        project_id = os.getenv('PROJECT_NAME')
        bucket_name = os.getenv("BUCKET_NAME")

        vertexai.init(project=project_id, location="europe-west1")  # Assuming Europe-West1
        model = GenerativeModel("gemini-1.5-flash-001")

        contents = []

        if path_in_bucket:  # Handles both "" and None
            try:
                data = gs.read_binary(bucket_name, path_in_bucket)
                pdf_file = Part.from_data(data, mime_type="application/pdf")
                contents.append(pdf_file)
            except Exception as e:
                return {"error": f"Error reading PDF: {e}"}


        if chat_history:
            contents.append(json.dumps(chat_history))

        contents.append(user_message)

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
        return {"error": f"An error occurred: {e}"}


