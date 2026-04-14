"""
Flask web application for AquaMetric AI.

This is the main backend server that handles PDF uploads and analysis.
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import backend modules
from backend.pdf_extractor import PDFExtractor
from backend.table_extractor import TableExtractor
from backend.data_processor import DataProcessor
from backend.rag_pipeline import RAGPipeline
from backend.agent import WaterSustainabilityAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize backend components
pdf_extractor = PDFExtractor()
table_extractor = TableExtractor()
data_processor = DataProcessor()
rag_pipeline = RAGPipeline(vectorstore_dir="./vectorstore")

# Initialize agent (lazy loading on first use)
agent = None


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_agent():
    """Get or initialize the agent (lazy loading)."""
    global agent
    if agent is None:
        try:
            agent = WaterSustainabilityAgent()
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing agent: {str(e)}")
            raise
    return agent


@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handle PDF upload and analysis.

    Expected POST data:
    - file: PDF file
    - waterScarcityContext: (optional) Context from water scarcity dataset

    Returns:
        JSON response with analysis results
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File saved: {filepath}")

        # Extract PDF text
        logger.info("Extracting PDF text...")
        pdf_text = pdf_extractor.extract_text(filepath)

        if not pdf_text:
            return jsonify({'error': 'Failed to extract text from PDF'}), 400

        # Extract tables
        logger.info("Extracting tables from PDF...")
        tables = table_extractor.extract_tables(filepath)
        tables_context = ""

        if tables:
            for i, table in enumerate(tables):
                tables_context += f"\n\nTable {i + 1}:\n{table.to_string()}"

        # Combine contexts
        full_text = pdf_text + tables_context

        # Store in vector database
        logger.info("Processing document into vector store...")
        rag_pipeline.process_pdf_to_vectorstore(full_text)

        # Search for relevant context
        logger.info("Searching for relevant context...")
        relevant_docs = rag_pipeline.search(
            "water usage consumption WUE effectiveness sustainability",
            k=5
        )
        context = "\n".join(relevant_docs) if relevant_docs else ""

        # Get optional water scarcity context from request
        water_scarcity_context = request.form.get('waterScarcityContext', '')

        # Analyze using agent
        logger.info("Running sustainability analysis...")
        agent_instance = get_agent()
        analysis_result = agent_instance.analyze_sustainability_report(
            full_text,
            water_scarcity_context=water_scarcity_context or context
        )

        if not analysis_result:
            # If full analysis fails, try to extract metrics only
            logger.warning("Full analysis failed, attempting metric extraction...")
            analysis_result = agent_instance.extract_metrics_only(full_text)

            if analysis_result:
                # Generate recommendations separately
                water_usage = analysis_result.get('water_usage', 'Unknown')
                wue = analysis_result.get('WUE', 'Unknown')
                region = analysis_result.get('region', 'Unknown')

                recommendations = agent_instance.generate_recommendations(
                    water_usage, wue, region
                )

                analysis_result['recommendations'] = recommendations or []
                analysis_result['risk_level'] = data_processor.estimate_risk_level(
                    float(water_usage) if isinstance(water_usage, str) and water_usage.replace('.', '', 1).isdigit() else 0,
                    region
                )
            else:
                return jsonify({'error': 'Failed to analyze PDF'}), 400

        logger.info("Analysis completed successfully")

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not delete uploaded file: {str(e)}")

        return jsonify({
            'success': True,
            'data': analysis_result
        })

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File is too large. Maximum size is 50MB.'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting AquaMetric AI Flask application...")
    logger.info("API Key configured: " + ("Yes" if os.getenv("OPENAI_API_KEY") else "No"))

    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
