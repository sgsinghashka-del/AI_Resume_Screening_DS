**🧠 Enterprise ATS – AI-Powered Resume Screening System**

An AI-enabled Applicant Tracking System (ATS) built with Streamlit, designed to automate resume screening, skill matching, and recruitment pipeline management.

This project demonstrates a production-ready MVP with clean UI, NLP-based resume parsing, and a structured hiring workflow.

**🚀 Features**
**🔐 Role-based Login System**
Admin, HR, Recruiter, Client roles
📄 Resume Upload (PDF / DOCX)

**🧠 NLP-based Skill Extraction**
Powered by spaCy

**📊 Automated Match Scoring**
Role vs Candidate skill matching

**🗂️ Recruitment Pipeline**
Applied → Shortlisted → Interview → Offer
**⚖️ Compliance / Bias Audit View**
**📤 Shortlist Export**
**💾 SQLite Database (Lightweight & Fast)**

**🛠️ Tech Stack**
Layer	Technology
Frontend	Streamlit
Backend	Python
NLP	spaCy
Database	SQLite
File Parsing	PyPDF2, python-docx
Deployment	Docker
**📁 Project Structure**
.
├── app.py              # Main Streamlit application
├── ats.db              # SQLite database (auto-created if missing)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

**⚙️ Installation (Local)**
1️⃣ Clone the Repository
git clone https://github.com/your-username/enterprise-ats.git
cd enterprise-ats

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

4️⃣ Run the Application
streamlit run app.py

Open your browser at:

http://localhost:8501

**🔐 Demo Login Credentials**
Role	Email	Password
Admin	admin@company.com	admin123
HR	hr@company.com	hr123
Recruiter	recruiter@company.com	rec123
Client	demo@client.com	demo

**📊 How Matching Works**
Resume text is extracted (PDF/DOCX)
NLP engine identifies known skills
Skills are matched against role requirements
Match Score (%) is calculated automatically
Candidate progresses through pipeline stages

**🧠 Architecture Notes**
Designed as a Streamlit monolith MVP
Ready for future refactor into:
Microservices (FastAPI)
External NLP service
RBAC enforcement module
Optimized for clarity, speed, and demo readiness

**📌 Future Enhancements**
🔑 OAuth / SSO Authentication
📈 Advanced Analytics Dashboard
🤖 LLM-based Resume Understanding
🧪 Automated Interview Scoring
☁️ Cloud Deployment (AWS / Azure / GCP)

👩‍💻 Author
Ashka Singh




This project is licensed under the MIT License.

⭐ If you like this project, give it a star on GitHub!
