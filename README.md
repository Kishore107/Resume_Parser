# Resume Parser

**Resume Parser** is an intelligent application that extracts, processes, and organizes information from resumes. This tool is designed to help recruiters and hiring managers streamline the resume analysis process by providing structured data for better decision-making.

## Features

- Extracts essential details such as:
  - Candidate's name
  - Contact information
  - Education background
  - Work experience
  - Skills and certifications
- Supports resumes in various formats (PDF, DOCX, etc.)
- Utilizes Natural Language Processing (NLP) for accurate data extraction.
- User-friendly interface for uploading resumes and viewing parsed results.
- Generates JSON outputs for easy integration with other platforms.

## Technologies Used

- **Programming Language**: Python
- **Frameworks and Libraries**:
  - Flask (for the web interface)
  - Spacy (for NLP tasks)
  - PyPDF2 and python-docx (for document parsing)
  - Pandas (for structured data manipulation)
- **Deployment**: Dockerized for easy scalability and compatibility.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kishore107/Resume_Parser.git
   cd Resume_Parser


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
