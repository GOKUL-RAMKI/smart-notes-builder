from google import genai
from google.genai import types

from services.config_service import load_api_key

MODEL_NAME = "gemini-2.5-flash-lite"


def process_notes(images: list[dict]) -> str:

    api_key = load_api_key()

    if not api_key:
        raise ValueError(
            "Please configure Gemini API Key in Settings."
        )

    client = genai.Client(api_key=api_key)

    prompt = """
        You are processing handwritten student lecture notes.

        Instructions:

        1. Read all visible text from all images.
        2. Combine information from all images.
        3. Remove duplicate content.
        4. Fix spelling mistakes.
        5. Improve formatting and readability.
        6. Preserve technical terminology exactly.
        7. Create proper headings and subheadings.
        8. Convert handwritten bullet points into structured notes.
        9. Convert tables into readable text when possible.
        10. Do not add information that is not present in the notes.

        Output format:

        # Topic

        ## Subtopic

        - Point 1
        - Point 2

        Return only the cleaned notes.
        """

    parts = [
        types.Part.from_text(text=prompt)
    ]

    for image in images:

        parts.append(
            types.Part.from_bytes(
                data=image["bytes"],
                mime_type=image["mime_type"]
            )
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=parts
    )

    return response.text


def test_connection() -> str:
    api_key = load_api_key()

    if not api_key:
        raise ValueError(
            "Please configure Gemini API Key in Settings."
        )

    try:
        client = genai.Client(api_key=api_key)

        print("Sending request...")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with exactly: Gemini connection successful"
        )

    except Exception as e:
        if "503" in str(e):
            raise Exception(
                "Gemini is currently busy. Try again in a few minutes."
            )

        raise

    print(response.text)

    return response.text.strip()