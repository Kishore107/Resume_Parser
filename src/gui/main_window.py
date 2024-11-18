from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                         QLabel, QFileDialog, QMessageBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette

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
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Resume Parser")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Create header
        header_label = QLabel("Resume Parser")
        header_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2f3542;
            padding: 20px;
        """)
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Create upload section frame
        upload_frame = QFrame()
        upload_layout = QVBoxLayout(upload_frame)
        
        # Resume upload section
        self.resume_label = QLabel("📄 No resume file selected")
        self.resume_button = QPushButton("Upload Resume")
        self.resume_button.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon))
        upload_layout.addWidget(self.resume_label)
        upload_layout.addWidget(self.resume_button)

        # Add some spacing
        upload_layout.addSpacing(20)

        # Job description upload section
        self.job_label = QLabel("📋 No job description file selected")
        self.job_button = QPushButton("Upload Job Description")
        self.job_button.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon))
        upload_layout.addWidget(self.job_label)
        upload_layout.addWidget(self.job_button)

        layout.addWidget(upload_frame)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Match")
        self.analyze_button.setStyleSheet("""
            background-color: #2ecc71;
            font-weight: bold;
        """)
        layout.addWidget(self.analyze_button)

        # Create results frame with scroll area
        results_frame = QFrame()
        results_layout = QVBoxLayout(results_frame)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        results_widget = QWidget()
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        """)
        
        results_widget_layout = QVBoxLayout(results_widget)
        results_widget_layout.addWidget(self.results_label)
        scroll_area.setWidget(results_widget)
        results_layout.addWidget(scroll_area)
        
        layout.addWidget(results_frame)

        # Connect buttons
        self.resume_button.clicked.connect(self.upload_resume)
        self.job_button.clicked.connect(self.upload_job)
        self.analyze_button.clicked.connect(self.analyze)

        # Initialize file paths
        self.resume_path = None
        self.job_path = None
        
        # Initially disable analyze button
        self.analyze_button.setEnabled(False)

    def upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Resume File",
            "",
            "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;Text Files (*.txt)"
        )
        if file_path:
            self.resume_path = file_path
            self.resume_label.setText(f"📄 Resume selected: {file_path.split('/')[-1]}")
            self._update_analyze_button()

    def upload_job(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Job Description File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if file_path:
            self.job_path = file_path
            self.job_label.setText(f"📋 Job description selected: {file_path.split('/')[-1]}")
            self._update_analyze_button()

    def _update_analyze_button(self):
        """Enable analyze button only when both files are selected"""
        self.analyze_button.setEnabled(bool(self.resume_path and self.job_path))

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
            <div style='background-color: white; padding: 20px; border-radius: 10px;'>
                <h2 style='color: #2f3542;'>Match Results</h2>
                <div style='background-color: {'#2ecc71' if match_results['overall_score'] > 0.7 else '#e74c3c'}; 
                          color: white; 
                          padding: 10px; 
                          border-radius: 5px;
                          margin: 10px 0;'>
                    <h3>Overall Score: {match_results['overall_score']:.2%}</h3>
                </div>
                
                <h3 style='color: #2f3542; margin-top: 20px;'>Missing Skills:</h3>
                <ul style='color: #e74c3c;'>
                {"".join(f"<li>{skill}</li>" for skill in match_results['missing_skills'])}
                </ul>

                <h3 style='color: #2f3542; margin-top: 20px;'>Suggestions:</h3>
                <ul style='color: #546de5;'>
                {"".join(f"<li>{suggestion}</li>" for suggestion in match_results['suggestions'])}
                </ul>
            </div>
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