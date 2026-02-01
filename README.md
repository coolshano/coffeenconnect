☕ CoffeeNConnect

AI-powered mentor–mentee matching platform

CoffeeNConnect connects mentees with the right mentors using AI-driven semantic matching and interest-based filtering.
Instead of browsing random profiles, users get ranked, personalized mentor matches.

------------------------------------------------------------------------------------------------------------------------

🌟 Why CoffeeNConnect?

Finding the right mentor is hard.
CoffeeNConnect solves this by combining:

Feature	Benefit
🎯 Interest-based filtering	Psychology mentees see psychology mentors
🧠 AI semantic matching	Matches based on meaning, not keywords
👥 Mentor & Mentee dashboards	Clean, professional UX
📄 CV + profile system	Better credibility & matching
🔐 Secure login & roles	Mentor and Mentee flows separated

-------------------------------------------------------------------------------------------------------------------------

🧠 How Matching Works

CoffeeNConnect uses a two-layer AI matching engine:

1️⃣ Domain Filtering

Users select an Interested Field:

Psychology

Medical

Technology

Mentees are only matched with mentors in the same field.

2️⃣ AI Similarity Scoring

We generate vector embeddings from profile descriptions using:

SentenceTransformer: all-MiniLM-L6-v2

We then compute similarity using cosine similarity:
Similarity(mentee, mentor) = cosine(mentee_embedding, mentor_embedding)
This allows us to match users based on:

-------------------------------------------------------------------------------------------------------------------------


🧭 User Flow
🧑‍🎓 Mentee Journey

Register
Choose Interested Field
Upload CV + Profile
See ranked mentor matches
Send mentorship requests

🧑‍🏫 Mentor Journey

Register
Choose Interested Field
Add experience & CV
Receive mentee requests
Accept / Reject

🖥️ Dashboards
Mentee Dashboard

Profile card (photo, name, country)
Ranked mentor matches
Match percentage
Request button
Mentor Dashboard
Incoming mentee requests
Accept / Reject controls
Mentor profile

🛠️ Tech Stack
Layer	Tech
Backend	Django
Frontend	HTML + CSS
Database	SQLite (can upgrade to Postgres)
AI Engine	SentenceTransformers
Vector Math	NumPy
Auth	Django Auth
File Storage	Django Media

--------------------------------------------------------------------------------------------------------------------------------

🚀 Getting Started
1️⃣ Clone the project git clone https://github.com/yourusername/coffeenconnect.git
cd coffeenconnect

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start server
python manage.py runserver

-------------------------------------------------------------------------------------------------------------------------------

🧪 Sample Accounts

You can create:

Mentor accounts
Mentee accounts
Select the Interested Field during signup to enable matching.

🧠 AI Engine

We use:

SentenceTransformer("all-MiniLM-L6-v2")
Each profile is embedded and stored in the database as a vector.
Matching is instant and scalable.

🧑‍💻 Built By

CoffeeNConnect is built as an AI-first mentorship platform.
This project demonstrates:
AI matching
Multi-role SaaS design
Real-world data modeling
Production-ready architecture

⭐ Future Roadmap

Chat between mentors & mentees
Session booking
Stripe payments
Video calls
Reputation system
Admin analytics
