from google.cloud import documentai_v1 as documentai
from google.cloud import language_v1
from pathlib import Path
import requests
import os

def process_scan_with_docai(project_id, location, processor_id, file_path, mime_type="image/jpeg"):
    client = documentai.DocumentProcessorServiceClient()
    processor_path = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = {
        "name": processor_path,
        "raw_document": {
            "content": image_content,
            "mime_type": mime_type
        }
    }

    result = client.process_document(request=request)
    document = result.document

    return {"text": document.text}

def extract_medical_entities(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_entities(document=document)
    entities = [{"name": e.name, "type": e.type_.name, "salience": e.salience} for e in response.entities]
    return entities
