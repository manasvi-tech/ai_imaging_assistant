from google.cloud import documentai_v1 as documentai

def process_scan_with_docai(project_id, location, processor_id, file_path, mime_type):
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )
    name = client.processor_path(project_id, location, processor_id)
    with open(file_path, "rb") as f:
        raw = documentai.RawDocument(content=f.read(), mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw)
    doc = client.process_document(request=request).document
    # Extract text and entities
    text = "".join([page.text for page in doc.pages])
    ents = [(ent.text_anchor.content, ent.type_) for ent in doc.entities]
    return {"text": text, "entities": ents}
