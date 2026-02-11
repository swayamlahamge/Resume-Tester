from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfplumber
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

app = Flask(__name__)
CORS(app)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return None

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and short words
    stop_words = set(stopwords.words('english'))
    keywords = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    return keywords

def extract_resume_sections(text):
    """Extract main sections from resume"""
    sections = {
        'contact': '',
        'summary': '',
        'experience': '',
        'skills': '',
        'education': '',
        'projects': ''
    }
    
    # Simple pattern matching for common sections
    text_lower = text.lower()
    
    # Find section boundaries
    section_patterns = {
        'summary': r'(summary|profile|objective)(.*?)(?=experience|skills|education|projects|$)',
        'experience': r'(experience|work)(.*?)(?=skills|education|projects|summary|$)',
        'skills': r'(skills|technical)(.*?)(?=experience|education|projects|summary|$)',
        'education': r'(education|degree)(.*?)(?=experience|skills|projects|summary|$)',
    }
    
    for section, pattern in section_patterns.items():
        match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(2).strip()[:500]
    
    return sections

def analyze_resume(resume_text, job_description):
    """Analyze resume against job description"""
    # Extract keywords from both
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Count occurrences
    resume_counter = Counter(resume_keywords)
    job_counter = Counter(job_keywords)
    
    # Find matches
    matched_keywords = []
    missing_keywords = []
    
    for keyword in job_counter.most_common(50):
        if keyword[0] in resume_counter:
            matched_keywords.append(keyword[0])
        else:
            missing_keywords.append(keyword[0])
    
    # Calculate match percentage
    if len(job_counter) > 0:
        match_percentage = (len(matched_keywords) / min(len(job_counter), 50)) * 100
    else:
        match_percentage = 0
    
    match_percentage = min(match_percentage, 100)
    
    # Extract sections
    resume_sections = extract_resume_sections(resume_text)
    
    # Generate recommendations
    recommendations = generate_recommendations(
        resume_text, 
        job_description,
        resume_sections,
        matched_keywords,
        missing_keywords
    )
    
    return {
        'match_percentage': round(match_percentage, 1),
        'matched_keywords': matched_keywords[:10],
        'missing_keywords': missing_keywords[:15],
        'recommendations': recommendations,
        'resume_sections': resume_sections
    }

def generate_recommendations(resume_text, job_description, sections, matched, missing):
    """Generate actionable recommendations"""
    recommendations = []
    
    # Check for missing keywords
    if missing:
        recommendations.append({
            'priority': 'high',
            'title': 'Add Missing Keywords',
            'description': f"Include these key terms from the job description: {', '.join(missing[:5])}",
            'action': 'Add these skills/technologies to your resume where relevant'
        })
    
    # Check if summary exists
    if not sections['summary'] or len(sections['summary']) < 50:
        recommendations.append({
            'priority': 'high',
            'title': 'Add/Improve Summary',
            'description': 'Your resume lacks a professional summary or objective',
            'action': 'Add a brief professional summary highlighting key skills and achievements'
        })
    
    # Check for achievements/metrics
    if not re.search(r'\d+%|\$\d+|increased|improved|reduced', resume_text.lower()):
        recommendations.append({
            'priority': 'high',
            'title': 'Add Quantifiable Achievements',
            'description': 'Resumes with metrics/numbers are more impactful',
            'action': 'Add percentages, dollar amounts, or quantifiable results to your accomplishments'
        })
    
    # Check for action verbs
    action_verbs = ['led', 'managed', 'developed', 'created', 'improved', 'designed', 'implemented', 'increased']
    action_verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    
    if action_verb_count < 3:
        recommendations.append({
            'priority': 'medium',
            'title': 'Use Strong Action Verbs',
            'description': 'Limited use of powerful action verbs detected',
            'action': f"Replace weak verbs with action words like: {', '.join(action_verbs[:4])}"
        })
    
    # ATS Optimization
    if re.search(r'[^\x00-\x7F]', resume_text):  # Check for special characters
        recommendations.append({
            'priority': 'medium',
            'title': 'ATS Compatibility',
            'description': 'Special characters detected that may confuse ATS systems',
            'action': 'Use standard characters and fonts for ATS compatibility'
        })
    
    # Check for experience
    if not sections['experience'] or len(sections['experience']) < 50:
        recommendations.append({
            'priority': 'high',
            'title': 'Highlight Relevant Experience',
            'description': 'Experience section is missing or too brief',
            'action': 'Add detailed work experience with achievements and responsibilities'
        })
    
    # Check skills section
    if not sections['skills'] or len(sections['skills']) < 30:
        recommendations.append({
            'priority': 'medium',
            'title': 'Expand Skills Section',
            'description': 'Skills section is missing or too brief',
            'action': 'List relevant technical and soft skills'
        })
    
    # Check for education
    if not sections['education'] or len(sections['education']) < 30:
        recommendations.append({
            'priority': 'low',
            'title': 'Add Education Details',
            'description': 'Education section is missing or incomplete',
            'action': 'Include degree, institution, and graduation date'
        })
    
    return recommendations

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze resume"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not job_description:
            return jsonify({'error': 'No job description provided'}), 400
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume_file)
        
        if not resume_text:
            return jsonify({'error': 'Failed to parse PDF'}), 400
        
        # Analyze resume
        analysis = analyze_resume(resume_text, job_description)
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/style.css')
def serve_css():
    """Serve CSS file"""
    with open('style.css', 'r', encoding='utf-8') as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
