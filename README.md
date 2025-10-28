# Gutenberg Text Cleaner

A Flask web service to clean and analyze text from Project Gutenberg books.  
Includes a web interface to input URLs, view text statistics, a 500-character preview, and a 3-sentence summary.

---

## Features

- Clean and normalize Project Gutenberg text
- Compute text statistics (characters, words, sentences, averages)
- Generate a 3-sentence summary
- Web interface for easy URL input and results display
- Simple API endpoints for integration

---

## Setup Instructions

1. **Clone the repository**


git clone <repository-url>
cd scaffolding3_startup
Create and activate a virtual environment (recommended)

bash
Copy code
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the Flask app

bash
Copy code
python app.py
Open in your browser

Go to http://localhost:5000 to access the web interface.

Screenshots of working application : 

<img width="3420" height="2214" alt="image" src="https://github.com/user-attachments/assets/125188ae-2fe1-4e10-9b56-0f098c66eddd" />

<img width="3420" height="2214" alt="image" src="https://github.com/user-attachments/assets/c2185f5f-3f18-421e-981e-599ad31af2db" />
