"""
Data processing module for water scarcity and sustainability data.

This module handles cleaning, validation, and normalization of data.
Supports both the legacy water_scarcity.csv and the comprehensive
WRI Aqueduct 4.0 dataset (aqueduct_water_risk.csv).
"""

import pandas as pd
import logging
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and clean water scarcity and sustainability data."""

    def __init__(self):
        """Initialize data processor."""
        self.logger = logger
        self.water_scarcity_df = None  # kept for backward compat in find_water_stress_level
        self.aqueduct_df = None

    # ------------------------------------------------------------------
    # Dataset loading
    # ------------------------------------------------------------------

    def load_water_scarcity_dataset(self, csv_path: str) -> Optional[pd.DataFrame]:
        """
        Backward-compatible alias for load_aqueduct_dataset.

        .. deprecated:: Use load_aqueduct_dataset() instead.
        """
        self.logger.info("load_water_scarcity_dataset is deprecated, delegating to load_aqueduct_dataset")
        return self.load_aqueduct_dataset(csv_path)

    def load_aqueduct_dataset(self, csv_path: str = "data/aqueduct_water_risk.csv") -> Optional[pd.DataFrame]:
        """
        Load the WRI Aqueduct 4.0 water risk dataset.

        This is a comprehensive dataset with 190+ countries containing:
        - Baseline Water Stress (bws_score, 0-5 scale)
        - Baseline Water Depletion (bwd_score, 0-5)
        - Interannual Variability (iav_score, 0-5)
        - Seasonal Variability (sev_score, 0-5)
        - Overall composite risk score and label

        It also includes backward-compatible columns (water_stress_level,
        water_scarcity_index) so existing code continues to work.

        Args:
            csv_path: Path to the aqueduct CSV file

        Returns:
            Cleaned DataFrame or None if loading fails
        """
        try:
            df = pd.read_csv(csv_path)
            self.logger.info(f"Loaded Aqueduct 4.0 dataset with {len(df)} countries")

            df = self._clean_dataframe(df)
            self.aqueduct_df = df

            # Also set as the water_scarcity_df for backward compatibility
            self.water_scarcity_df = df
            return df

        except FileNotFoundError:
            self.logger.error(f"Aqueduct CSV not found: {csv_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading Aqueduct dataset: {str(e)}")
            return None

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean dataframe by handling missing values and normalizing columns.

        Args:
            df: DataFrame to clean

        Returns:
            Cleaned DataFrame
        """
        # Normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Handle missing values
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("Unknown")
            else:
                df[col] = df[col].fillna(df[col].mean())

        # Remove duplicates (keep first occurrence by country name)
        if "country" in df.columns:
            df.drop_duplicates(subset=["country"], keep="first", inplace=True)
        else:
            df.drop_duplicates(inplace=True)

        self.logger.info("Data cleaning completed")
        return df

    # ------------------------------------------------------------------
    # Lookup methods
    # ------------------------------------------------------------------

    def find_water_stress_level(self, region: str) -> Optional[dict]:
        """
        Find water stress level for a region/country.

        Searches by country name, ISO code, and region columns.

        Args:
            region: Region, country name, or ISO alpha-3 code

        Returns:
            Dictionary with region data or None if not found
        """
        try:
            df = self.aqueduct_df if self.aqueduct_df is not None else self.water_scarcity_df
            if df is None:
                self.logger.error("No water dataset loaded")
                return None

            region_lower = region.strip().lower()

            # PRIORITY 1: Exact ISO code match (high confidence)
            if len(region_lower) == 3:
                iso_match = df[df["iso_a3"].str.lower() == region_lower]
                if not iso_match.empty:
                    return iso_match.iloc[0].to_dict()

            # PRIORITY 2: Exact country name match
            country_match = df[df["country"].str.lower() == region_lower]
            if not country_match.empty:
                return country_match.iloc[0].to_dict()

            # PRIORITY 3: Fallback to partial search across columns
            search_cols = ["country", "iso_a3", "region"]
            for col in search_cols:
                if col not in df.columns: continue
                matches = df[df[col].str.lower().str.contains(region_lower, na=False)]
                if not matches.empty:
                    return matches.iloc[0].to_dict()

            # Fallback for legacy CSV (first column)
            matches = df[df.iloc[:, 0].str.contains(region, case=False, na=False)]
            if not matches.empty:
                return matches.iloc[0].to_dict()

            self.logger.warning(f"Region not found: {region}")
            return None

        except Exception as e:
            self.logger.error(f"Error finding water stress level: {str(e)}")
            return None

    def get_country_risk_profile(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Get a full Aqueduct 4.0 risk profile for a country.

        Returns all risk indicators in a structured format useful
        for AI analysis and report generation.

        Args:
            country: Country name or ISO alpha-3 code

        Returns:
            Dictionary with full risk profile, or None if not found
        """
        try:
            data = self.find_water_stress_level(country)
            if data is None:
                return None

            profile = {
                "country": data.get("country", country),
                "iso_code": data.get("iso_a3", "GBL"),
                "region": data.get("region", "Global Operations"),
                "baseline_water_stress": {
                    "score": data.get("bws_score", None),
                    "label": data.get("bws_label", "Moderate"),
                },
                "baseline_water_depletion": {
                    "score": data.get("bwd_score", None),
                },
                "interannual_variability": {
                    "score": data.get("iav_score", None),
                },
                "seasonal_variability": {
                    "score": data.get("sev_score", None),
                },
                "overall_risk": {
                    "score": data.get("overall_risk_score", None),
                    "label": data.get("overall_risk_label", "Medium"),
                },
                "population_millions": data.get("population_millions", None),
                # Legacy fields
                "water_stress_level": data.get("water_stress_level", "Unknown"),
                "water_scarcity_index": data.get("water_scarcity_index", None),
            }

            return profile

        except Exception as e:
            self.logger.error(f"Error getting country risk profile: {str(e)}")
            return None

    # ------------------------------------------------------------------
    # Risk estimation
    # ------------------------------------------------------------------

    def estimate_risk_level(
        self, 
        water_usage: float, 
        water_stress: str, 
        wue: Optional[float] = None,
        recycled_water_ratio: Optional[float] = None
    ) -> str:
        """
        Estimate environmental risk level using Aqueduct data or a weighted heuristic.

        Args:
            water_usage: Total water usage in ML/year
            water_stress: Water stress level string, country name, or "Global"/"Multi-Region"
            wue: Water Usage Effectiveness (L/kWh)
            recycled_water_ratio: Percentage of recycled water (0-100)

        Returns:
            Risk level: "Low", "Medium", or "High"
        """
        try:
            # Try to look up the country in Aqueduct data for richer scoring
            country_data = self.find_water_stress_level(water_stress)
            
            # 1. Exact country match found in Aqueduct dataset
            if country_data and "overall_risk_score" in country_data and water_stress.lower() not in ["global", "multi-region", "multi region"]:
                return self._estimate_risk_with_aqueduct(water_usage, country_data)

            # 2. Weighted Heuristic for Global/Multi-Region or unmatched data
            score = 0

            # Usage Score
            if water_usage > 10000:
                score += 2
            elif water_usage > 5000:
                score += 1

            # WUE Score (if available)
            if wue is not None:
                if wue > 0.4:
                    score += 2
                elif wue > 0.2:
                    score += 1

            # Recycling Credit (if available)
            if recycled_water_ratio is not None and recycled_water_ratio > 10:
                score -= 1

            # Final classification
            # Refined thresholds for enterprise realism
            if score >= 4:
                return "High"
            elif score >= 2:
                return "Medium"
            else:
                return "Low"

        except Exception as e:
            self.logger.error(f"Error estimating risk level: {str(e)}")
            return "Medium"  # Safe fallback

    def _estimate_risk_with_aqueduct(self, water_usage: float, country_data: dict) -> str:
        """
        Estimate risk using Aqueduct 4.0 composite score + water usage volume.

        Args:
            water_usage: Total water usage in ML/year
            country_data: Dictionary from Aqueduct dataset row

        Returns:
            Risk level string
        """
        try:
            composite = float(country_data.get("overall_risk_score", 2.0))

            # Adjust based on absolute water usage volume
            if water_usage > 1000000:
                composite += 0.5
            elif water_usage > 500000:
                composite += 0.25

            # Map to risk label
            if composite >= 3.5:
                return "High"
            elif composite >= 2.0:
                return "Medium"
            else:
                return "Low"

        except (ValueError, TypeError):
            return "Unknown"

    # ------------------------------------------------------------------
    # Metric validation
    # ------------------------------------------------------------------

    def validate_water_metrics(
        self, water_usage: str, wue: str
    ) -> Tuple[bool, Optional[float], Optional[float]]:
        """
        Validate and convert water metrics to numeric values.

        Args:
            water_usage: Water usage as string (e.g., "1.5M liters")
            wue: WUE as string (e.g., "0.85")

        Returns:
            Tuple of (is_valid, water_usage_numeric, wue_numeric)
        """
        try:
            water_numeric = self._parse_water_value(water_usage)
            wue_numeric = self._parse_numeric_value(wue)

            if water_numeric is not None and wue_numeric is not None:
                return True, water_numeric, wue_numeric
            else:
                return False, None, None

        except Exception as e:
            self.logger.error(f"Error validating metrics: {str(e)}")
            return False, None, None

    def _parse_water_value(self, value: str) -> Optional[float]:
        """Parse water value with units (ML, liters, gallons, etc.)."""
        try:
            value = str(value).upper().strip()

            # Remove common units
            value = value.replace("ML", "").replace("LITERS", "").replace("GALLONS", "").strip()

            # Try to extract numeric value
            numeric_str = ""
            for char in value:
                if char.isdigit() or char == ".":
                    numeric_str += char

            return float(numeric_str) if numeric_str else None

        except Exception as e:
            self.logger.error(f"Error parsing water value: {str(e)}")
            return None

    def _parse_numeric_value(self, value: str) -> Optional[float]:
        """Parse numeric value, removing common units."""
        try:
            value = str(value).strip()

            # Remove common units
            for unit in ["L/KWH", "L/WATT", "%", "LITERS/WATT"]:
                value = value.replace(unit, "")

            numeric_str = ""
            for char in value:
                if char.isdigit() or char == ".":
                    numeric_str += char

            return float(numeric_str) if numeric_str else None

        except Exception as e:
            self.logger.error(f"Error parsing numeric value: {str(e)}")
            return None
