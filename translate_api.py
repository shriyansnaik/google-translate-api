from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uvicorn
import os
import time
import uuid
from datetime import datetime

# Import the translation function from our existing script
from google_translate import translate_text, chunk_text

# Language data: name to ISO code mapping
SUPPORTED_LANGUAGES = {
    "Abkhaz": "ab",
    "Acehnese": "ace",
    "Acholi": "ach",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Alur": "alz",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Awadhi": "awa",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Balinese": "ban",
    "Bambara": "bm",
    "Bashkir": "ba",
    "Basque": "eu",
    "Batak Karo": "btx",
    "Batak Simalungun": "bts",
    "Batak Toba": "bbc",
    "Belarusian": "be",
    "Bemba": "bem",
    "Bengali": "bn",
    "Betawi": "bew",
    "Bhojpuri": "bho",
    "Bikol": "bik",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Buryat": "bua",
    "Cantonese": "yue",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa (Nyanja)": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Chuvash": "cv",
    "Corsican": "co",
    "Crimean Tatar": "crh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dinka": "din",
    "Divehi": "dv",
    "Dogri": "doi",
    "Dombe": "dov",
    "Dutch": "nl",
    "Dzongkha": "dz",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Fijian": "fj",
    "Filipino (Tagalog)": "fil",
    "Finnish": "fi",
    "French": "fr",
    "French (French)": "fr-FR",
    "French (Canadian)": "fr-CA",
    "Frisian": "fy",
    "Fulfulde": "ff",
    "Ga": "gaa",
    "Galician": "gl",
    "Ganda (Luganda)": "lg",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hakha Chin": "cnh",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hiligaynon": "hil",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Hunsrik": "hrx",
    "Icelandic": "is",
    "Igbo": "ig",
    "Iloko": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kapampangan": "pam",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kiga": "cgg",
    "Kinyarwanda": "rw",
    "Kituba": "ktu",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish (Kurmanji)": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latgalian": "ltg",
    "Latin": "la",
    "Latvian": "lv",
    "Ligurian": "lij",
    "Limburgan": "li",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Lombard": "lmo",
    "Luo": "luo",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maithili": "mai",
    "Makassar": "mak",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malay (Jawi)": "ms-Arab",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Meadow Mari": "chm",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Minang": "min",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Ndebele (South)": "nr",
    "Nepalbhasa (Newari)": "new",
    "Nepali": "ne",
    "Northern Sotho (Sepedi)": "nso",
    "Norwegian": "no",
    "Nuer": "nus",
    "Occitan": "oc",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Pangasinan": "pag",
    "Papiamento": "pap",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Portuguese (Portugal)": "pt-PT",
    "Portuguese (Brazil)": "pt-BR",
    "Punjabi": "pa",
    "Punjabi (Shahmukhi)": "pa-Arab",
    "Quechua": "qu",
    "Romani": "rom",
    "Romanian": "ro",
    "Rundi": "rn",
    "Russian": "ru",
    "Samoan": "sm",
    "Sango": "sg",
    "Sanskrit": "sa",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Seychellois Creole": "crs",
    "Shan": "shn",
    "Shona": "sn",
    "Sicilian": "scn",
    "Silesian": "szl",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swati": "ss",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Tetum": "tet",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Tswana": "tn",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi (Akan)": "ak",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Yucatec Maya": "yua",
    "Zulu": "zu"
}

app = FastAPI(
    title="Google Translate API",
    description="""
    An API for translating text using Google Translate.
    
    ## Supported Languages
    
    This API supports translation between many languages. Use the `/languages` endpoint 
    to get a complete list of supported languages and their codes.
    
    ## Translation Process
    
    1. Submit text for translation using the `/translate` endpoint
    2. Receive a job ID that you can use to check translation status
    3. Poll the `/translate/{job_id}` endpoint to check if translation is complete
    4. Once complete, the translation result will be available in the response
    
    For large texts, the translation is processed in chunks and may take some time to complete.
    """,
    version="1.0.0"
)

# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for translation jobs
translation_jobs: Dict[str, Dict] = {}

# Define request and response models
class TranslationRequest(BaseModel):
    text: str = Field(..., description="The text to translate")
    source_language: str = Field(default="en", description="Source language code (e.g., 'en' for English)")
    target_language: str = Field(default="hi", description="Target language code (e.g., 'hi' for Hindi)")
    
class TranslationResponse(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the translation job")
    status: str = Field(..., description="Status of the translation job")
    
class TranslationStatus(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the translation job")
    status: str = Field(..., description="Status of the translation job")
    created_at: str = Field(..., description="When the job was created")
    completed_at: Optional[str] = Field(None, description="When the job was completed")
    text_length: int = Field(..., description="Length of the source text")
    chunks: int = Field(..., description="Number of chunks the text was split into")
    result: Optional[str] = Field(None, description="The translation result (if completed)")

class Language(BaseModel):
    name: str = Field(..., description="Full name of the language")
    code: str = Field(..., description="ISO code of the language")

class LanguageList(BaseModel):
    languages: List[Language] = Field(..., description="List of supported languages")
    count: int = Field(..., description="Total number of supported languages")

def perform_translation(job_id: str, text: str, source_lang: str, target_lang: str):
    """Background task to perform translation"""
    try:
        # Update job status to in progress
        translation_jobs[job_id]["status"] = "in_progress"
        
        # Define output file for this job
        output_file = f"translations/{job_id}.txt"
        
        # Perform translation
        result = translate_text(
            text_to_translate=text,
            output_file=output_file,
            source_lang=source_lang,
            target_lang=target_lang
        )
        
        # Update job with success
        translation_jobs[job_id]["status"] = "completed"
        translation_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        translation_jobs[job_id]["result"] = result
        
    except Exception as e:
        # Update job with error
        translation_jobs[job_id]["status"] = "failed"
        translation_jobs[job_id]["error"] = str(e)
        translation_jobs[job_id]["completed_at"] = datetime.now().isoformat()

@app.get("/languages", response_model=LanguageList, tags=["Languages"])
async def get_languages():
    """
    Get a list of all supported languages for translation.
    
    Returns a list of language names and their corresponding codes that can be used
    with the translation endpoints.
    """
    languages = [
        Language(name=name, code=code) for name, code in SUPPORTED_LANGUAGES.items()
    ]
    return LanguageList(languages=languages, count=len(languages))

@app.get("/languages/{language_code}", response_model=Language, tags=["Languages"])
async def get_language(language_code: str):
    """
    Get information about a specific language by its code.
    
    Returns the language name and code if found.
    """
    # Find language by code
    for name, code in SUPPORTED_LANGUAGES.items():
        if code.lower() == language_code.lower():
            return Language(name=name, code=code)
    
    # If not found, raise 404
    raise HTTPException(status_code=404, detail=f"Language with code '{language_code}' not found")

@app.post("/translate", response_model=TranslationResponse, tags=["Translation"])
async def translate(request: TranslationRequest, background_tasks: BackgroundTasks):
    """
    Translate text from one language to another using Google Translate.
    
    This endpoint creates a translation job that runs in the background.
    Returns a job ID that can be used to check the status of the translation.
    
    - **text**: The text to translate
    - **source_language**: Source language code (e.g., 'en' for English)
    - **target_language**: Target language code (e.g., 'hi' for Hindi)
    
    Use the `/languages` endpoint to get a list of all supported language codes.
    """
    # Validate language codes
    source_found = any(code.lower() == request.source_language.lower() for code in SUPPORTED_LANGUAGES.values())
    target_found = any(code.lower() == request.target_language.lower() for code in SUPPORTED_LANGUAGES.values())
    
    if not source_found:
        raise HTTPException(status_code=400, detail=f"Source language '{request.source_language}' not supported")
    if not target_found:
        raise HTTPException(status_code=400, detail=f"Target language '{request.target_language}' not supported")
    
    # Create a unique job ID
    job_id = str(uuid.uuid4())
    
    # Ensure translations directory exists
    os.makedirs("translations", exist_ok=True)
    
    # Calculate chunks
    chunks = chunk_text(request.text, chunk_size=4000)
    
    # Store job information
    translation_jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "text_length": len(request.text),
        "chunks": len(chunks),
        "result": None
    }
    
    # Start translation in background
    background_tasks.add_task(
        perform_translation,
        job_id=job_id,
        text=request.text,
        source_lang=request.source_language,
        target_lang=request.target_language
    )
    
    return TranslationResponse(job_id=job_id, status="pending")

@app.get("/translate/{job_id}", response_model=TranslationStatus, tags=["Translation"])
async def get_translation_status(job_id: str):
    """
    Check the status of a translation job.
    
    Returns the current status and, if completed, the translation result.
    """
    if job_id not in translation_jobs:
        raise HTTPException(status_code=404, detail="Translation job not found")
    
    return TranslationStatus(**translation_jobs[job_id])

@app.get("/translations", response_model=List[TranslationStatus], tags=["Translation"])
async def list_translations():
    """
    List all translation jobs.
    """
    return [TranslationStatus(**job) for job in translation_jobs.values()]

@app.delete("/translate/{job_id}", tags=["Translation"])
async def delete_translation(job_id: str):
    """
    Delete a translation job.
    """
    if job_id not in translation_jobs:
        raise HTTPException(status_code=404, detail="Translation job not found")
    
    # Remove from memory
    job = translation_jobs.pop(job_id)
    
    # Also delete the file if it exists
    try:
        file_path = f"translations/{job_id}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
    
    return {"status": "deleted", "job_id": job_id}

if __name__ == "__main__":
    uvicorn.run("translate_api:app", host="0.0.0.0", port=8080, reload=True) 