import os
import base64
import tempfile

def setup_google_credentials():
    GOOGLE_APPLICATION_CREDENTIALS_BASE64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_BASE64")

    if GOOGLE_APPLICATION_CREDENTIALS_BASE64:
        json_bytes = base64.b64decode(GOOGLE_APPLICATION_CREDENTIALS_BASE64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(json_bytes)
            temp_file_path = temp_file.name

        os.environ["GOOGLE_APPLICATION_CREDENTIALS_BASE64"] = temp_file_path
    else:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_BASE64 is not set")