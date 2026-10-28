## TypeBlitz ⚡
TypeBlitz is a Streamlit-based typing speed game that helps you practise typing, improve accuracy, and track your progress through short timed challenges.
# Features
- Timed typing tests with multiple duration options
- Difficulty levels for different typing challenges
- Typing statistics to review speed and accuracy
- Daily challenge for an extra practice goal
- Sound effects for typing feedback, including a custom sound option for incorrect keys
- Records, badges, and history to make practice more engaging
# Live Demo
Add your deployed Streamlit app URL here.
# Tech Stack
- Python
- Streamlit
- HTML/CSS/JavaScript for in-app interface behaviour and sound effects
# Run Locally
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/TypeBlitz.git
cd TypeBlitz
Replace YOUR-USERNAME with your GitHub username.
2. Create and activate a virtual environment (recommended)
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Start the app
streamlit run app.py
Streamlit will show a local URL in your terminal, usually http://localhost:8501.
# Deployment
TypeBlitz can be deployed using Streamlit Community Cloud:
1. Push this repository to GitHub.
2. Open Streamlit Community Cloud and connect your GitHub account.
3. Create a new app and select this repository, the main branch, and app.py.
4. Deploy the app.
# Project Structure
TypeBlitz/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
# Contributing
Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.
# License
No license has been specified yet. Add a LICENSE file if you want to publish this project under a particular open-source license.
