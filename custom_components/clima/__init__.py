"""Clima - Multi-Zone AC Controller Integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import discovery
from homeassistant.helpers.entity_registry import async_get
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_ZONES,
    CONF_ZONE_NAME,
    CONF_AC_ENTITY,
    CONF_TEMP_SENSOR,
    CONF_WINDOW_SENSOR,
    CONF_OUTSIDE_TEMP,
    SERVICE_SET_ZONE_TEMP,
    SERVICE_TOGGLE_ZONE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = []


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Clima from a config entry."""
    _LOGGER.info("🌡️ Setting up Clima integration")

    hass.data.setdefault(DOMAIN, {})

    # Discover AC units (climate entities)
    discovered_zones = await _discover_ac_units(hass)

    if not discovered_zones:
        _LOGGER.warning(
            "⚠️ No AC units found! Install Midea AC integration first and "
            "restart Home Assistant."
        )
    else:
        _LOGGER.info(f"🔍 Found {len(discovered_zones)} AC unit(s)")
        for zone_id, zone_info in discovered_zones.items():
            _LOGGER.info(f"  ✓ {zone_info['name']} ({zone_info['ac_entity']})")

    hass.data[DOMAIN][entry.entry_id] = {
        "zones": discovered_zones,
        "outside_temp": entry.data.get(CONF_OUTSIDE_TEMP),
    }

    # Create helper entities for discovered zones
    await _create_helper_entities(hass, discovered_zones)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_ZONE_TEMP,
        _handle_set_zone_temp,
        schema=vol.Schema({}),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TOGGLE_ZONE,
        _handle_toggle_zone,
        schema=vol.Schema({}),
    )

    # Listen for options updates
    entry.async_on_unload(entry.add_update_listener(async_update_listener))

    _LOGGER.info("✅ Clima integration setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    discovered_zones = await _discover_ac_units(hass)
    hass.data[DOMAIN][entry.entry_id] = {
        "zones": discovered_zones,
        "outside_temp": entry.options.get(CONF_OUTSIDE_TEMP),
    }


async def _discover_ac_units(hass: HomeAssistant) -> Dict[str, Dict[str, str]]:
    """
    Auto-discover AC units (climate entities) in Home Assistant.

    Returns:
        Dictionary with zone info for each found AC unit
    """
    discovered = {}

    # Get all entities
    entity_registry = async_get(hass)

    # Search for climate entities (AC units)
    for entity_id, entity_entry in entity_registry.entities.items():
        if entity_id.startswith("climate."):
            # Extract zone name from entity ID
            # e.g., climate.bedroom_ac -> bedroom
            zone_name = entity_entry.name or entity_id.replace("climate.", "").replace("_ac", "")
            zone_id = zone_name.lower().replace(" ", "_")

            discovered[zone_id] = {
                "name": zone_name,
                "ac_entity": entity_id,
                "id": zone_id,
            }

            _LOGGER.debug(f"Discovered AC unit: {entity_id} -> {zone_name}")

    return discovered


async def _create_helper_entities(hass: HomeAssistant, zones: Dict[str, Dict]) -> None:
    """Auto-create required helper entities for discovered zones."""
    if not zones:
        _LOGGER.warning("No zones to create helpers for")
        return

    _LOGGER.info(f"📝 Creating helper entities for {len(zones)} zone(s)...")

    # Create global helpers (once per integration)
    try:
        await hass.services.async_call(
            "input_boolean",
            "create",
            {
                "object_id": "calibration_learning_enabled",
                "name": "Calibration Learning",
                "icon": "mdi:lightbulb-auto",
                "initial": True,
            },
            blocking=True,
        )
        _LOGGER.debug("✓ Created: input_boolean.calibration_learning_enabled")
    except Exception as e:
        _LOGGER.debug(f"  (Skipped learning boolean: already exists or error: {type(e).__name__})")

    try:
        await hass.services.async_call(
            "input_text",
            "create",
            {
                "object_id": "calibration_status",
                "name": "Calibration Status",
                "icon": "mdi:information",
            },
            blocking=True,
        )
        _LOGGER.debug("✓ Created: input_text.calibration_status")
    except Exception as e:
        _LOGGER.debug(f"  (Skipped calibration status: already exists or error: {type(e).__name__})")

    try:
        await hass.services.async_call(
            "input_number",
            "create",
            {
                "object_id": "calibration_tolerance",
                "name": "Calibration Tolerance",
                "unit_of_measurement": "°C",
                "min": 0.5,
                "max": 5.0,
                "step": 0.1,
                "mode": "slider",
                "icon": "mdi:thermometer",
                "initial": 2.0,
            },
            blocking=True,
        )
        _LOGGER.debug("✓ Created: input_number.calibration_tolerance")
    except Exception as e:
        _LOGGER.debug(f"  (Skipped calibration tolerance: already exists or error: {type(e).__name__})")

    # Create per-zone helper entities
    for zone_id, zone_info in zones.items():
        zone_name = zone_info.get("name", zone_id)

        # Create target temperature input number
        try:
            object_id = f"{zone_id}_target"
            await hass.services.async_call(
                "input_number",
                "create",
                {
                    "object_id": object_id,
                    "name": f"{zone_name} Target Temperature",
                    "unit_of_measurement": "°C",
                    "min": 16.0,
                    "max": 30.0,
                    "step": 0.1,
                    "mode": "slider",
                    "icon": "mdi:thermometer",
                    "initial": 22.0,
                },
                blocking=True,
            )
            _LOGGER.debug(f"✓ Created: input_number.{object_id}")
        except Exception as e:
            _LOGGER.debug(f"  (Skipped {zone_name} target: {type(e).__name__})")

        # Create calibration locked toggle
        try:
            object_id = f"{zone_id}_calibration_locked"
            await hass.services.async_call(
                "input_boolean",
                "create",
                {
                    "object_id": object_id,
                    "name": f"{zone_name} Calibration Locked",
                    "icon": "mdi:lock",
                    "initial": False,
                },
                blocking=True,
            )
            _LOGGER.debug(f"✓ Created: input_boolean.{object_id}")
        except Exception as e:
            _LOGGER.debug(f"  (Skipped {zone_name} lock: {type(e).__name__})")

        # Create calibration offset sensor for tracking
        try:
            object_id = f"{zone_id}_calibration_offset"
            await hass.services.async_call(
                "input_number",
                "create",
                {
                    "object_id": object_id,
                    "name": f"{zone_name} Calibration Offset",
                    "unit_of_measurement": "°C",
                    "min": -5.0,
                    "max": 5.0,
                    "step": 0.1,
                    "mode": "box",
                    "icon": "mdi:plus-minus",
                    "initial": 0.0,
                },
                blocking=True,
            )
            _LOGGER.debug(f"✓ Created: input_number.{object_id}")
        except Exception as e:
            _LOGGER.debug(f"  (Skipped {zone_name} offset: {type(e).__name__})")

    _LOGGER.info(f"✅ Created helpers for {len(zones)} zone(s)")


async def _handle_set_zone_temp(call: ServiceCall) -> None:
    """Handle set zone temperature service call."""
    zone_id = call.data.get("zone_id")
    temperature = call.data.get("temperature")

    # Validate inputs
    if not zone_id or not isinstance(zone_id, str):
        _LOGGER.error(f"Invalid service call: zone_id must be a string, got {zone_id}")
        return

    try:
        temp_value = float(temperature)
    except (TypeError, ValueError):
        _LOGGER.error(f"Invalid service call: temperature must be numeric, got {temperature}")
        return

    # Validate temperature range
    if not 16 <= temp_value <= 30:
        _LOGGER.error(f"Invalid temperature {temp_value}°C: must be between 16-30°C")
        return

    _LOGGER.info(f"Setting zone {zone_id} to {temp_value}°C")


async def _handle_toggle_zone(call: ServiceCall) -> None:
    """Handle toggle zone service call."""
    zone_id = call.data.get("zone_id")
    enabled = call.data.get("enabled")

    # Validate inputs
    if not zone_id or not isinstance(zone_id, str):
        _LOGGER.error(f"Invalid service call: zone_id must be a string, got {zone_id}")
        return

    if not isinstance(enabled, bool):
        _LOGGER.error(f"Invalid service call: enabled must be boolean, got {enabled}")
        return

    _LOGGER.info(f"Toggling zone {zone_id} to {enabled}")
