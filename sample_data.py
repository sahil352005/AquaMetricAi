"""
Sample sustainability report for testing AquaMetric AI.

This module generates sample test data for development and testing.
"""

import os


def create_sample_pdf_text():
    """Create sample PDF text for testing."""
    return """
    GOOGLE CLOUD SUSTAINABILITY REPORT 2024
    
    Executive Summary
    Google is committed to reducing environmental impact of its operations.
    This report details our water management initiatives.
    
    Data Center Operations
    Our global data centers process petabytes of information daily.
    We maintain facilities in North America, Europe, and Asia.
    
    Water Usage Metrics
    Total Water Consumption: 1,500,000 ML per year
    Water Usage Effectiveness (WUE): 0.85 L/kWh
    Data Center Location: Virginia, United States
    Regional Water Stress: Medium-High
    
    Performance Indicators
    - Achieved 12% reduction in water usage from 2023
    - Improved cooling efficiency by 15%
    - Implemented AI-driven temperature management
    
    Detailed Metrics
    Water Withdrawal: 1,500,000 megalitres
    Water Recycled: 450,000 megalitres (30%)
    WUE Benchmark: 0.85 liters per kilowatt-hour
    
    Sustainability Initiatives
    1. Cooling Tower Optimization
    2. Wastewater Recycling Program
    3. Efficient HVAC Systems
    
    Recommendations for 2025
    - Increase water recycling to 40%
    - Implement predictive cooling maintenance
    - Expand regenerative water systems
    
    Tables Extracted:
    Year | Water Usage ML | WUE | Reduction %
    2022 | 1,700,000 | 1.05 | -
    2023 | 1,500,000 | 0.92 | 12%
    2024 | 1,500,000 | 0.85 | 8%
    
    Conclusion
    Google Cloud continues its commitment to water stewardship in data centers.
    Our innovations in cooling efficiency and water recycling set industry standards.
    We project further 20% reduction by 2028.
    """


def create_sample_analysis_result():
    """Create sample analysis result for frontend testing."""
    return {
        "water_usage": "1500000",
        "WUE": "0.85",
        "region": "United States",
        "risk_level": "Medium",
        "recommendations": [
            {
                "strategy": "Cooling Optimization",
                "description": "Implement machine learning-based cooling systems that dynamically adjust CRAC/CRAH units based on real-time temperature sensors. This reduces evaporative cooling needs.",
                "impact": "18"
            },
            {
                "strategy": "Recycled Water Usage",
                "description": "Install advanced water recycling systems for cooling tower makeup. Implement greywater harvesting and TDS removal to enable water reuse.",
                "impact": "22"
            },
            {
                "strategy": "Efficiency Improvements",
                "description": "Conduct annual water audits and upgrade to high-efficiency cooling towers. Implement predictive maintenance to identify leaks early.",
                "impact": "15"
            }
        ]
    }


def get_sample_water_scarcity_context():
    """Get sample water scarcity context for a region."""
    regions = {
        "United States": {
            "water_stress_level": "Low",
            "water_scarcity_index": 0.3,
            "population_millions": 331
        },
        "North America": {
            "water_stress_level": "Low-Medium",
            "water_scarcity_index": 0.4,
            "population_millions": 580
        },
        "Europe": {
            "water_stress_level": "Low",
            "water_scarcity_index": 0.35,
            "population_millions": 450
        },
        "Asia": {
            "water_stress_level": "High",
            "water_scarcity_index": 0.75,
            "population_millions": 4630
        }
    }
    return regions


if __name__ == "__main__":
    print("Sample PDF Text:")
    print(create_sample_pdf_text())
    print("\n" + "=" * 80 + "\n")
    print("Sample Analysis Result:")
    import json
    print(json.dumps(create_sample_analysis_result(), indent=2))
