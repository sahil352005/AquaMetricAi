# API Documentation - AquaMetric AI

## Overview

AquaMetric AI provides a REST API for analyzing sustainability reports and generating water-saving recommendations for data centers. The API is built with Flask and integrates OpenAI's GPT models with ChromaDB vector search.

---

## Base URL

```
http://localhost:5000
```

---

## Authentication

Currently, the API does not require authentication. In production, consider adding API key authentication.

---

## Endpoints

### 1. GET /

**Description:** Renders the main dashboard HTML page.

**Method:** GET

**Request:**
```
GET / HTTP/1.1
Host: localhost:5000
```

**Response:**
```
HTML page with embedded CSS and JavaScript
Status Code: 200
Content-Type: text/html
```

**Example:**
```bash
curl http://localhost:5000/
```

---

### 2. POST /analyze

**Description:** Analyzes an uploaded PDF sustainability report and generates water-saving recommendations.

**Method:** POST

**Content-Type:** multipart/form-data

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | PDF file to analyze |
| waterScarcityContext | string | No | Additional water scarcity context |

**Request Example:**
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@sustainability_report.pdf" \
  -F "waterScarcityContext=Region: North America"
```

**Response (Success - 200):**
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
        "description": "Implement machine learning-based cooling systems...",
        "impact": "18"
      },
      {
        "strategy": "Recycled Water Usage",
        "description": "Install water recycling systems...",
        "impact": "22"
      },
      {
        "strategy": "Efficiency Improvements",
        "description": "Conduct annual water audits...",
        "impact": "15"
      }
    ]
  }
}
```

**Response (Error - 400):**
```json
{
  "error": "Only PDF files are allowed"
}
```

**Response (Error - 413):**
```json
{
  "error": "File is too large. Maximum size is 50MB."
}
```

**Response (Error - 500):**
```json
{
  "error": "Server error: [error message]"
}
```

**Status Codes:**
- 200 OK - Analysis successful
- 400 Bad Request - Invalid file or request
- 413 Payload Too Large - File exceeds 50MB
- 500 Internal Server Error - Server error

**Processing Steps:**
1. PDF text extraction using PyMuPDF
2. Table extraction using Camelot
3. Vector store creation using ChromaDB
4. Similarity search for context retrieval
5. AI analysis using OpenAI GPT-4o-mini
6. Generation of water-saving recommendations

---

### 3. GET /health

**Description:** Health check endpoint to verify API availability.

**Method:** GET

**Request:**
```bash
curl http://localhost:5000/health
```

**Response (200):**
```json
{
  "status": "healthy"
}
```

---

## Response Schema

### Analysis Response (Success)

```json
{
  "success": boolean,
  "data": {
    "water_usage": string,           // ML/year or liters
    "WUE": string,                   // L/kWh
    "region": string,                // Location/Country
    "risk_level": string,            // "Low", "Medium", "High"
    "recommendations": [
      {
        "strategy": string,          // Strategy name
        "description": string,       // Implementation details
        "impact": string             // Estimated % reduction
      }
    ]
  }
}
```

### Analysis Response (Error)

```json
{
  "error": string                    // Error message
}
```

---

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 400 | No file provided | Include PDF file in request |
| 400 | No file selected | Select a file before uploading |
| 400 | Only PDF files allowed | Upload a valid PDF file |
| 400 | Failed to extract text from PDF | Ensure PDF contains selectable text (not scanned image) |
| 413 | File is too large | Upload file smaller than 50MB |
| 500 | OPENAI_API_KEY not set | Set OPENAI_API_KEY environment variable |
| 500 | Failed to analyze PDF | Check logs for detailed error message |
| 500 | Internal server error | Contact support |

---

## Rate Limiting

Currently, there is no rate limiting. In production, implement rate limiting to prevent abuse:
- Per IP address
- Per API key
- Per hour

---

## Request Examples

### Using Python Requests

```python
import requests

# Upload and analyze PDF
with open('sustainability_report.pdf', 'rb') as f:
    files = {'file': f}
    data = {'waterScarcityContext': 'North America'}
    response = requests.post('http://localhost:5000/analyze', files=files, data=data)

result = response.json()
print(result['data'])
```

### Using JavaScript Fetch

```javascript
const formData = new FormData();
formData.append('file', document.getElementById('fileInput').files[0]);

const response = await fetch('/analyze', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.data);
```

### Using cURL

```bash
# Basic upload
curl -X POST http://localhost:5000/analyze \
  -F "file=@report.pdf"

# With additional context
curl -X POST http://localhost:5000/analyze \
  -F "file=@report.pdf" \
  -F "waterScarcityContext=Region: Asia"
```

---

## Data Types

### water_usage

**Type:** String  
**Format:** Numeric value with unit  
**Examples:** "1500000", "1.5M liters", "1500000 ML"  
**Range:** 100,000 - 10,000,000 ML/year

### WUE (Water Usage Effectiveness)

**Type:** String  
**Format:** Numeric value in L/kWh  
**Examples:** "0.85", "1.05 L/kWh"  
**Range:** 0.5 - 2.0 L/kWh

### region

**Type:** String  
**Format:** Country or region name  
**Examples:** "United States", "North America", "Virginia"

### risk_level

**Type:** String  
**Enum:** ["Low", "Medium", "High"]  
**Definition:**  
- Low: Water usage < 500k ML/year + Low water stress region
- Medium: Water usage 500k-1M ML/year OR Medium water stress
- High: Water usage > 1M ML/year AND High water stress region

### impact

**Type:** String  
**Format:** Percentage value  
**Examples:** "15", "20%"  
**Range:** 5-25%

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Average response time | 15-30 seconds |
| Max file size | 50 MB |
| Max concurrent requests | 10 |
| PDF processing time | 5-20 seconds |
| AI analysis time | 10-20 seconds |

---

## Best Practices

1. **Always include PDF file in request**
   ```bash
   # ✓ Correct
   curl -F "file=@report.pdf" http://localhost:5000/analyze
   
   # ✗ Wrong
   curl http://localhost:5000/analyze
   ```

2. **Use meaningful file names**
   ```bash
   curl -F "file=@google_sustainability_2024.pdf" http://localhost:5000/analyze
   ```

3. **Handle errors gracefully**
   ```javascript
   if (!response.ok) {
     const error = await response.json();
     console.error(error.error);
   }
   ```

4. **Implement retry logic**
   ```python
   import time
   max_retries = 3
   for attempt in range(max_retries):
       try:
           response = requests.post(url, files=files, timeout=60)
           break
       except requests.exceptions.Timeout:
           time.sleep(2 ** attempt)
   ```

5. **Validate file before upload**
   ```javascript
   // Check file type
   if (!file.type.includes('pdf')) {
       console.error('File must be PDF');
   }
   
   // Check file size
   if (file.size > 50 * 1024 * 1024) {
       console.error('File too large');
   }
   ```

---

## Webhook Support (Future)

Future versions may support webhooks for long-running analyses:

```json
{
  "webhook_url": "https://example.com/callback",
  "webhook_events": ["analysis.complete", "analysis.error"]
}
```

---

## API Versioning

Current API version: v1 (implicit)

Future versioning: `/api/v1/analyze`

---

## Changelog

### v1.0.0 (Current)
- Initial API release
- PDF analysis endpoint
- Health check endpoint
- JSON response format

---

## Support

For API issues:
1. Check logs: `logs/aquametric_*.log`
2. Test health endpoint: `GET /health`
3. Verify PDF format (must have selectable text)
4. Check OpenAI API key validity

---

## FAQ

**Q: How long does analysis take?**  
A: Typically 15-30 seconds depending on PDF size and complexity.

**Q: What PDF formats are supported?**  
A: Standard PDF files with selectable text (not scanned images).

**Q: Can I analyze the same PDF twice?**  
A: Yes, each upload is independent.

**Q: How is my data handled?**  
A: PDFs are stored temporarily, vectors in ChromaDB, no data retained after analysis.

**Q: What's the maximum file size?**  
A: 50 MB per file.

---

*Last Updated: 2024-01-15*
