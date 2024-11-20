from typing import Dict, List, Set
import spacy
import numpy as np
import google.generativeai as genai

class ResumeMatcher:
    def __init__(self, api_key: str = None):
        self.nlp = spacy.load("en_core_web_sm")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
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

        # Extract skills
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
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_text}
        
        Provide:
        1. Experience match score (0-1)
        2. Education match score (0-1)
        3. List of key missing skills by category
        4. Specific improvement suggestions
        
        Format as JSON with keys: experience_match, education_match, skill_gaps_by_category, suggestions
        """

        ai_response = self.model.generate_content(prompt)
        try:
            ai_analysis = eval(ai_response.text)
        except:
            ai_analysis = {
                'experience_match': 0.5,
                'education_match': 0.5,
                'skill_gaps_by_category': {'technical': list(missing_skills)},
                'suggestions': ['Consider adding more specific technical skills']
            }

        # Calculate overall score
        detailed_scores = {
            'skill_match': skill_match_score,
            'experience_match': ai_analysis.get('experience_match', 0.5),
            'education_match': ai_analysis.get('education_match', 0.5),
            'semantic_match': semantic_match
        }
        
        overall_score = np.mean(list(detailed_scores.values()))

        return {
            'overall_score': overall_score,
            'detailed_scores': detailed_scores,
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skill_gaps_by_category': ai_analysis.get('skill_gaps_by_category', {}),
            'suggestions': ai_analysis.get('suggestions', [])
        }