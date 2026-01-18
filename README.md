# MCP Konsulent-Staffing Løsning

Dette prosjektet demonstrerer en mikrotjenestearkitektur basert på Model Context Protocol (MCP) for å administrere og oppsummere konsulenttilgjengelighet ved bruk av en LLM.

## Arkitektur
Løsningen består av to uavhengige tjenester bygget med FastAPI:

* **konsulent-api**: En server som fungerer som datakilde og returnerer en liste over konsulenter med detaljer om navn, ferdigheter og nåværende belastning.
* **llm-verktoy-api**: En klient-tjeneste som fungerer som orkestrator. Den henter data fra serveren, filtrerer basert på spesifiserte krav, og sender informasjonen til OpenRouter for å generere et menneskelig sammendrag.

## Slik kjører du prosjektet lokalt

Løsningen er fullstendig containerisert med Docker for enkel distribusjon.

### Forutsetninger
* Docker og Docker Compose installert på din maskin.

### 1. Klon prosjektet
Kjør denne kommandoen i din terminal:

git clone https://github.com/maliktaleeb/mcp-konsulent-staffing.git

### 2. Gå inn i prosjektmappen
cd mcp-konsulent-staffing

### 3. Start med Docker Compose
Sørg for at Docker kjører, og skriv:

docker compose up --build

Dette vil:
1. Bygge begge API-tjenestene basert på Python 3.11-slim.
2. Installere nødvendige avhengigheter (fastapi, uvicorn, httpx).
3. Starte 'konsulent-api' på port 8001.
4. Starte 'llm-verktoy-api' på port 8002.

## Testing av API-et

Når tjenestene kjører, kan du teste hovedfunksjonaliteten via Swagger UI:

* URL: http://localhost:8002/docs
* Endepunkt: GET /tilgjengelige-konsulenter/sammendrag

### Parametre du kan teste med:
* min_tilgjengelighet_prosent: f.eks. 50
* påkrevd_ferdighet: f.eks. python

Systemet beregner tilgjengelighet (100 minus belastning) og finner de konsulentene som matcher dine krav før de oppsummeres av AI-modellen.

## Teknisk Stabel
* Backend: FastAPI
* HTTP Klient: Httpx (asynkron)
* Containerisering: Docker & Docker Compose
* LLM: GPT-4o-mini via OpenRouter