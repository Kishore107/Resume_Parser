from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
import google.generativeai as genai
import json

class ResumeMatcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')

    def calculate_match(self, resume_data: Dict, job_data: Dict) -> Dict:
        """Calculate the match between resume and job description using Gemini AI"""
        if not self.api_key:
            raise ValueError("API key is required for analysis")

        # Convert resume and job data to text
        resume_text = self._dict_to_text(resume_data)
        job_text = self._dict_to_text(job_data)

        # Create analysis prompt
        prompt = f"""You are a professional resume analyzer. Compare this resume against the job description and provide a detailed analysis.
        
        Resume:
        {resume_text}

        Job Description:
        {job_text}

        Provide your analysis in the following format:
        MATCH_PERCENTAGE: (number between 0-100)
        MISSING_SKILLS: (comma-separated list)
        MISSING_QUALIFICATIONS: (comma-separated list)
        SUGGESTIONS: (one suggestion per line, start each with '-')
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse the response
            analysis = self._parse_gemini_response(response_text)
            
            return {
                'overall_score': analysis['match_percentage'] / 100,
                'detailed_scores': {
                    'skill_match': self._calculate_skill_match_percentage(analysis['missing_skills']),
                    'experience_match': 0.7,
                    'education_match': 0.7,
                    'semantic_match': analysis['match_percentage'] / 100
                },
                'missing_skills': analysis['missing_skills'],
                'skill_gaps_by_category': {'technical': analysis['missing_skills']},
                'suggestions': analysis['suggestions']
            }
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return self._generate_fallback_response()

    def _dict_to_text(self, data: Dict) -> str:
        """Convert dictionary data to formatted text"""
        return '\n'.join(f"{k}: {v}" for k, v in data.items())

    def _calculate_skill_match_percentage(self, missing_skills: List[str]) -> float:
        """Calculate skill match percentage based on missing skills"""
        # Simple calculation - can be enhanced
        return 1.0 if not missing_skills else 0.7

    def _generate_fallback_response(self) -> Dict:
        """Generate a fallback response when API fails"""
        return {
            'overall_score': 0.5,
            'detailed_scores': {
                'skill_match': 0.5,
                'experience_match': 0.5,
                'education_match': 0.5,
                'semantic_match': 0.5
            },
            'missing_skills': ['Unable to analyze skills'],
            'skill_gaps_by_category': {'technical': ['Analysis failed']},
            'suggestions': ['Unable to generate suggestions due to API error']
        }

    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse the formatted response from Gemini"""
        try:
            lines = response_text.split('\n')
            analysis = {
                'match_percentage': 0,
                'missing_skills': [],
                'missing_qualifications': [],
                'suggestions': []
            }
            
            for line in lines:
                line = line.strip()
                if line.startswith('MATCH_PERCENTAGE:'):
                    analysis['match_percentage'] = float(line.split(':')[1].strip())
                elif line.startswith('MISSING_SKILLS:'):
                    skills = line.split(':')[1].strip()
                    analysis['missing_skills'] = [s.strip() for s in skills.split(',') if s.strip()]
                elif line.startswith('MISSING_QUALIFICATIONS:'):
                    quals = line.split(':')[1].strip()
                    analysis['missing_qualifications'] = [q.strip() for q in quals.split(',') if q.strip()]
                elif line.startswith('-'):
                    analysis['suggestions'].append(line[1:].strip())
            
            return analysis
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}")
            raise