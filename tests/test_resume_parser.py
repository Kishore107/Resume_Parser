import unittest
from pathlib import Path
from src.parser.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        
    def test_extract_skills(self):
        test_text = "Experienced Python developer with SQL and AWS knowledge"
        skills = self.parser._extract_skills(test_text)
        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("aws", skills) 