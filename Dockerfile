FROM python:3.9-slim

# Install LibreOffice and tools
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Copy requirements & app
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
