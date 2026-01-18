from fastapi import FastAPI

app = FastAPI(title="Konsulent API")

@app.get("/konsulenter")
def hent_konsulenter():
    return [
        {
            "id": 1,
            "navn": "Anna K.",
            "ferdigheter": ["python", "fastapi", "docker"],
            "belastning_prosent": 40
        },
        {
            "id": 2,
            "navn": "Leo T.",
            "ferdigheter": ["java", "spring", "docker"],
            "belastning_prosent": 20
        },
        {
            "id": 3,
            "navn": "Sara M.",
            "ferdigheter": ["python", "data", "ml"],
            "belastning_prosent": 70
        }
    ]
