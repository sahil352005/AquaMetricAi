# 🚀 AquaMetric AI – Data Center Water Sustainability Analyzer

## 📋 Overview

**AquaMetric AI** is a production-ready full-stack AI system that analyzes corporate sustainability reports to extract water usage metrics and provide intelligent recommendations for water conservation in data centers.

The system combines:
- **PDF Text & Table Extraction** - Automatically extracts data from sustainability reports
- **RAG Pipeline** - Retrieves relevant context using embeddings and ChromaDB
- **Agentic AI** - Uses OpenAI GPT-4o-mini to analyze and generate recommendations
- **Web Dashboard** - Beautiful, responsive interface for results visualization

---

## 🎯 Key Features

✅ **PDF Analysis** - Extract water metrics from sustainability reports  
✅ **AI-Powered Recommendations** - Get 3 actionable water-saving strategies  
✅ **Risk Assessment** - Calculate water vulnerability based on region & usage  
✅ **Data Visualization** - Interactive charts for strategy impact  
✅ **Export Capability** - Save results as JSON or CSV  
✅ **Production-Ready** - Error handling, logging, security best practices  

---

## 🗂️ Project Architecture

```
aquametric-ai/
│
├── app.py                      # Flask main application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── backend/                   # Backend modules
│   ├── __init__.py
│   ├── pdf_extractor.py       # Extract text from PDFs
│   ├── table_extractor.py     # Extract tables from PDFs
│   ├── data_processor.py      # Clean and validate data
│   ├── rag_pipeline.py        # Vector DB & similarity search
│   └── agent.py               # AI agent for analysis
│
├── templates/                 # HTML templates
│   └── index.html             # Main dashboard
│
├── static/                    # Frontend assets
│   ├── style.css              # CSS styles
│   └── script.js              # JavaScript functionality
│
├── data/                      # Dataset directory
│   └── water_scarcity.csv     # Kaggle water scarcity data
│
└── vectorstore/               # ChromaDB storage (auto-created)
```

---

## 🧠 How It Works

### Phase 1: Document Ingestion
1. User uploads sustainability PDF report
2. Text extracted using PyMuPDF
3. Tables extracted using Camelot

### Phase 2: RAG Pipeline
1. Text split into chunks (1000 chars, 200 overlap)
2. Embeddings generated using OpenAI
3. Stored in ChromaDB vector database

### Phase 3: AI Analysis
1. Agent receives extracted text + RAG context
2. Extracts: water usage, WUE, region
3. Matches region with water scarcity dataset
4. Generates 3 water-saving strategies
5. Returns results as structured JSON

### Phase 4: Visualization
1. Results displayed in dashboard
2. Interactive charts using Chart.js
3. Export to JSON/CSV

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- OpenAI API key
- pip or conda

### Step 1: Clone/Download Project
```bash
cd c:\Users\HP\Downloads\AquaMetricAi
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### Step 5: Run Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 📊 API Endpoints

### GET `/`
Renders the main dashboard.

**Response:** HTML page

### POST `/analyze`
Analyzes an uploaded PDF file.

**Request:**
```
Header: Content-Type: multipart/form-data
Body:
  - file: [PDF file]
  - waterScarcityContext: (optional) Context string
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "water_usage": "1500",
    "WUE": "0.85",
    "region": "North America",
    "risk_level": "Medium",
    "recommendations": [
      {
        "strategy": "Cooling Optimization",
        "description": "Upgrade to AI-driven cooling systems",
        "impact": "15"
      },
      {
        "strategy": "Recycled Water Usage",
        "description": "Implement water recycling systems",
        "impact": "20"
      },
      {
        "strategy": "Efficiency Improvements",
        "description": "Regular maintenance and upgrades",
        "impact": "12"
      }
    ]
  }
}
```

**Response (Error):**
```json
{
  "error": "Only PDF files are allowed"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your_key_here

# Optional
OPENAI_MODEL=gpt-4o-mini
FLASK_ENV=development
FLASK_DEBUG=False
MAX_PDF_SIZE=50MB
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Flask Configuration (app.py)
- Max file size: 50MB
- Upload folder: `./uploads` (auto-created)
- Vector store: `./vectorstore` (auto-created)

---

## 📝 Usage Example

### 1. Start Application
```bash
python app.py
# Output: Running on http://0.0.0.0:5000/
```

### 2. Open Dashboard
Navigate to: `http://localhost:5000`

### 3. Upload PDF
- Click upload area or drag-drop a sustainability PDF
- PDF must contain water usage/WUE metrics

### 4. Click "Analyze PDF"
- System extracts data
- AI generates recommendations
- Results displayed with charts

### 5. Export Results
- Click "Export Results"
- Downloads JSON + CSV files

---

## 🧩 Backend Module Details

### pdf_extractor.py
Extracts text from PDF files using PyMuPDF.

```python
from backend.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
text = extractor.extract_text('report.pdf')
```

### table_extractor.py
Extracts tables from PDFs using Camelot.

```python
from backend.table_extractor import TableExtractor

extractor = TableExtractor()
tables = extractor.extract_tables('report.pdf')
```

### data_processor.py
Cleans and validates data.

```python
from backend.data_processor import DataProcessor

processor = DataProcessor()
df = processor.load_water_scarcity_dataset('water_scarcity.csv')
risk = processor.estimate_risk_level(1500, 'High')
```

### rag_pipeline.py
Vector database operations.

```python
from backend.rag_pipeline import RAGPipeline

rag = RAGPipeline()
rag.initialize_embeddings()
rag.process_pdf_to_vectorstore(pdf_text)
results = rag.search('water usage', k=5)
```

### agent.py
AI analysis agent.

```python
from backend.agent import WaterSustainabilityAgent

agent = WaterSustainabilityAgent()
result = agent.analyze_sustainability_report(pdf_text)
recommendations = agent.generate_recommendations(1500, 0.85, 'US')
```

---

## 🧪 Testing

### Test with Sample PDF
Create a simple PDF with water metrics:

```
Google Cloud Sustainability Report 2024

Data Center Water Usage: 1.5 Million Liters per Year
Water Usage Effectiveness (WUE): 0.85 L/kWh
Location: North America (USA - Virginia)

Summary: Our data centers implemented advanced cooling
efficiency measures reducing water consumption by 12%.
```

### Debug Mode
Enable debug logging:

```python
# In app.py or .env
FLASK_DEBUG=True
```

### Check Logs
Monitor application logs for errors:

```
2024-01-15 10:30:45 - app - INFO - File saved: uploads/report.pdf
2024-01-15 10:30:46 - app - INFO - Extracting PDF text...
2024-01-15 10:30:47 - app - INFO - Analysis completed successfully
```

---

## ⚠️ Error Handling

### Common Errors & Solutions

**Error: "OPENAI_API_KEY not set"**
```
Solution: Create .env file and add your API key
OPENAI_API_KEY=sk-your-key-here
```

**Error: "Failed to extract text from PDF"**
```
Solution: Ensure PDF is not scanned image, contains selectable text
```

**Error: "File is too large"**
```
Solution: Upload PDF smaller than 50MB
```

**Error: "ChromaDB error"**
```
Solution: Delete vectorstore/ folder and restart app
rm -rf vectorstore/
python app.py
```

---

## 📈 Performance Optimization

### Vector Store Management
- Chunk size: 1000 chars (adjustable via .env)
- Chunk overlap: 200 chars (for context continuity)
- Embeddings: OpenAI (3072 dimensions)

### API Call Optimization
- Uses GPT-4o-mini for cost efficiency
- Temperature: 0.7 (balanced creativity/accuracy)
- Max tokens: Auto-calculated

### Frontend Caching
- JavaScript results cached in memory
- Charts destroyed/recreated on refresh
- Minimal API calls

---

## 🔐 Security Considerations

✅ **API Key Management** - Uses environment variables, never hardcoded  
✅ **File Validation** - Only PDF files allowed  
✅ **File Size Limits** - 50MB maximum  
✅ **Input Sanitization** - XSS protection in frontend  
✅ **Error Messages** - Safe, non-revealing errors  
✅ **Logging** - No sensitive data logged  

---

## 📚 Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| LangChain | LLM orchestration |
| OpenAI | GPT-4o-mini access |
| ChromaDB | Vector database |
| PyMuPDF | PDF text extraction |
| Camelot | PDF table extraction |
| Pandas | Data manipulation |
| python-dotenv | Environment config |

---

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 📖 Example API Response

```json
{
  "success": true,
  "data": {
    "water_usage": "1500000",
    "WUE": "0.85",
    "region": "United States",
    "risk_level": "Medium",
    "recommendations": [
      {
        "strategy": "Cooling Optimization",
        "description": "Implement machine learning-based cooling systems for multi-site facilities. Monitor real-time temperature sensors and adjust CRAC/CRAH units dynamically. Expected savings: 10-20% reduction in evaporative cooling needs.",
        "impact": "18"
      },
      {
        "strategy": "Recycled Water Usage",
        "description": "Install water recycling systems for cooling tower makeup. Implement greywater harvesting from facility operations. Remove TDS (Total Dissolved Solids) before reuse.",
        "impact": "22"
      },
      {
        "strategy": "Efficiency Improvements",
        "description": "Conduct annual water audits. Replace aging cooling equipment. Upgrade to high-efficiency cooling towers (85%+ efficiency). Implement predictive maintenance.",
        "impact": "15"
      }
    ]
  }
}
```

---

## 📞 Support & Troubleshooting

### Check Dependencies
```bash
pip list
```

### Verify OpenAI Connection
```bash
python -c "from openai import OpenAI; print('OK')"
```

### Test PDF Extraction
```bash
python -c "from backend.pdf_extractor import PDFExtractor; PDFExtractor().extract_text('test.pdf')"
```

### Clear Cache
```bash
rm -rf vectorstore/
rm -rf uploads/
```

---

## 📄 License

This project is provided as-is for educational and commercial purposes.

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for LLM orchestration
- ChromaDB for vector storage
- Camelot for table extraction
- Chart.js for visualization

---

## 🎓 Learn More

- [OpenAI API Docs](https://platform.openai.com/docs)
- [LangChain Documentation](https://langchain.readthedocs.io)
- [ChromaDB Guide](https://docs.trychroma.com)
- [Flask Tutorial](https://flask.palletsprojects.com)

---

**Built with ❤️ for sustainable data centers**

🌍 *Helping organizations reduce their water footprint*
