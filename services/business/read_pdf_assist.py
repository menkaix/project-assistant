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
