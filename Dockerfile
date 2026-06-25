# ---------- Base Image ----------
FROM python:3.10-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- Working Directory ----------
WORKDIR /app

# ---------- Install Python Dependencies ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Download spaCy Model ----------
RUN python -m spacy download en_core_web_sm

# ---------- Copy Application Code ----------
COPY . .

# ---------- Expose Streamlit Port ----------
EXPOSE 8501

# ---------- Run Application ----------
CMD ["streamlit", "run", "app.py"]
