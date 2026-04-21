"""Temperature calibration system for Clima."""

import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.storage import STORAGE_VERSION

STORAGE_KEY = "clima_calibration"
CALIBRATION_VERSION = 1


class TemperatureCalibration:
    """Manages temperature offset calibration for each zone."""

    def __init__(self, hass: HomeAssistant):
        """Initialize calibration system."""
        self.hass = hass
        self.calibrations: Dict[str, dict] = {}
        self.learning_enabled = True
        self.tolerance = 2.0  # ±2°C tolerance
        self.learning_threshold = 0.5  # Minimum change to register

    async def async_load(self) -> None:
        """Load calibration data from storage."""
        store = self.hass.helpers.storage.Store(
            STORAGE_VERSION, STORAGE_KEY
        )
        try:
            data = await store.async_load()
            if data:
                self.calibrations = data.get("calibrations", {})
                self.learning_enabled = data.get("learning_enabled", True)
        except Exception:
            self.calibrations = {}

    async def async_save(self) -> None:
        """Save calibration data to storage."""
        store = self.hass.helpers.storage.Store(
            STORAGE_VERSION, STORAGE_KEY
        )
        await store.async_save({
            "calibrations": self.calibrations,
            "learning_enabled": self.learning_enabled,
            "version": CALIBRATION_VERSION,
        })

    def learn_offset(
        self,
        zone_id: str,
        setpoint: float,
        external_temp: float
    ) -> Optional[float]:
        """
        Learn temperature offset for a zone.

        Args:
            zone_id: Zone identifier
            setpoint: AC setpoint temperature
            external_temp: External sensor temperature

        Returns:
            Calculated offset or None if no learning needed
        """
        if not self.learning_enabled:
            return None

        # Calculate the difference
        current_offset = setpoint - external_temp

        # Initialize zone calibration if needed
        if zone_id not in self.calibrations:
            self.calibrations[zone_id] = {
                "offset": 0.0,
                "samples": [],
                "last_updated": None,
                "locked": False,
            }

        cal = self.calibrations[zone_id]

        # Skip if calibration is locked
        if cal.get("locked", False):
            return None

        # Check if offset is outside tolerance
        if abs(current_offset) <= self.tolerance:
            return None

        # Record sample
        cal["samples"].append({
            "timestamp": datetime.now().isoformat(),
            "setpoint": setpoint,
            "external_temp": external_temp,
            "offset": current_offset,
        })

        # Keep only last 10 samples
        if len(cal["samples"]) > 10:
            cal["samples"] = cal["samples"][-10:]

        # Calculate average offset from recent samples
        offsets = [s["offset"] for s in cal["samples"]]
        avg_offset = sum(offsets) / len(offsets)

        # Update if change is significant
        if abs(avg_offset - cal["offset"]) >= self.learning_threshold:
            cal["offset"] = round(avg_offset, 1)
            cal["last_updated"] = datetime.now().isoformat()
            return cal["offset"]

        return None

    def get_adjusted_setpoint(
        self,
        zone_id: str,
        target_temp: float
    ) -> float:
        """
        Get adjusted AC setpoint based on learned offset.

        Args:
            zone_id: Zone identifier
            target_temp: Desired temperature from external sensor

        Returns:
            Adjusted setpoint for AC unit
        """
        if zone_id not in self.calibrations:
            return target_temp

        offset = self.calibrations[zone_id].get("offset", 0.0)
        adjusted = target_temp + offset

        # Clamp to reasonable range
        return max(16.0, min(30.0, adjusted))

    def get_calibration_data(self, zone_id: str) -> Optional[dict]:
        """Get calibration data for a zone."""
        return self.calibrations.get(zone_id)

    def set_calibration_locked(self, zone_id: str, locked: bool) -> None:
        """Lock/unlock calibration for a zone."""
        if zone_id not in self.calibrations:
            self.calibrations[zone_id] = {
                "offset": 0.0,
                "samples": [],
                "last_updated": None,
                "locked": False,
            }
        self.calibrations[zone_id]["locked"] = locked

    def reset_calibration(self, zone_id: str) -> None:
        """Reset calibration for a zone."""
        if zone_id in self.calibrations:
            self.calibrations[zone_id] = {
                "offset": 0.0,
                "samples": [],
                "last_updated": None,
                "locked": False,
            }

    def reset_all(self) -> None:
        """Reset all calibrations."""
        self.calibrations = {}

    def get_all_calibrations(self) -> Dict[str, dict]:
        """Get all calibration data."""
        return self.calibrations.copy()

    def set_learning_enabled(self, enabled: bool) -> None:
        """Enable/disable automatic learning."""
        self.learning_enabled = enabled

    def set_tolerance(self, tolerance: float) -> None:
        """Set tolerance threshold."""
        if 0.5 <= tolerance <= 5.0:
            self.tolerance = tolerance

    def get_statistics(self, zone_id: str) -> Optional[dict]:
        """Get calibration statistics for a zone."""
        if zone_id not in self.calibrations:
            return None

        cal = self.calibrations[zone_id]
        samples = cal.get("samples", [])

        if not samples:
            return None

        offsets = [s["offset"] for s in samples]

        return {
            "zone_id": zone_id,
            "current_offset": round(cal["offset"], 1),
            "sample_count": len(samples),
            "min_offset": min(offsets),
            "max_offset": max(offsets),
            "avg_offset": round(sum(offsets) / len(offsets), 1),
            "locked": cal.get("locked", False),
            "last_updated": cal.get("last_updated"),
        }
