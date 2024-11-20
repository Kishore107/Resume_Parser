import spacy
from typing import Dict, List, Union
from pathlib import Path

class JobParser:
    def parse_job_description(self, text: Union[str, Path]) -> Dict:
        """Parse job description"""
        if isinstance(text, Path):
            text = text.read_text(encoding='utf-8')
        
        return {
            'full_text': text,
            'file_name': str(text) if isinstance(text, Path) else 'job_description'
        }
  