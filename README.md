# Resume Parser

An intelligent Resume Parser application that helps job seekers optimize their resumes by comparing them against job descriptions. The application provides a user-friendly GUI interface and detailed analysis of resume-job matches.

## Features

- **Document Support**: Parse resumes in multiple formats (PDF, DOCX, TXT)
- **Skill Analysis**: Identify and extract skills from both resumes and job descriptions
- **Match Scoring**: Calculate compatibility scores between resumes and job requirements
- **Missing Skills**: Highlight skills required by the job but missing from the resume
- **Smart Suggestions**: Receive personalized recommendations for resume improvement
- **User-Friendly Interface**: Easy-to-use GUI for file uploads and result visualization

## Installation

1. Clone the repository:


git clone https://github.com/yourusername/resume-parser.git


2. Create and activate a virtual environment:


python -m venv venv

source venv/bin/activate # Linux/Mac

.\venv\Scripts\activate   # Windows

3. Install dependencies:

pip install -r requirements.txt

python -m spacy download en_core_web_sm

## Usage

1. Launch the application:


python src/main.py


## Analysis Features

The application provides:
- Overall match score
- Detailed scoring breakdown:
  - Skills Match
  - Experience Match
  - Education Match
  - Semantic Match
- Missing skills by category
- Personalized improvement suggestions

## Requirements

- Python 3.9+
- spaCy
- PyQt6
- Google Gemini API access
- Other dependencies listed in requirements.txt

## Project Structure

```
resume_parser/
├── src/
│   ├── analyzer/
│   │   └── matcher.py      # Core matching logic
│   ├── parser/
│   │   ├── resume_parser.py    # Resume parsing
│   │   └── job_parser.py       # Job description parsing
│   ├── gui/
│   │   └── main_window.py      # GUI implementation
│   └── main.py                 # Application entry point
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- spaCy for NLP capabilities
- Google Gemini for AI analysis
- PyQt6 for the GUI framework

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- spaCy for NLP capabilities
- Google Gemini for AI analysis
- PyQt6 for the GUI framework

from typing import Dict, List, Set

import spacy


import google.generativeai as genai



class ResumeMatcher:

    def __init__(self, api_key: str = None):

        self.nlp = spacy.load("en_core_web_sm")

        if api_key:

            genai.configure(api_key=api_key)

            self.model = genai.GenerativeModel('gemini-pro')

        


        """Calculate similarity between two texts using spaCy"""

        doc1 = self.nlp(text1.lower())

        doc2 = self.nlp(text2.lower())

        return doc1.similarity(doc2)



    def _extract_skills(self, text: str) -> Set[str]:

        """Extract skills from text"""

        doc = self.nlp(text.lower())

        # Simple skill extraction based on noun chunks

        skills = {chunk.text for chunk in doc.noun_chunks}

        return skills



    def calculate_match(self, resume_data: Dict, job_data: Dict) -> Dict:

        """Calculate match between resume and job description"""

        resume_text = resume_data.get('full_text', '').lower()

        job_text = job_data.get('full_text', '').lower()




        resume_skills = self._extract_skills(resume_text)

        job_skills = self._extract_skills(job_text)

        

        # Calculate skill match

        matching_skills = resume_skills.intersection(job_skills)

        missing_skills = job_skills - resume_skills

        skill_match_score = len(matching_skills) / len(job_skills) if job_skills else 0



        # Calculate semantic similarity

        semantic_match = self._calculate_text_similarity(resume_text, job_text)



        # Use AI to analyze experience and education match

        prompt = f"""

        Analyze the match between this resume and job description:

And the main GUI implementation shown in:

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                         QLabel, QFileDialog, QMessageBox, QFrame, QScrollArea, QLineEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette
from pathlib import Path

class StyleSheet:
    MAIN_STYLE = """
    QMainWindow {
        background-color: #f5f6fa;
    }
    QLabel {
        color: #2f3542;
        font-size: 14px;
        padding: 10px;
    }
    QPushButton {
        background-color: #546de5;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 14px;
        min-width: 200px;
    }
    QPushButton:hover {
        background-color: #574bd6;
    }
    QPushButton:pressed {
        background-color: #3c40c6;
    }
    QPushButton:disabled {
        background-color: #a4b0be;
    }
    QFrame {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
    }
    """

