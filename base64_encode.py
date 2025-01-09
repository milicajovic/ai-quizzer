import base64
# Putanja do vašeg JSON fajla


def generate_base64_code(): 
    file_path = "C:\\Users\\jovic\\Downloads\\earn-your-screentime-b89397ea23a2.json"   
    # Čitanje sadržaja fajla
    with open(file_path, "rb") as json_file:
        json_bytes = json_file.read()

    # Konverzija u Base64 string
    base64_key = base64.b64encode(json_bytes).decode("utf-8")

    # Štampanje rezultata
    print(base64_key)

# if __name__ == "__main__":
#     generate_base64_code()  