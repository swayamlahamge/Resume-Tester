# Resume Tester

An AI-powered resume analyzer that compares your resume against job descriptions and provides actionable feedback to improve your chances of getting hired.

## Features

- **PDF Resume Upload** - Upload your resume as a PDF file
- **Job Description Analysis** - Paste the job description you're targeting
- **Keyword Matching** - See which keywords from the job description are in your resume
- **Match Score** - Get a percentage score showing how well your resume aligns with the job
- **Actionable Recommendations** - Receive specific suggestions to improve your resume
- **ATS Compatibility Check** - Ensure your resume passes Applicant Tracking Systems
- **100% Free** - No APIs, no paid services, completely offline (except for the PDF parsing)

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **PDF Parsing**: pdfplumber
- **NLP**: NLTK

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**
   ```bash
   cd "resume tester"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask backend server**
   ```bash
   python app.py
   ```
   
   The server will start at `http://localhost:5000`

5. **Open the application**
   - Open `index.html` in your web browser
   - Or use a local server like Live Server (VS Code extension)
   - Visit `http://localhost:5000` if using Flask to serve

## How to Use

1. **Upload Your Resume**
   - Click "Choose Resume" and select your PDF resume file

2. **Paste Job Description**
   - Copy and paste the job description or requirements from the job posting

3. **Click "Analyze Resume"**
   - The system will analyze your resume against the job description

4. **Review Results**
   - See your match score (0-100%)
   - View matched keywords from the job description
   - See missing keywords you should add
   - Read detailed recommendations for improvement

## How It Works

The analyzer uses:
- **Keyword Extraction**: Extracts important technical terms from both resume and job description
- **Pattern Matching**: Compares keywords and identifies gaps
- **Section Analysis**: Checks if key resume sections exist (Summary, Experience, Skills, Education)
- **Best Practice Rules**: Applies industry-standard resume guidelines
- **Scoring Algorithm**: Calculates overall match percentage

## Recommendations Include

- **Missing Keywords** - Technical skills and terms you should add
- **Summary Section** - If you lack a professional summary
- **Quantifiable Achievements** - Adding metrics and numbers
- **Action Verbs** - Using powerful verbs to describe accomplishments
- **ATS Compatibility** - Formatting and structure improvements
- **Experience Details** - Highlighting relevant work experience
- **Skills Section** - Listing relevant technical and soft skills

## Tips for Best Results

1. **Use actual job descriptions** - The more specific, the better the analysis
2. **Full resume text** - Ensure your PDF contains readable text (not a scanned image)
3. **Standard formatting** - Use simple fonts and layouts for better parsing
4. **Be specific** - Include all relevant skills, experiences, and keywords

## Troubleshooting

**Issue**: "Failed to parse PDF"
- Solution: Ensure your PDF contains selectable text. Scanned images won't work.

**Issue**: "Connection refused" error
- Solution: Make sure Flask server is running on port 5000

**Issue**: Limited recommendations
- Solution: Make sure your job description is detailed and specific

## Future Enhancements

- Support for .docx files
- Job description fetching from LinkedIn/Indeed
- Email recommendations report
- Resume improvement suggestions using AI
- Multi-language support

## License

This project is open source and free to use.

## Support

For issues or suggestions, please check the code or feel free to contribute!
