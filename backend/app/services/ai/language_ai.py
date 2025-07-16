from google.cloud import language_v1

def extract_medical_entities(text):
    client = language_v1.LanguageServiceClient()
    doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(request={"document": doc}).entities
    return [
        {"name": e.name, "type": e.type_.name, "salience": e.salience}
        for e in entities
    ]
