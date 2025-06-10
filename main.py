from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

# Configuration
app = FastAPI()
JSON_FILE = "metadata.json"

# Endpoint to get JSON data
@app.get("/get_metadata")
async def get_metadata():
    """
    Retrieves the JSON data from metadata.json in the repository.
    """
    try:
        if not Path(JSON_FILE).exists():
            raise HTTPException(status_code=404, detail="metadata.json file not found")
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "metadata" not in data:
            raise HTTPException(status_code=400, detail="Invalid JSON format: must be an object with a 'metadata' key")
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data in metadata.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving JSON: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Use Railway's PORT or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
