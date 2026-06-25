from fastapi import FastAPI, UploadFile
import spacy, re, tempfile, os
from PyPDF2 import PdfReader
from docx import Document

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

SKILL_SYNONYMS = {
    "python": ["python","django","flask"],
    "sql": ["sql","mysql","postgres"],
    "ml": ["machine learning","ml","model"],
    "aws": ["aws","cloud"],
    "react": ["react","frontend"]
}

def extract_text(path):
    if path.endswith(".pdf"):
        return " ".join(p.extract_text() or "" for p in PdfReader(path).pages)
    doc = Document(path)
    return " ".join(p.text for p in doc.paragraphs)

@app.post("/parse")
async def parse_resume(file: UploadFile):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(await file.read())
    tmp.close()

    text = extract_text(tmp.name).lower()
    doc = nlp(text)

    skills = set()
    for base, syns in SKILL_SYNONYMS.items():
        if any(s in text for s in syns):
            skills.add(base)

    exp = 0
    for ent in doc.ents:
        if ent.label_ == "DATE":
            nums = re.findall(r"\d+", ent.text)
            if nums:
                exp = max(exp, int(nums[0]))

    os.unlink(tmp.name)
    return {"skills": list(skills), "experience": exp}