import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")

    QDRANT_API_KEY=os.getenv("QDRANT_API_KEY") 
    QDRANT_URL=os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_COLLECTION_NAME="Enterprise_RAG"

    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    GROQ_FALLBACK_API_KEY=os.getenv("GROQ_FALLBACK_API_KEY")
    GROQ_MODEL="llama-3.3-70b-versatile"

    PORTKEY_API_KEY=os.getenv("PORTKEY_API_KEY") # we have added this line by ourself
    GROQ_SLUG=os.getenv("GROQ_SLUG") # we have added this line by ourself
    GROQ_SLUG_2=os.getenv("GROQ_SLUG_2") # we have added this line by ourself

settings = Settings()  #object of Settings class to get and set values globally

