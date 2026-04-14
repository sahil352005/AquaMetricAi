"""
Utility functions for AquaMetric AI.

This module provides common utilities used across the application.
"""

import json
import re
from typing import Any, Dict, Optional


def parse_llm_json_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON response from LLM, handling markdown code blocks.

    Args:
        response_text: Raw response from LLM

    Returns:
        Parsed JSON dictionary or None
    """
    try:
        # Clean markdown code blocks
        text = response_text.strip()

        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        # Parse JSON
        return json.loads(text.strip())

    except json.JSONDecodeError:
        return None


def extract_numeric_value(text: str) -> Optional[float]:
    """
    Extract numeric value from text with units.

    Args:
        text: Text containing numeric value

    Returns:
        Numeric value or None
    """
    try:
        # Remove common units
        cleaned = text.upper()
        for unit in ["ML", "LITERS", "GALLONS", "L/KWH", "L/WATT", "%", "LITERS/WATT"]:
            cleaned = cleaned.replace(unit, "")

        # Extract numeric value
        numeric_str = ""
        for char in str(cleaned):
            if char.isdigit() or char == ".":
                numeric_str += char

        return float(numeric_str) if numeric_str else None

    except Exception:
        return None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove special characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = re.sub(r'\s+', '_', filename)
    # Limit length
    return filename[:255]


def truncate_text(text: str, max_length: int = 5000) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text (rough approximation).

    Args:
        text: Text to count

    Returns:
        Estimated token count
    """
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4


def format_percentage(value: float) -> str:
    """
    Format value as percentage.

    Args:
        value: Numeric value

    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"


def format_water_volume(value: float, unit: str = "ML") -> str:
    """
    Format water volume with appropriate units.

    Args:
        value: Volume value
        unit: Unit (ML, liters, gallons)

    Returns:
        Formatted string
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M {unit}"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K {unit}"
    else:
        return f"{value:.2f} {unit}"


def risk_level_color(risk_level: str) -> str:
    """
    Get color code for risk level.

    Args:
        risk_level: Risk level string

    Returns:
        Hex color code
    """
    colors = {
        "low": "#10b981",       # Green
        "medium": "#f59e0b",    # Orange
        "high": "#ef4444",      # Red
        "unknown": "#6b7280"    # Gray
    }
    return colors.get(risk_level.lower(), colors["unknown"])


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def dict_to_csv(data: Dict[str, Any]) -> str:
    """
    Convert dictionary to CSV line.

    Args:
        data: Dictionary with data

    Returns:
        CSV formatted string
    """
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(data.keys())
    # Write values
    writer.writerow(data.values())

    return output.getvalue()


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge two dictionaries recursively.

    Args:
        dict1: First dictionary
        dict2: Second dictionary

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


if __name__ == "__main__":
    # Test utilities
    print("Testing utilities...")

    # Test JSON parsing
    json_str = "```json\n{\"water_usage\": \"1500\"}\n```"
    result = parse_llm_json_response(json_str)
    print(f"✓ JSON parsing: {result}")

    # Test numeric extraction
    value = extract_numeric_value("1.5M liters per year")
    print(f"✓ Numeric extraction: {value}")

    # Test water volume formatting
    formatted = format_water_volume(1_500_000, "ML")
    print(f"✓ Water formatting: {formatted}")

    # Test risk color
    color = risk_level_color("High")
    print(f"✓ Risk color: {color}")

    print("\nAll utilities working correctly!")
