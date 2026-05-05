import os
import json
import traceback
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from sentence_transformers import SentenceTransformer
import webbrowser
from threading import Timer
from dotenv import load_dotenv

# Internal project modules
from models.person import Person
from nlp.wiki_client import WikiClient
from sorting.factory import SortingFactory
from core.history_manager import HistoryManager

# Server configuration and global constants
SERVER_IP = "http://127.0.0.1:8000"

app = FastAPI()

# Enable CORS for local development and frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


# Initialize AI Client and local NLP components
client_ai = genai.Client(api_key=api_key)
model = SentenceTransformer('all-MiniLM-L6-v2')
wiki = WikiClient()
factory = SortingFactory()
history_manager = HistoryManager()


@app.get("/sort")
async def sort_character(name: str, universe: str, user_id: str = "guest"):
    """
    Core sorting endpoint. Handles data retrieval, AI processing,
    and provides a local NLP fallback if the AI service fails.
    """
    try:
        # Step 1: Check if character exists in user history (MongoDB)
        person = await history_manager.get_cached_person(user_id, name)

        if not person:
            # Step 2: If not in history, fetch biography from Wikipedia
            person = Person(name)
            success = wiki.fetch_person_data(person)
            if not success:
                return {"Error": "Character not found!"}

        # Step 3: Return cached result if already sorted for this universe
        if universe in person.world_assignments:
            saved_data = person.world_assignments[universe]
            GEMINI_API_KEY = api_key
            if isinstance(saved_data, dict):
                return {
                    "name": person.name,
                    "house": saved_data["house"],
                    "reason": saved_data["reason"]
                }
            else:
                return {
                    "name": person.name,
                    "house": saved_data,
                    "reason": "Retrieved from your history (original reason not saved)."
                }

        # Step 4: Primary Sorting Method - Generative AI
        house = None  # Initialize to avoid UnboundLocalError
        reason = ""

        try:
            prompt_text = f"""
            Sort {person.name} into a {universe} house/nation, only one of the 4 respected houses/ nations.
            Summary: {person.summary[:1000]}
            Return ONLY JSON: {{"house": "name", "reason": "why"}}
            """

            response = client_ai.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=prompt_text
            )

            text_response = response.text.strip()

            # Clean potential Markdown formatting from AI response
            if "```json" in text_response:
                text_response = text_response.split("```json")[1].split("```")[0]
            elif "```" in text_response:
                text_response = text_response.split("```")[1].split("```")[0]

                # Parse JSON and assign values outside the conditional blocks to ensure availability
            ai_data = json.loads(text_response.strip())
            house = ai_data['house']
            reason = ai_data['reason']

        except Exception as ai_error:
            # Step 5: Graceful Degradation - Fallback to local NLP
            # Triggered if Gemini API is unavailable or returns an error
            print(f"--- AI FALLBACK TRIGGERED: {type(ai_error).__name__} ---")

            # Use SentenceTransformer to generate a local vector embedding
            person_vector = model.encode(person.summary)

            # Select appropriate strategy via Factory and perform vector sorting
            strategy = factory.get_strategy(universe, model)
            house = strategy.sort(person_vector)
            reason = (f"Sorted using local vector similarity due to high AI demand. "
                      f"{person.name} matches the core traits of {house}.")

        # Step 6: Save the result to history and return to user
        if house:
            person.world_assignments[universe] = {
                "house": house,
                "reason": reason
            }
            await history_manager.save_person(user_id, person)

            return {
                "name": person.name,
                "house": house,
                "reason": reason
            }

        return {"Error": "Sorting failed."}

    except Exception as e:
        # Final safety net for critical system errors
        print(f"--- CRITICAL SERVER ERROR ---")
        traceback.print_exc()
        return {"Error": "The Sorting Hat is confused. Please try again."}


# Static file serving configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(current_dir, "static")

if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")


def open_browser():
    """Utility to open the browser automatically upon server launch."""
    webbrowser.open_new(SERVER_IP)


if __name__ == "__main__":
    import uvicorn

    # Delay browser opening slightly to ensure the server is ready
    Timer(1, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)