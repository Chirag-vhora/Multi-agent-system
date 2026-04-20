from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI


# ---------------- Gemini Model ----------------
def get_gemini():

    return ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=1.0,
    )


# ---------------- Mistral Model ----------------
def get_mistral():

    return ChatMistralAI(
        model="mistral-small-2506",
        temperature=1.0,
    )


# ---------------- Active Provider ----------------
USE_PROVIDER = "gemini"
# change to "mistral" anytime


# ---------------- Final Export ----------------
if USE_PROVIDER == "gemini":
    llm = get_gemini()
else:
    llm = get_mistral()