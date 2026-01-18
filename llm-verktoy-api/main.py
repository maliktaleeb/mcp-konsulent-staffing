import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="LLM Verktøy API")

# Konfigurasjon
KONSULENT_API_URL = "http://konsulent-api:8000/konsulenter"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def generer_sammendrag_med_llm(konsulenter, ferdighet, min_tilgjengelighet):
    """Bruker GPT-4o-mini via OpenRouter for å lage et menneskelig sammendrag."""
    prompt = (
        f"Lag et kort sammendrag av tilgjengelige konsulenter med ferdigheten '{ferdighet}' "
        f"og minst {min_tilgjengelighet}% tilgjengelighet. Her er dataen: {konsulenter}. "
        "Svaret skal være profesjonelt og på norsk."
    )
    
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {
        "model": "google/gemini-2.0-flash-001", # God balanse mellom hastighet og pris
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=20.0)
        result = response.json()
        return result['choices'][0]['message']['content']

@app.get("/tilgjengelige-konsulenter/sammendrag")
async def hent_sammendrag(min_tilgjengelighet_prosent: int, påkrevd_ferdighet: str):
    async with httpx.AsyncClient() as client:
        try:
            # 1. Hent data fra konsulent-api
            resp = await client.get(KONSULENT_API_URL)
            alle_konsulenter = resp.json()
            
            # 2. Filtrer data basert på kriterier
            filtrert = []
            for k in alle_konsulenter:
                tilgjengelighet = 100 - k["belastning_prosent"]
                if tilgjengelighet >= min_tilgjengelighet_prosent and påkrevd_ferdighet.lower() in [f.lower() for f in k["ferdigheter"]]:
                    k["tilgjengelighet_prosent"] = tilgjengelighet
                    filtrert.append(k)
            
            # 3. Generer sammendrag via LLM
            sammendrag = await generer_sammendrag_med_llm(filtrert, påkrevd_ferdighet, min_tilgjengelighet_prosent)
            
            return {"sammendrag": sammendrag}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))