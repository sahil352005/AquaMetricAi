# 🚀 AquaMetric AI – Data Center Water Sustainability Analyzer

## 📋 Overview

**AquaMetric AI** is an enterprise-grade Sustainability Intelligence Agent designed for precise data center water usage analysis. It transforms raw ESG reports into actionable, data-driven insights using the WRI Aqueduct 4.0 global risk framework.

The system combines:
- **Deterministic Extraction** - Advanced regex-first metric extraction for 100% accuracy on reporting units (ML, MGal, L/kWh).
- **RAG Pipeline** - Contextual retrieval of water scarcity and sustainability targets using ChromaDB.
- **Agentic AI** - Senior Sustainability Consultant persona (OpenAI/Groq) for technical, impact-driven strategy generation.
- **WRI Aqueduct Integration** - Objective regional risk assessment based on scientific country-level datasets.

---

## 🎯 Key Features

✅ **Technical Metric Extraction** - Precisely extract Water Usage, WUE, and Recycled Water volumes.  
✅ **Aqueduct 4.0 Risk Assessment** - Real-time lookup of water stress markers (BWS, BWD, IAV).  
✅ **Weighted Heuristic Scoring** - Data-driven risk classification (Usage + WUE + Recycling + Regional Stress).  
✅ **Premium Advice** - High-value recommendations for liquid cooling, HVAC optimization, and thermal management.  
✅ **Multi-Pass Logic** - Deterministic regex correction followed by AI-refined strategy generation.  

---

## 🗂️ Project Architecture

```
aquametric-ai/
│
├── app.py                      # Flask main application & REST API
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── backend/                   # Backend modules
│   ├── data_processor.py      # WRI Aqueduct lookup & Weighted Heuristic
│   ├── rag_pipeline.py        # Vector DB & contextual search
│   ├── agent.py               # AquaMetric AI Analysis Agent
│   ├── pdf_extractor.py       # PyMuPDF text engine
│   └── table_extractor.py     # Camelot table engine
│
├── data/                      # Dataset directory
│   └── aqueduct_water_risk.csv # WRI Aqueduct 4.0 Country Dataset
│
├── static/                    # Frontend assets (script.js, style.css)
├── templates/                 # UI Templates (index.html)
└── vectorstore/               # ChromaDB storage (auto-created)
```

---

## 🧠 How It Works

### Phase 1: Metric Extraction (Deterministic First)
1. System extracts text/tables from the sustainability PDF.
2. Advanced Regex patterns identify `water_usage` (ML) and `WUE` (L/kWh).
3. Values are normalized (converting gallons/liters to Megaliters).

### Phase 2: RAG & Context
1. Document is vectorized into ChromaDB.
2. System searches for sustainability targets, recycling initiatives, and regional locations.

### Phase 3: Data-Driven Risk Assessment
1. **Lookup**: Region/Country matched against the **WRI Aqueduct 4.0** dataset for physical risk.
2. **Heuristic**: If the region is "Global", a weighted score is calculated:
   - `Usage Score` + `WUE Score` - `Recycling Credit`.
3. **Thresholds**: 
   - 🔴 **High** (Score ≥ 4)
   - 🟡 **Medium** (Score ≥ 2)
   - 🟢 **Low** (Else)

### Phase 4: Strategy Generation
1. A senior consultant LLM pass generates 3 technical, high-value engineering strategies.
2. Each strategy includes an estimated Impact % and technical description.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- OpenAI or Groq API key
- pip

### Installation
1. Clone the project.
2. Create venv: `python -m venv venv` and activate it.
3. Install: `pip install -r requirements.txt`.
4. Configure `.env` using `.env.example`.
5. Run: `python app.py`.

---

## 📊 API Reference

### POST `/analyze`
Analyzes a PDF sustainability report.

**Request:** `multipart/form-data` with `file`.

**Response (Example):**
```json
{
  "success": true,
  "data": {
    "company": "Meta Platforms, Inc.",
    "report_year": "2023",
    "water_usage": 15637.0,
    "WUE": 0.19,
    "recycled_water": 3421.0,
    "region": "Global Operations",
    "risk_level": "Medium",
    "summary": "Meta demonstrates best-in-class WUE (0.19) and high recycling rates, offsetting high gross usage.",
    "recommendations": [
      {
        "strategy": "AI-Driven Thermal Balancing",
        "description": "Implement predictive AI cooling to shift compute loads based on regional water availability.",
        "impact": 15
      },
      {
        "strategy": "Direct-to-Chip Liquid Cooling",
        "description": "Transition high-density clusters to liquid-to-liquid exchange units to reduce evaporative loss.",
        "impact": 22
      }
    ]
  }
}
```

---

## ⚠️ Security & Standards

✅ **Hallucination Prevention**: Deterministic regex overrides LLM numbers if they deviate >10%.  
✅ **Source of Truth**: All geographic risk is driven by WRI Aqueduct 4.0, not LLM internal knowledge.  
✅ **Privacy**: Local file processing with automatic cleanup after analysis.  

---

## 📄 License
AquaMetric AI is provided for professional sustainability analysis and commercial ESG intelligence.

🌍 *Helping organizations optimize their water footprint through data.*
dthedocs.io)
- [ChromaDB Guide](https://docs.trychroma.com)
- [Flask Tutorial](https://flask.palletsprojects.com)

---

**Built with ❤️ for sustainable data centers**

🌍 *Helping organizations reduce their water footprint*
