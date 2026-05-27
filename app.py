import os
import subprocess
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

TEMP_DIR = "/tmp/libreoffice_conversions"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/")
async def convert_document(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    try:
        # Save input file to temp path
        input_path = os.path.join(TEMP_DIR, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Build output format conversion command
        # e.g., soffice --headless --convert-to pdf input.docx --outdir /tmp
        cmd = [
            "soffice",
            "--headless",
            "--convert-to",
            target_format,
            input_path,
            "--outdir",
            TEMP_DIR
        ]
        
        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"LibreOffice conversion failed: {result.stderr}")

        # Locate output file
        base_name, _ = os.path.splitext(file.filename)
        output_filename = f"{base_name}.{target_format.lower()}"
        output_path = os.path.join(TEMP_DIR, output_filename)

        if not os.path.exists(output_path):
            # Fallback if LibreOffice changed name casing or character encoding
            raise HTTPException(status_code=500, detail="Converted file could not be generated.")

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
