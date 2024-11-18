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
        # This is a basic implementation that can be enhanced
        doc = self.nlp(text)
        experiences = []
        
        # Implementation details to be added
        return experiences

    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        # Implementation details to be added
        return []

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certification information"""
        # Implementation details to be added
        return [] 