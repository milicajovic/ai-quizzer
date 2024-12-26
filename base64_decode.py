import os
import base64
import tempfile

def setup_google_credentials():
    BASE64_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")

    if BASE64_KEY:
        json_bytes = base64.b64decode(BASE64_KEY)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(json_bytes)
            temp_file_path = temp_file.name

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path
    else:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_BASE64 is not set")