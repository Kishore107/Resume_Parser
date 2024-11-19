from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
from collections import defaultdict
import re

class ResumeMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Enhanced skill categories with weights and aliases
        self.skill_categories = {
            'programming_languages': {
                'weight': 0.25,
                'skills': {
                    'python': ['py', 'python3'],
                    'java': ['java8', 'java11', 'jvm'],
                    'javascript': ['js', 'es6', 'ecmascript'],
                    'c++': ['cpp', 'c plus plus'],
                    'ruby': ['rb', 'ruby on rails'],
                    'php': ['php7', 'php8'],
                    'swift': ['swift3', 'swift5'],
                    'kotlin': ['kt']
                }
            },
            'frameworks': {
                'weight': 0.20,
                'skills': {
                    'django': ['django rest framework', 'drf'],
                    'flask': ['flask-restful'],
                    'spring': ['spring boot', 'spring mvc'],
                    'react': ['react.js', 'reactjs'],
                    'angular': ['angular2+', 'angularjs'],
                    'vue': ['vue.js', 'vuejs'],
                    'express': ['express.js', 'node.js']
                }
            },
            'databases': {
                'weight': 0.15,
                'skills': {
                    'sql': ['mysql', 'postgresql', 'sql server'],
                    'mongodb': ['mongo', 'nosql'],
                    'oracle': ['pl/sql', 'oracle db'],
                    'redis': ['redis cache']
                }
            },
            'cloud_services': {
                'weight': 0.25,
                'skills': {
                    'aws': ['amazon web services', 'ec2', 's3', 'lambda'],
                    'azure': ['microsoft azure', 'azure cloud'],
                    'gcp': ['google cloud', 'google cloud platform'],
                    'docker': ['containerization', 'docker-compose'],
                    'kubernetes': ['k8s', 'container orchestration']
                }
            },
            'soft_skills': {
                'weight': 0.15,
                'skills': {
                    'leadership': ['team lead', 'project lead', 'management'],
                    'communication': ['interpersonal', 'presentation'],
                    'teamwork': ['collaboration', 'team player'],
                    'problem solving': ['analytical', 'critical thinking'],
                    'agile': ['scrum', 'kanban', 'sprint']
                }
            }
        }

    def calculate_match(self, resume_data: Dict, job_data: Dict) -> Dict:
        # Calculate various scores with weights
        skill_scores = self._calculate_detailed_skill_match(
            resume_data.get('skills', []),
            job_data.get('required_skills', [])
        )
        
        experience_score = self._calculate_experience_match(
            resume_data.get('experience', []),
            job_data.get('experience_requirements', {})
        )
        
        education_score = self._calculate_education_match(
            resume_data.get('education', []),
            job_data.get('education_requirements', [])
        )
        
        semantic_score = self._calculate_semantic_similarity(resume_data, job_data)
        
        # Calculate weighted category scores
        category_scores = {}
        total_weight = 0
        for category, details in self.skill_categories.items():
            weight = details['weight']
            if category in skill_scores:
                category_scores[category] = skill_scores[category] * weight
                total_weight += weight

        # Normalize category scores
        overall_skill_score = sum(category_scores.values()) / total_weight if total_weight > 0 else 0

        # Final weighted score calculation
        weights = {
            'skills': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'semantic': 0.1
        }
        
        overall_score = (
            overall_skill_score * weights['skills'] +
            experience_score * weights['experience'] +
            education_score * weights['education'] +
            semantic_score * weights['semantic']
        )

        return {
            'overall_score': overall_score,
            'detailed_scores': {
                'skill_match': overall_skill_score,
                'skill_category_scores': category_scores,
                'experience_match': experience_score,
                'education_match': education_score,
                'semantic_match': semantic_score
            },
            'missing_skills': self._identify_critical_missing_skills(
                resume_data.get('skills', []),
                job_data.get('required_skills', [])
            ),
            'skill_gaps_by_category': self._analyze_skill_gaps(
                resume_data.get('skills', []),
                job_data.get('required_skills', [])
            ),
            'suggestions': self._generate_advanced_suggestions(
                resume_data, job_data, category_scores
            )
        }

    def _calculate_detailed_skill_match(self, resume_skills: List[str], required_skills: List[str]) -> Dict[str, float]:
        scores = {}
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        for category, details in self.skill_categories.items():
            category_skills = set()
            required_category_skills = set()
            
            # Check each skill and its aliases in the category
            for main_skill, aliases in details['skills'].items():
                # Check resume skills
                if any(alias in resume_skills_lower for alias in [main_skill] + aliases):
                    category_skills.add(main_skill)
                
                # Check required skills
                if any(alias in required_skills_lower for alias in [main_skill] + aliases):
                    required_category_skills.add(main_skill)
            
            # Calculate score for this category
            if required_category_skills:
                matching_skills = category_skills.intersection(required_category_skills)
                scores[category] = len(matching_skills) / len(required_category_skills)
            else:
                scores[category] = 1.0
        
        return scores

    def _identify_critical_missing_skills(self, resume_skills: List[str], required_skills: List[str]) -> List[Dict[str, str]]:
        missing_skills = []
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        
        for skill in required_skills:
            skill_lower = skill.lower()
            found = False
            
            # Check each category for the skill and its aliases
            for category, details in self.skill_categories.items():
                for main_skill, aliases in details['skills'].items():
                    if skill_lower in [main_skill] + aliases and \
                       not any(alias in resume_skills_lower for alias in [main_skill] + aliases):
                        missing_skills.append({
                            'skill': skill,
                            'category': category,
                            'importance': 'Critical' if details['weight'] >= 0.2 else 'Recommended'
                        })
                        found = True
                        break
                if found:
                    break
                    
        return missing_skills

    def _generate_advanced_suggestions(self, resume_data: Dict, job_data: Dict, category_scores: Dict) -> List[str]:
        suggestions = []
        
        # Analyze skill gaps by category
        for category, score in category_scores.items():
            if score < 0.6:
                suggestions.append(f"Focus on improving {category.replace('_', ' ')} skills")
                
        # Experience-based suggestions
        exp_match = self._calculate_experience_match(
            resume_data.get('experience', []),
            job_data.get('experience_requirements', {})
        )
        if exp_match < 0.7:
            suggestions.append("Consider highlighting more relevant work experience")
            
        # Education suggestions
        edu_match = self._calculate_education_match(
            resume_data.get('education', []),
            job_data.get('education_requirements', [])
        )
        if edu_match < 0.7:
            suggestions.append("Consider additional certifications or training")
            
        # Add specific skill suggestions
        missing_skills = self._identify_critical_missing_skills(
            resume_data.get('skills', []),
            job_data.get('required_skills', [])
        )
        if missing_skills:
            critical_skills = [s['skill'] for s in missing_skills if s['importance'] == 'Critical']
            if critical_skills:
                suggestions.append(f"Priority: Add these critical skills: {', '.join(critical_skills)}")
                
        return suggestions

    def _calculate_semantic_similarity(self, resume_data: Dict, job_data: Dict) -> float:
        """Calculate semantic similarity using TF-IDF and cosine similarity"""
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # Combine relevant text from resume and job
        resume_text = ' '.join(str(value) for value in resume_data.values())
        job_text = ' '.join(str(value) for value in job_data.values())
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            return 0.0

    def _analyze_skill_gaps(self, resume_skills: List[str], required_skills: List[str]) -> Dict:
        """Analyze skill gaps by category"""
        resume_skills = set(skill.lower() for skill in resume_skills)
        required_skills = set(skill.lower() for skill in required_skills)
        
        gaps_by_category = {}
        for category, details in self.skill_categories.items():
            # Get all skills and aliases for this category
            category_skills = set()
            for main_skill, aliases in details['skills'].items():
                if any(skill in required_skills for skill in [main_skill] + aliases):
                    category_skills.add(main_skill)
            
            # Find missing skills in this category
            missing_in_category = category_skills - resume_skills
            if missing_in_category:
                gaps_by_category[category] = list(missing_in_category)
        
        return gaps_by_category

    def _calculate_experience_match(self, resume_exp: List[Dict], required_exp: Dict) -> float:
        """Calculate experience match considering years and relevance"""
        if not required_exp or not resume_exp:
            return 0.5
        
        required_years = required_exp.get('years', 0)
        total_relevant_years = sum(
            exp.get('years', 0) for exp in resume_exp 
            if self._is_experience_relevant(exp, required_exp)
        )
        
        if required_years == 0:
            return 1.0
        return min(total_relevant_years / required_years, 1.0)

    def _is_experience_relevant(self, exp: Dict, required_exp: Dict) -> bool:
        """Check if experience is relevant to job requirements"""
        exp_text = ' '.join(str(value) for value in exp.values()).lower()
        required_text = ' '.join(str(value) for value in required_exp.values()).lower()
        
        # Use spaCy for better text comparison
        exp_doc = self.nlp(exp_text)
        req_doc = self.nlp(required_text)
        
        return exp_doc.similarity(req_doc) > 0.3

    def _calculate_education_match(self, resume_edu: List[Dict], required_edu: List[str]) -> float:
        """Calculate education match score"""
        if not required_edu:
            return 1.0
            
        education_levels = {
            'high school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5
        }
        
        # Get highest education level from resume
        resume_level = 0
        for edu in resume_edu:
            edu_text = edu.get('degree', '').lower()
            for level, value in education_levels.items():
                if level in edu_text:
                    resume_level = max(resume_level, value)
        
        # Get required education level
        required_level = 0
        for req in required_edu:
            req_text = req.lower()
            for level, value in education_levels.items():
                if level in req_text:
                    required_level = max(required_level, value)
        
        if required_level == 0:
            return 1.0
        return min(resume_level / required_level, 1.0)

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