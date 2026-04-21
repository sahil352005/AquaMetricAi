# 🚀 Getting Started with AquaMetric AI

Welcome! This guide will help you set up and run AquaMetric AI in 5 minutes.

---

## ⚡ Quick Start (5 minutes)

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- 2GB RAM minimum
- 500MB disk space

### Step 1: Clone/Download Project
```bash
cd c:\Users\HP\Downloads\AquaMetricAi
```

### Step 2: Run Installation Script

**Windows:**
```bash
install.bat
```

**macOS/Linux:**
```bash
bash install.sh
```

**Manual Installation:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
```

### Step 3: Configure API Key

Edit `.env` file:
```bash
nano .env
# or
code .env
```

Find this line:
```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

**Where to get API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in with your OpenAI account
3. Click "Create new secret key"
4. Copy the key
5. Paste it in `.env`

### Step 4: Validate Setup

```bash
python quickstart.py
```

You should see:
```
✓ Python version OK
✓ .env file found
✓ OPENAI_API_KEY configured
✓ backend/ found
✓ templates/ found
... (more checks)
✅ All checks passed! Ready to start.
```

### Step 5: Start Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### Step 6: Open Dashboard

Open your browser to:
```
http://localhost:5000
```

You should see the beautiful AquaMetric AI dashboard!

---

## 📝 First Analysis (Step-by-Step)

### 1. Prepare a PDF
You need a PDF file with water/sustainability metrics. For testing, use one with:
- Water usage data (e.g., "15,637 ML", "5 Billion Gallons")
- WUE data (e.g., "0.19 L/kWh")
- Location or country name
- Recycled water stats (optional)

**Sample content:**
```
Meta Sustainability Summary
Reporting Year: 2023
Total water withdrawal: 15,637 Megaliters (ML)
Water Usage Effectiveness (WUE): 0.19 L/kWh
Locations: Global operations across USA, Europe, and Asia.
Recycled Water: 3,421 ML reused in facilities.
```

### 2. Upload PDF
- Click the upload area or drag and drop your PDF.

### 3. Click "Analyze PDF"
- The system will run a multi-pass analysis:
  - **Pass 1**: Deterministic extraction of metrics.
  - **Pass 2**: Water stress lookup via WRI Aqueduct 4.0.
  - **Pass 3**: Premium recommendation generation.

### 4. View Results
- **Metrics cards**: Show `water_usage`, `WUE`, `region`, and `risk_level`.
- **Charts**: New **Water Usage Distribution** chart shows current vs. recycled water.
- **Recommendations**: 3 high-value engineering strategies tailored to the risk level.

### 5. Export Results
Click "Export Results" to download:
- `aquametric-results-[timestamp].json` - Complete analysis
- `aquametric-results-[timestamp].csv` - Data in spreadsheet format

---

## 🧪 Test with Sample Data

If you don't have a real PDF, create one with this content:

### Option A: Create PDF with Python
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("test_report.pdf", pagesize=letter)
c.drawString(100, 750, "Sustainability Report 2024")
c.drawString(100, 700, "Water Usage: 1,500,000 ML/year")
c.drawString(100, 650, "WUE: 0.85 L/kWh")
c.drawString(100, 600, "Region: North America")
c.showPage()
c.save()
```

### Option B: Use Google Docs
1. Export any document as PDF
2. Add water metrics to the text
3. Upload to AquaMetric AI

### Option C: Use Online PDF Tools
1. Google Docs → Download as PDF
2. Microsoft Word → Export as PDF
3. Any text editor → Print to PDF

---

## 🔧 Common Setup Issues

### Issue 1: "OPENAI_API_KEY not found"
**Solution:**
```bash
# Check if .env exists
ls -la .env  # macOS/Linux
dir .env     # Windows

# If missing, create it
cp .env.example .env

# Edit and add your key
nano .env
```

### Issue 2: "Module not found: langchain"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or individually
pip install langchain openai chromadb
```

### Issue 3: "Port 5000 already in use"
**Solution:**

**Option A: Use different port**
Edit `app.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

**Option B: Kill process on port 5000**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# macOS/Linux
lsof -i :5000
kill -9 [PID]
```

### Issue 4: "PDF extraction failed"
**Solution:**
- Ensure PDF has selectable text (not scanned image)
- Try converting PDF to text first
- Use Google Docs to convert PDF

### Issue 5: "ChromaDB error"
**Solution:**
```bash
# Delete vectorstore and restart
rm -rf vectorstore/  # macOS/Linux
rmdir /s vectorstore  # Windows

# Restart application
python app.py
```

---

## 🚀 Next Steps

### After successful first analysis:

#### 1. Test with Real PDFs
- Download actual sustainability reports from:
  - Google Cloud Sustainability
  - Microsoft Environmental Report
  - Meta Sustainability Report

#### 2. Explore Dashboard Features
- Try uploading multiple PDFs
- Compare results
- Export and analyze data

#### 3. Understand the System
- Read [README.md](README.md) for full documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Review [PROJECT_MANIFEST.md](PROJECT_MANIFEST.md) for architecture

#### 4. Customize Configuration
Edit `.env` to adjust:
```
CHUNK_SIZE=1000              # Larger = more context, slower processing
CHUNK_OVERLAP=200            # More overlap = better context flow
FLASK_DEBUG=True             # Enable debug mode
```

#### 5. Deploy to Production
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📚 Learning Resources

### About the Project
- **What it does:** Analyzes water usage in data centers from PDFs
- **How it works:** Extracts data → AI analysis → Recommendations
- **Why it matters:** Helps companies reduce water consumption

### Key Technologies
- **Flask** - Web framework (https://flask.palletsprojects.com)
- **LangChain** - LLM orchestration (https://langchain.readthedocs.io)
- **ChromaDB** - Vector database (https://docs.trychroma.com)
- **OpenAI** - AI models (https://platform.openai.com)
- **Chart.js** - Data visualization (https://www.chartjs.org)

### Useful Commands
```bash
# Run tests
python quickstart.py

# View logs
tail -f logs/aquametric_*.log  # macOS/Linux
type logs/aquametric_*.log     # Windows

# Check Python packages
pip list

# Deactivate virtual environment
deactivate
```

---

## 💡 Pro Tips

### Tip 1: Use Virtual Environment
Always activate virtual environment before running:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Tip 2: Check Logs
Monitor application logs for debugging:
```bash
# Real-time log monitoring
tail -f logs/aquametric_*.log
```

### Tip 3: Keep API Key Secret
- Never commit `.env` to git
- Never share your API key
- `.env` is in `.gitignore` automatically

### Tip 4: Experiment Safely
- Test features locally first
- Use sample PDFs before production data
- Check API usage in OpenAI console

### Tip 5: Optimize Performance
- Larger PDFs take longer to process
- Results are cached in browser
- Clear vectorstore if running out of disk

---

## ❓ FAQ

**Q: How long does analysis take?**
A: Typically 15-30 seconds for a PDF analysis.

**Q: What PDF formats work?**
A: Standard PDFs with selectable text. Scanned images won't work.

**Q: Can I run this offline?**
A: No, you need OpenAI API access for AI features.

**Q: What's included in the results?**
A: Water metrics, risk level, and 3 actionable recommendations.

**Q: Can I export results?**
A: Yes! JSON and CSV export available.

**Q: Is my data safe?**
A: PDFs are temporary, vectors stored locally, no data retained.

**Q: How much does it cost?**
A: Only OpenAI API charges (gpt-4o-mini is affordable).

**Q: Can I run multiple instances?**
A: Yes, use different ports for each instance.

---

## 🎯 Final Checklist

Before first use:
- [ ] Downloaded/cloned project
- [ ] Ran install.bat or install.sh
- [ ] Created .env file
- [ ] Added OpenAI API key
- [ ] Ran quickstart.py (all checks passed)
- [ ] Started app.py
- [ ] Opened http://localhost:5000
- [ ] Tested with sample PDF
- [ ] Successfully analyzed first report
- [ ] Exported results

---

## 🆘 Still Having Issues?

1. **Check the logs:**
   ```bash
   cat logs/aquametric_*.log
   ```

2. **Validate setup:**
   ```bash
   python quickstart.py
   ```

3. **Read documentation:**
   - README.md - Full guide
   - API_DOCUMENTATION.md - API reference
   - PROJECT_MANIFEST.md - Architecture

4. **Check Python version:**
   ```bash
   python --version  # Should be 3.10+
   ```

5. **Verify dependencies:**
   ```bash
   pip list
   ```

---

## 🎉 Congratulations!

You've successfully set up AquaMetric AI! 

Now:
1. Start analyzing sustainability reports
2. Explore the dashboard features
3. Export and share results
4. Deploy to production when ready

**Questions?** Check the other documentation files or review the code comments.

**Ready to scale?** See deployment section in README.md.

---

**Built with ❤️ for sustainable data centers**

🌍 Help reduce water consumption in data centers worldwide!
