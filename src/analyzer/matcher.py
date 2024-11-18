from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_match(self, resume_data: Dict, job_data: Dict) -> Dict:
        """
        Calculate match score between resume and job description
        """
        # Calculate different aspect scores
        skill_score = self._calculate_skill_match(
            resume_data['skills'],
            job_data['required_skills']
        )
        
        qualification_score = self._calculate_qualification_match(
            resume_data['education'],
            job_data['qualifications']
        )
        
        experience_score = self._calculate_experience_match(
            resume_data['experience'],
            job_data['experience']
        )

        # Calculate overall score
        overall_score = (skill_score * 0.5 + 
                        qualification_score * 0.3 + 
                        experience_score * 0.2)

        return {
            'overall_score': overall_score,
            'skill_score': skill_score,
            'qualification_score': qualification_score,
            'experience_score': experience_score,
            'missing_skills': self._identify_missing_skills(
                resume_data['skills'],
                job_data['required_skills']
            ),
            'suggestions': self._generate_suggestions(
                resume_data,
                job_data
            )
        }

    def _calculate_skill_match(self, resume_skills: List[str], 
                             required_skills: List[str]) -> float:
        """Calculate skill match score"""
        if not required_skills:
            return 1.0
            
        matched_skills = set(resume_skills) & set(required_skills)
        return len(matched_skills) / len(required_skills)

    def _calculate_qualification_match(self, resume_quals: List[Dict],
                                    required_quals: List[str]) -> float:
        """Calculate qualification match score"""
        # Implementation details to be added
        return 0.0

    def _calculate_experience_match(self, resume_exp: List[Dict],
                                  required_exp: Dict) -> float:
        """Calculate experience match score"""
        # Implementation details to be added
        return 0.0

    def _identify_missing_skills(self, resume_skills: List[str],
                               required_skills: List[str]) -> List[str]:
        """Identify skills missing from resume"""
        return list(set(required_skills) - set(resume_skills))

    def _generate_suggestions(self, resume_data: Dict,
                            job_data: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Add missing skills suggestion
        missing_skills = self._identify_missing_skills(
            resume_data['skills'],
            job_data['required_skills']
        )
        if missing_skills:
            suggestions.append(
                f"Consider adding these missing skills: {', '.join(missing_skills)}"
            )
            
        # Add more specific suggestions based on other criteria
        return suggestions 