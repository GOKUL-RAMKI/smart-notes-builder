from google import genai
from google.genai import types

from services.config_service import (load_api_key,load_model)


def process_notes(images: list[dict]) -> str:
    model_name = load_model()

    api_key = load_api_key()

    if not api_key:
        raise ValueError(
            "Please configure Gemini API Key in Settings."
        )

    client = genai.Client(api_key=api_key)

    prompt = """
        You are an expert academic note transcriber and formatter.

        Your task is to convert one or more images of handwritten or printed lecture notes into clean, well-structured study notes.

        Rules:

        1. Read ALL images before generating the final notes.
        2. Combine information from all images into a single coherent document.
        3. Remove duplicate content.
        4. Correct obvious spelling mistakes.
        5. Preserve technical terms, formulas, code snippets, variable names, keywords, and definitions exactly when identifiable.
        6. Do NOT invent information that is not visible in the notes.
        7. If a word is unclear, make the best reasonable interpretation.
        8. If text is completely unreadable, write:
        [Unreadable Text]
        9. Maintain the logical order of the original notes.
        10. Expand poorly formatted bullet lists into clean structured notes.
        11. Convert rough handwritten abbreviations into complete readable sentences when the meaning is obvious.
        12. Preserve examples, formulas, definitions, and important observations.
        13. Convert tables into readable bullet points when necessary.
        14. If a table is present in the notes:
            - Preserve the table structure whenever possible.
            - Represent the table using Markdown table formatting.
            - Ensure rows and columns remain aligned correctly.
            - Preserve column headers exactly as written.
            - Do not convert tables into paragraphs unless the table is unreadable.
        15. If a diagram, flowchart, architecture diagram, graph, UML diagram, network diagram, or sketch is present:

            * Create a section titled:

            ## Diagram Description
            * Describe the diagram in simple points.
            * Mention relationships, arrows, components, and flow directions when visible.

        Formatting Rules:

        * Use Markdown.
        * Use one H1 title for the main topic.
        * Use H2 headings for major sections.
        * Use H3 headings for subsections when needed.
        * Use bullet points for lists.
        * Use numbered lists for procedures.
        * Keep spacing clean and consistent.
        * Do not include explanations about the OCR process.
        * Do not include phrases such as:
        "Based on the image"
        "The notes appear to say"
        "I can see"

        Output Structure:

        # Main Topic

        ## Section

        * Important Point

        * Important Point

        ### Subsection

        * Detail

        ## Definitions

        * Definition

        ## Examples

        * Example

        ## Diagram Description

        * Description of identified diagrams

        Return ONLY the final cleaned notes in Markdown format.

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

    try:

        response = client.models.generate_content(
            model=model_name,
            contents=parts
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:
            raise ValueError(
                "Error 429: Gemini rate limit exceeded for "+model_name+"."
            )
        
        if "503" in error_message:
            raise ValueError(
                "Error 503: Gemini is currently busy. Please try again later."
            )

        if "401" in error_message:
            raise ValueError(
                "Error 401: Invalid Gemini API key. Check Settings."
            )

        raise ValueError(
            f"Gemini error: {error_message}"
        )

def test_connection() -> str:
    model_name = load_model()
    api_key = load_api_key()

    if not api_key:
        raise ValueError(
            "Please configure Gemini API Key in Settings."
        )

    try:
        client = genai.Client(api_key=api_key)

        print("Sending request...")

        response = client.models.generate_content(
            model=model_name,
            contents="Reply with exactly: Gemini connection successful"
        )

    except Exception as e:
    
        error_message = str(e)
    
        if "429" in error_message:
            raise ValueError(
                "Error 429: Gemini rate limit exceeded for "+model_name+"."
            )
            
        if "503" in error_message:
            raise ValueError(
                    "Error 503: Gemini is currently busy. Please try again later."
                )
    
        if "401" in error_message:
            raise ValueError(
                    "Error 401: Invalid Gemini API key. Check Settings."
                )
    
        raise ValueError(
                f"Gemini error: {error_message}"
            )
    print(response.text)

    return response.text.strip()