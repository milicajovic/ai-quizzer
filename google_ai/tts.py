import re
from google.cloud import texttospeech
import tempfile
import logging


def replace_unsupported_voices(text: str) -> str:
    """
    Replace all occurrences of unsupported voice names with supported alternatives in the given text.

    Args:
    text (str): The input text containing voice names.

    Returns:
    str: The text with all unsupported voice names replaced by their alternatives.
    """
    voice_replacements = {
        'hr-HR-Standard-A': 'sr-RS-Standard-A',
        # Add more replacements here as needed
    }

    for unsupported, supported in voice_replacements.items():
        text = text.replace(unsupported, supported)

    return text


def generate_speech_from_ssml(ssml_text, quiz):
    """
    Generate speech from SSML text using Google Cloud Text-to-Speech API.

    Args:
    ssml_text (str): The SSML text to convert to speech.

    Returns:
    str: Path to the temporary audio file.

    Raises:
    Exception: If anything goes wrong.
    """
    try:
        # Zameni nepodržane glasove unutar SSML
        ssml_text = replace_unsupported_voices(ssml_text)

        # Izvuci jezik iz SSML (pretpostavimo da je format: <voice name="xx-XX-...">)
        language_code = "en-US"  # Podrazumevani jezik
        match = re.search(r'<voice name="([a-z]{2}-[A-Z]{2})-', ssml_text)
        if match:
            language_code = match.group(1)

        # Postavi glas na osnovu jezika
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Pozovi Google TTS API
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Snimi generisani govor u privremeni fajl
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file.write(response.audio_content)

        return temp_audio_file.name

    except Exception as e:
        logging.error(f"Error in generate_speech_from_ssml: {str(e)}")
        raise