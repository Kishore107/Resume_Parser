import spacy
import PyPDF2
import docx
from pathlib import Path
from typing import Dict, List, Union

class ResumeParser:
    def __init__(self):
        # Load spaCy model for NLP tasks
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common skills and keywords to look for
        self.skill_patterns = [
            "python", "java", "javascript", "sql", "aws", "docker",
            "machine learning", "data analysis", "project management"
        ]

    def parse_resume(self, file_path: Union[str, Path]) -> Dict:
        """
        Parse resume file and extract relevant information
        """
        text = self._extract_text(file_path)
        
        return {
            'personal_info': self._extract_personal_info(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'certifications': self._extract_certifications(text)
        }

    def _extract_text(self, file_path: Union[str, Path]) -> str:
        """Extract text from PDF, DOCX, or TXT files"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() == '.docx':
            return self._extract_from_docx(file_path)
        elif file_path.suffix.lower() == '.txt':
            return file_path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def _extract_from_pdf(self, file_path: Path) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _extract_from_docx(self, file_path: Path) -> str:
        doc = docx.Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])

    def _extract_personal_info(self, text: str) -> Dict:
        """Extract name, email, and phone number"""
        doc = self.nlp(text)
        # Basic implementation - can be enhanced with regex patterns
        return {
            'name': self._extract_name(doc),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text)
        }

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP and pattern matching"""
        doc = self.nlp(text.lower())
        skills = []
        
        # Match skills from predefined patterns
        for skill in self.skill_patterns:
            if skill in text.lower():
                skills.append(skill)
                
        return list(set(skills))

    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries"""
        import re
        experiences = []
        
        # Look for date patterns and job titles
        date_pattern = r'(\d{4})\s*-\s*(\d{4}|present)'
        
        # Split text into sections
        sections = text.split('\n\n')
        for section in sections:
            date_match = re.search(date_pattern, section, re.IGNORECASE)
            if date_match:
                experiences.append({
                    'period': date_match.group(0),
                    'description': section.strip(),
                    'company': self._extract_company(section),
                    'title': self._extract_job_title(section)
                })
        
        return experiences

    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        # Common education keywords
        edu_keywords = ["bachelor", "master", "phd", "degree", "university", "college"]
        
        # Split text into sections
        sections = text.split('\n\n')
        for section in sections:
            if any(keyword in section.lower() for keyword in edu_keywords):
                education.append({
                    'degree': self._extract_degree(section),
                    'institution': self._extract_institution(section),
                    'year': self._extract_year(section)
                })
        
        return education

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certification information"""
        # Implementation details to be added
        return []

    def _extract_name(self, doc) -> str:
        """Extract name using NER"""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return ""

    def _extract_email(self, text: str) -> str:
        """Extract email using regex"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else ""

    def _extract_phone(self, text: str) -> str:
        """Extract phone number using regex"""
        import re
        phone_pattern = r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else ""

    def _extract_degree(self, text: str) -> str:
        """
        Extract degree information from education section text
        """
        # Basic degree keywords to look for
        degree_keywords = [
            'B.Tech', 'B.E.', 'Bachelor', 'M.Tech', 'M.E.', 'Master',
            'PhD', 'Diploma', 'HSC', 'SSLC'
        ]
        
        for degree in degree_keywords:
            if degree.lower() in text.lower():
                return degree
        
        return 'Not specified'

    def _extract_institution(self, text: str) -> str:
        """Extract institution name from education section text"""
        # Common education institution keywords
        institution_keywords = ['university', 'college', 'institute', 'school']
        
        # Split text into lines and look for lines containing institution keywords
        for line in text.split('\n'):
            if any(keyword in line.lower() for keyword in institution_keywords):
                return line.strip()
        
        return 'Not specified'

    def _extract_year(self, text: str) -> str:
        """Extract year from education section text"""
        import re
        # Look for year patterns (e.g., 2020, 2015-2019)
        year_pattern = r'(19|20)\d{2}(?:\s*-\s*(19|20)\d{2})?'
        match = re.search(year_pattern, text)
        return match.group(0) if match else 'Not specified'
        