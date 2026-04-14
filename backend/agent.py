"""
AI Agent for water sustainability analysis using LangChain and OpenAI.

This agent extracts water metrics, analyzes sustainability impact,
and suggests water-saving strategies.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import config
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a sustainability engineer specializing in data center infrastructure.

Your tasks:

1. Extract total water usage (ML/year or liters)
2. Extract Water Usage Effectiveness (WUE) in L/kWh
3. Identify data center location or region
4. Compare with water scarcity dataset (if provided)
5. Suggest 3 actionable strategies to reduce water usage:
   - Cooling optimization
   - Recycled water usage
   - Efficiency improvements
6. Estimate percentage reduction for each strategy (5-25%)

Return output ONLY in this JSON format, no additional text:
{
    "water_usage": "numeric value in ML/year",
    "WUE": "numeric value in L/kWh",
    "region": "identified region or country",
    "risk_level": "Low, Medium, or High",
    "recommendations": [
        {
            "strategy": "strategy name",
            "description": "how to implement",
            "impact": "estimated % reduction"
        },
        {
            "strategy": "strategy name",
            "description": "how to implement",
            "impact": "estimated % reduction"
        },
        {
            "strategy": "strategy name",
            "description": "how to implement",
            "impact": "estimated % reduction"
        }
    ]
}"""


class WaterSustainabilityAgent:
    """AI Agent for water sustainability analysis."""

    def __init__(self):
        """
        Initialize the sustainability agent using config.
        """
        self.logger = logger
        self.config = config.config
        self.llm = None
        self.parser = JsonOutputParser()

        # Initialize LLM based on provider
        provider = self.config.LLM_PROVIDER
        model = self.config.LLM_MODEL
        
        self.logger.info(f"Initializing LLM: {provider}/{model}")
        
        if provider == 'openai':
            api_key = self.config.OPENAI_API_KEY
            self.llm = ChatOpenAI(
                model=model,
                api_key=api_key,
                temperature=0.7,
            )
        elif provider == 'groq':
            api_key = self.config.GROQ_API_KEY
            self.llm = ChatGroq(
                model=model,
                api_key=api_key,
                temperature=0.7,
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
        
        self.logger.info("LLM initialized successfully")

    def analyze_sustainability_report(
        self,
        pdf_text: str,
        water_scarcity_context: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze sustainability report and generate recommendations.

        Args:
            pdf_text: Extracted text from PDF
            water_scarcity_context: Context from water scarcity dataset

        Returns:
            Analysis result as dictionary or None if failed
        """
        try:
            # Build the user prompt
            user_prompt = f"""Analyze the following sustainability report and extract water metrics and recommendations:

SUSTAINABILITY REPORT:
{pdf_text[:5000]}  # Limit to first 5000 chars for token efficiency

"""
            if water_scarcity_context:
                user_prompt += f"""
WATER SCARCITY CONTEXT:
{water_scarcity_context}

Use this context to assess regional water stress and tailor recommendations.
"""

            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("human", user_prompt),
            ])

            # Run the chain
            chain = prompt | self.llm
            response = chain.invoke({})

            # Parse JSON response
            response_text = response.content.strip()

            # Handle markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove ```

            result = json.loads(response_text)

            # Validate result structure
            required_fields = ["water_usage", "WUE", "region", "risk_level", "recommendations"]
            if not all(field in result for field in required_fields):
                self.logger.error("Invalid response structure from LLM")
                return None

            self.logger.info("Analysis completed successfully")
            return result

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error analyzing report: {str(e)}")
            return None

    def extract_metrics_only(self, pdf_text: str) -> Optional[Dict[str, Any]]:
        """
        Extract only water metrics without recommendations.

        Args:
            pdf_text: Extracted text from PDF

        Returns:
            Dictionary with extracted metrics
        """
        try:
            extraction_prompt = """Extract ONLY these fields from the text, return as JSON:
{
    "water_usage": "value in ML/year or liters",
    "WUE": "value in L/kWh",
    "region": "location mentioned"
}

If any field is not found, set to null."""

            prompt = ChatPromptTemplate.from_messages([
                ("human", pdf_text[:2000] + f"\n\n{extraction_prompt}"),
            ])

            chain = prompt | self.llm
            response = chain.invoke({})

            response_text = response.content.strip()

            # Clean markdown
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text)
            return result

        except Exception as e:
            self.logger.error(f"Error extracting metrics: {str(e)}")
            return None

    def generate_recommendations(
        self,
        water_usage: float,
        wue: float,
        region: str
    ) -> Optional[list]:
        """
        Generate water-saving recommendations based on metrics.

        Args:
            water_usage: Water usage in ML/year
            wue: Water Usage Effectiveness
            region: Data center region

        Returns:
            List of recommendation dictionaries
        """
        try:
            recommendation_prompt = f"""Based on these data center metrics, generate 3 specific water-saving recommendations:

Water Usage: {water_usage} ML/year
WUE: {wue} L/kWh
Region: {region}

For each recommendation, provide:
- Strategy name
- How to implement
- Estimated % reduction (5-25%)

Return as JSON array."""

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a sustainability engineer. Provide practical recommendations."),
                ("human", recommendation_prompt),
            ])

            chain = prompt | self.llm
            response = chain.invoke({})

            response_text = response.content.strip()

            # Clean markdown
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            recommendations = json.loads(response_text)
            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return None
