# QUICK START GUIDE

## Installation & Running (Windows)

### Option 1: Automatic Setup (Easiest)
1. Double-click `setup.bat`
2. Wait for the server to start
3. Open `index.html` in your browser

### Option 2: Manual Setup
1. Open Command Prompt in this folder
2. Create virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Run server: `python app.py`
6. Open `index.html` in your browser

## How to Use the App

1. **Upload PDF Resume** - Click to select your resume PDF file
2. **Paste Job Description** - Copy and paste the job posting you're applying for
3. **Click "Analyze Resume"** - Wait for the analysis to complete
4. **Review Results**:
   - Your match score (0-100%)
   - Keywords you already have
   - Keywords you're missing (add these!)
   - Specific recommendations to improve

## Project Structure

```
resume tester/
├── index.html          # Frontend UI
├── style.css           # Styling
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── setup.bat           # Windows setup script
├── README.md           # Full documentation
└── QUICKSTART.md       # This file
```

## Features

✅ Free (no API costs)
✅ Offline (except file upload)
✅ Keyword matching
✅ Match score calculation
✅ ATS compatibility checks
✅ Actionable recommendations
✅ Simple, clean interface

## Troubleshooting

**Port 5000 already in use?**
- Edit `app.py` line 109: change `port=5000` to `port=5001`
- Then update `API_URL` in `index.html` line 109

**PDF won't parse?**
- Make sure it's a real PDF with text (not a scanned image)
- Try a different PDF reader to copy text

**Server won't start?**
- Make sure Python is installed
- Check if port 5000 is available
- Try restarting the setup script

## Next Steps

1. Try analyzing a few resumes with different job descriptions
2. See which keywords are consistently missing
3. Update your resume with suggested improvements
4. Test again to see your improved match score!

## Pro Tips

- Use the actual job description from the company's website
- Include all your relevant skills in your resume
- Use strong action verbs (led, managed, developed, etc.)
- Add numbers/metrics to your achievements
- Keep formatting simple and ATS-friendly

Good luck with your job applications! 🚀
