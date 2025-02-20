from fastapi import FastAPI, File, UploadFile
import uvicorn
from transcriber import transcribe_audio

app = FastAPI()

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    result = transcribe_audio(file)  # Directly passing file
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
