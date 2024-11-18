from parser.resume_parser import ResumeParser
from parser.job_parser import JobParser
from analyzer.matcher import ResumeMatcher

def main(resume_path, job_description_path):
    # Initialize parsers
    resume_parser = ResumeParser()
    job_parser = JobParser()
    matcher = ResumeMatcher()
    
    # Parse resume and job description
    resume_data = resume_parser.parse_resume('/Users/kishore/Downloads/J KISHORE KUMAR RESUME.pdf')
    job_data = job_parser.parse_job_description('/Users/kishore/Downloads/file.txt')
    
    # Calculate match and get feedback
    match_results = matcher.calculate_match(resume_data, job_data)
    
    # Print results
    print(f"Overall Match Score: {match_results['overall_score']:.2%}")
    print("\nMissing Skills:")
    for skill in match_results['missing_skills']:
        print(f"- {skill}")
    print("\nSuggestions:")
    for suggestion in match_results['suggestions']:
        print(f"- {suggestion}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <resume_path> <job_description_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2]) 