from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                         QLabel, QFileDialog, QMessageBox, QFrame, QScrollArea, QLineEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette
from pathlib import Path

class StyleSheet:
    MAIN_STYLE = """
    QMainWindow {
        background-color: #f5f6fa;
    }
    QLabel {
        color: #2f3542;
        font-size: 14px;
        padding: 10px;
    }
    QPushButton {
        background-color: #546de5;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 14px;
        min-width: 200px;
    }
    QPushButton:hover {
        background-color: #574bd6;
    }
    QPushButton:pressed {
        background-color: #3c40c6;
    }
    QPushButton:disabled {
        background-color: #a4b0be;
    }
    QFrame {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
    }
    """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_key = None
        self.resume_path = None
        self.job_path = None
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Resume Parser")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # API Key section
        api_label = QLabel("Enter Google API Key:")
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_submit = QPushButton("Submit API Key")
        self.api_submit.clicked.connect(self.submit_api_key)
        
        layout.addWidget(api_label)
        layout.addWidget(self.api_input)
        layout.addWidget(self.api_submit)

        # Add spacing
        layout.addSpacing(20)

        # Resume upload section
        self.resume_label = QLabel("No resume file selected")
        self.resume_button = QPushButton("Upload Resume")
        self.resume_button.clicked.connect(self.upload_resume)
        self.resume_button.setEnabled(False)  # Disabled until API key is provided
        layout.addWidget(self.resume_label)
        layout.addWidget(self.resume_button)

        # Add spacing
        layout.addSpacing(20)

        # Job description upload section
        self.job_label = QLabel("No job description file selected")
        self.job_button = QPushButton("Upload Job Description")
        self.job_button.clicked.connect(self.upload_job)
        self.job_button.setEnabled(False)  # Disabled until API key is provided
        layout.addWidget(self.job_label)
        layout.addWidget(self.job_button)

        # Add spacing
        layout.addSpacing(20)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Match")
        self.analyze_button.clicked.connect(self.analyze)
        self.analyze_button.setEnabled(False)  # Disabled until API key is provided
        layout.addWidget(self.analyze_button)

        # Results label
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)

    def submit_api_key(self):
        api_key = self.api_input.text().strip()
        if not api_key:
            QMessageBox.warning(
                self,
                "Invalid API Key",
                "Please enter a valid Google API Key."
            )
            return

        # Here you could add validation of the API key if needed
        self.api_key = api_key
        
        # Enable the upload buttons
        self.resume_button.setEnabled(True)
        self.job_button.setEnabled(True)
        self.analyze_button.setEnabled(True)
        
        QMessageBox.information(
            self,
            "Success",
            "API Key submitted successfully. You can now upload files."
        )

    def upload_resume(self):
        if not self.api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please submit your Google API Key first."
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Resume",
            "",
            "Documents (*.pdf *.docx *.txt)"
        )
        if file_path:
            self.resume_path = file_path
            self.resume_label.setText(f"Resume selected: {Path(file_path).name}")

    def upload_job(self):
        if not self.api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please submit your Google API Key first."
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Job Description",
            "",
            "Documents (*.pdf *.docx *.txt)"
        )
        if file_path:
            self.job_path = file_path
            self.job_label.setText(f"Job description selected: {Path(file_path).name}")

    def analyze(self):
        if not self.api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please submit your Google API Key first."
            )
            return

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

            # Initialize parsers and matcher with API key
            resume_parser = ResumeParser()
            job_parser = JobParser()
            matcher = ResumeMatcher(api_key=self.api_key)  # Pass API key to matcher

            # Parse files
            resume_data = resume_parser.parse_resume(self.resume_path)
            job_data = job_parser.parse_job_description(self.job_path)

            # Get match results
            match_results = matcher.calculate_match(resume_data, job_data)

            # Format results with HTML for better display
            results_text = f"""
            <h3>Match Analysis Results</h3>
            
            <h4>Overall Score: {match_results['overall_score']:.2%}</h4>
            
            <h4>Detailed Scores:</h4>
            <ul>
                <li>Skills Match: {match_results['detailed_scores']['skill_match']:.2%}</li>
                <li>Experience Match: {match_results['detailed_scores']['experience_match']:.2%}</li>
                <li>Education Match: {match_results['detailed_scores']['education_match']:.2%}</li>
                <li>Semantic Match: {match_results['detailed_scores']['semantic_match']:.2%}</li>
            </ul>

            <h4>Skill Gaps by Category:</h4>
            <ul>
            """
            
            for category, skills in match_results['skill_gaps_by_category'].items():
                category_name = category.replace('_', ' ').title()
                results_text += f"<li><b>{category_name}:</b> {', '.join(skills)}</li>"
            
            results_text += """
            </ul>

            <h4>Improvement Suggestions:</h4>
            <ul>
            """
            
            for suggestion in match_results['suggestions']:
                results_text += f"<li>{suggestion}</li>"
            
            results_text += "</ul>"
            
            self.results_label.setText(results_text)
            self.results_label.setTextFormat(Qt.TextFormat.RichText)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred during analysis: {str(e)}"
            )