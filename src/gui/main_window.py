from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Resume Parser")
        self.setGeometry(100, 100, 600, 400)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Resume upload section
        self.resume_label = QLabel("No resume file selected")
        self.resume_button = QPushButton("Upload Resume")
        self.resume_button.clicked.connect(self.upload_resume)
        layout.addWidget(self.resume_label)
        layout.addWidget(self.resume_button)

        # Add some spacing
        layout.addSpacing(20)

        # Job description upload section
        self.job_label = QLabel("No job description file selected")
        self.job_button = QPushButton("Upload Job Description")
        self.job_button.clicked.connect(self.upload_job)
        layout.addWidget(self.job_label)
        layout.addWidget(self.job_button)

        # Add some spacing
        layout.addSpacing(20)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Match")
        self.analyze_button.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_button)

        # Results label
        self.results_label = QLabel("")
        layout.addWidget(self.results_label)

        # Initialize file paths
        self.resume_path = None
        self.job_path = None

    def upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Resume File",
            "",
            "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;Text Files (*.txt)"
        )
        if file_path:
            self.resume_path = file_path
            self.resume_label.setText(f"Resume selected: {file_path.split('/')[-1]}")

    def upload_job(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Job Description File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if file_path:
            self.job_path = file_path
            self.job_label.setText(f"Job description selected: {file_path.split('/')[-1]}")

    def analyze(self):
        if not self.resume_path or not self.job_path:
            QMessageBox.warning(
                self,
                "Missing Files",
                "Please upload both resume and job description files."
            )
            return

        try:
            from ..parser.resume_parser import ResumeParser
            from ..parser.job_parser import JobParser
            from ..analyzer.matcher import ResumeMatcher

            # Initialize parsers and matcher
            resume_parser = ResumeParser()
            job_parser = JobParser()
            matcher = ResumeMatcher()

            # Parse files
            resume_data = resume_parser.parse_resume(self.resume_path)
            job_data = job_parser.parse_job_description(self.job_path)

            # Get match results
            match_results = matcher.calculate_match(resume_data, job_data)

            # Format results with HTML for better display
            results_text = f"""
            <h3>Match Results</h3>
            <p><b>Overall Score:</b> {match_results['overall_score']:.2%}</p>
            
            <h4>Missing Skills:</h4>
            <ul>
            {"".join(f"<li>{skill}</li>" for skill in match_results['missing_skills'])}
            </ul>

            <h4>Suggestions:</h4>
            <ul>
            {"".join(f"<li>{suggestion}</li>" for suggestion in match_results['suggestions'])}
            </ul>
            """
            
            # Set text with HTML formatting
            self.results_label.setText(results_text)
            self.results_label.setTextFormat(Qt.TextFormat.RichText)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred during analysis: {str(e)}"
            )