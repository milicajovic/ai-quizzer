import os
import base64
import tempfile

# Učitaj Base64 string iz varijable okruženja
BASE64_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")

if BASE64_KEY:
    # Dekodiranje Base64 stringa
    json_bytes = base64.b64decode(BASE64_KEY)

    # Kreiranje privremenog fajla
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(json_bytes)
        temp_file_path = temp_file.name

    # Postavljanje privremene putanje kao GOOGLE_APPLICATION_CREDENTIALS
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_BASE64 is not set")