from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_match(self, resume_data: Dict, job_data: Dict) -> Dict:
        """Calculate the match between resume and job description"""
        # Calculate skill match
        skill_score = self._calculate_skill_match(
            resume_data['skills'],
            job_data['required_skills']
        )
        
        # Get missing skills
        missing_skills = self._identify_missing_skills(
            resume_data['skills'],
            job_data['required_skills']
        )
        
        # Generate suggestions based on analysis
        suggestions = self._generate_suggestions(resume_data, job_data)
        
        return {
            'overall_score': skill_score,
            'missing_skills': missing_skills,
            'suggestions': suggestions
        }

    def _calculate_skill_match(self, resume_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill match score"""
        if not required_skills:
            return 1.0
        
        # Convert all skills to lowercase for comparison
        resume_skills = [skill.lower() for skill in resume_skills]
        required_skills = [skill.lower() for skill in required_skills]
        
        matched_skills = set(resume_skills) & set(required_skills)
        return len(matched_skills) / len(required_skills)

    def _identify_missing_skills(self, resume_skills: List[str], required_skills: List[str]) -> List[str]:
        """Identify skills missing from resume"""
        # Convert all skills to lowercase for comparison
        resume_skills = [skill.lower() for skill in resume_skills]
        required_skills = [skill.lower() for skill in required_skills]
        
        # Find missing skills
        missing = set(required_skills) - set(resume_skills)
        return list(missing)

    def _generate_suggestions(self, resume_data: Dict, job_data: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Check for missing skills
        missing_skills = self._identify_missing_skills(
            resume_data['skills'],
            job_data['required_skills']
        )
        
        if missing_skills:
            suggestions.append(
                f"Consider adding these key skills to your resume: {', '.join(missing_skills)}"
            )
        
        # Add suggestion about skill count
        if len(resume_data['skills']) < 5:
            suggestions.append(
                "Your resume could benefit from listing more relevant skills"
            )
        
        # Add suggestion about experience
        if 'experience' in job_data and 'experience' in resume_data:
            if len(resume_data['experience']) < 2:
                suggestions.append(
                    "Consider adding more detailed work experience to your resume"
                )
        
        # If no suggestions were generated, add a positive note
        if not suggestions:
            suggestions.append(
                "Your resume appears to be well-matched with the job requirements"
            )
        
        return suggestions 