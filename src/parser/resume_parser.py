import spacy
import PyPDF2
import docx
from pathlib import Path
from typing import Dict, List, Union

class ResumeParser:
    def parse_resume(self, file_path: Union[str, Path]) -> Dict:
        """Parse resume file and extract text"""
        text = self._extract_text(file_path)
        
        return {
            'full_text': text,
            'file_name': Path(file_path).name
        }

    def _extract_text(self, file_path: Union[str, Path]) -> str:
        """Extract text from PDF, DOCX, or TXT files"""
        file_path = Path(file_path)
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_path.suffix.lower() == '.docx':
                return self._extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                return file_path.read_text(encoding='utf-8')
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""

    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text() or '')
                return ' '.join(text)
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return ""

    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return ' '.join(text)
        except Exception as e:
            print(f"Error reading DOCX: {str(e)}")
            return ""
        