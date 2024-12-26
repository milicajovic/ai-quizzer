import os
import base64
import tempfile
from google.oauth2 import service_account

def setup_google_credentials():
    
    base64_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")

    if not base64_credentials:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_BASE64 has no value.")

    try:
        # Dekodiraj Base64 string
        json_bytes = base64.b64decode(base64_credentials)
        json_string = json_bytes.decode("utf-8")

        # Kreiraj privremeni fajl za kredencijale
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(json_bytes)
            temp_file_path = temp_file.name

        # Postavi putanju na privremeni fajl u varijablu okruženja
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

        # Test: učitaj kredencijale
        credentials = service_account.Credentials.from_service_account_file(temp_file_path)
        # print("Kredencijali su uspešno učitani.")

    except Exception as e:
        print(f"Greška prilikom obrade kredencijala: {e}")
