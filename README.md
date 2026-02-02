🚀 ConnectMe – AI-Powered Mentor–Mentee Matching Platform

ConnectMe is a smart web platform that connects mentees with the most relevant mentors using AI-based profile matching.
It analyzes user profiles and matches them using natural-language embeddings and cosine similarity.

🌟 Features
👤 Authentication

User registration & login
Mentor / Mentee role selection
Password change inside dashboard
Secure authentication

🧑‍🎓 Mentee

Create & edit profile
Select interested field (Psychology, Medical, Technology)
Upload profile photo and CV
View AI-generated mentor matches
Send mentor requests

🧑‍🏫 Mentor

Create professional mentor profile
Set interested field
Upload profile photo, LinkedIn, GitHub, CV
Get matched with relevant mentees

🤖 AI Matching Engine

Uses SentenceTransformer (MiniLM-L6-v2)
Generates vector embeddings from profile text
Uses cosine similarity to rank mentors
Filters mentors by interested field

🧠 How Matching Works

Mentee profile text → AI embedding
Mentor profile text → AI embedding
Similarity is calculated:
cosine(mentee_embedding, mentor_embedding)
Results are sorted by similarity
Scores are shown as percentages in the dashboard

🛠️ Technology Stack
Layer	Technology
Backend	Django 6
Frontend	HTML, CSS
AI	SentenceTransformers, NumPy
Database	SQLite
Auth	Django Auth
Media	Django File Uploads

⚙️ Installation
1️⃣ Clone the project
git clone https://github.com/yourusername/connectme.git
cd connectme

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver


Open: http://127.0.0.1:8000

🔐 Password Management

Users can change their password inside their dashboard.

🧪 Test Matching Engine
python manage.py shell

from core.models import Mentee
from core.ml import match_mentors

m = Mentee.objects.first()
match_mentors(m)

🚀 Future Enhancements

Chat between mentors and mentees

Video calls
Appointment scheduling
Reviews & ratings
Subscription system
Mobile app

👨‍💻 Developed By

Shannon Smith
AI-Driven Mentorship Platform