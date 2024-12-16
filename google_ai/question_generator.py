import json
from typing import List, Dict, Any, Optional
from flask import current_app
from .config import DEFAULT_PRO_MODEL
from .utils import execute_genai_operation
import re

def generate_questions(image_paths: List[str], model_name: str = DEFAULT_PRO_MODEL) -> Optional[List[Dict[str, Any]]]:
    """
    Generate questions based on the provided images using Google's Generative AI.

    Args:
    image_paths (List[str]): List of paths to image files.
    model_name (str): Name of the Gemini model to use. Defaults to the value in config.py.

    Returns:
    Optional[List[Dict[str, Any]]]: List of generated questions with their details, or None if generation failed.
    """
    prompt = """
    * make sure that you analyze all the uploaded images 
    * for each image find the relevant topics 
    * for each topic come up with one or more relevant questions
    * questions and answers MUST come from uploaded images ONLY!
    * if you can not analyze provide information on that 
    * do not stop until you have analyzed all images 
    * provide your results as JSON
    * each json element MUST have the following structure: page_nr, question, answer, difficulty_level
    * difficulty_level should be one of: easy, medium, hard
    * be very careful to provide VALID JSON!
    """

    result = []
    for image_path in image_paths:
        response = execute_genai_operation(
            prompt, file_paths=image_path, mime_type="image/jpeg", model_name=model_name)
                                                                
        if not response or not response.strip():                    # Ako je odgovor prazan ili sadrži samo praznine, logujemo grešku i preskačemo obradu
            current_app.logger.error(f"Empty response received for image: {image_path}")
            continue 
                                                                          
        try:                                                        # Očisti odgovor i parsiraj JSON
            match = re.search(r"\[.*\]", response, re.DOTALL)       # Tražimo JSON blok unutar odgovora pomoću regularnih izraza
            if match: 
                clean_json = match.group(0)                         # Ako je JSON pronađen, izdvajamo ga
                parsed_response = json.loads(clean_json)            # Parsiramo izdvojeni JSON string u Python listu (listu pitanja)
                if not isinstance(parsed_response, list):           # Proveravamo da li je parsirani odgovor zapravo lista (što očekujemo)
                    raise ValueError("Parsed JSON is not a list.")  # Ako nije lista, podižemo grešku
                result.extend(parsed_response)                      # Dodajemo sva pitanja iz parsiranog odgovora u rezultat
            else:
                raise ValueError("JSON block not found in response.")
        except (json.JSONDecodeError, ValueError) as e:
            current_app.logger.error(f"Failed to parse JSON for image {image_path}: {response}. Error: {str(e)}")
            continue                                                # Preskačemo ovu iteraciju i nastavljamo sa sledećom slikom

    return result
  