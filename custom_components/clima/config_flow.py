"""Config flow for Clima integration."""

from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_ZONES,
    CONF_ZONE_NAME,
    CONF_AC_ENTITY,
    CONF_TEMP_SENSOR,
    CONF_WINDOW_SENSOR,
    CONF_OUTSIDE_TEMP,
)


class ClimaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Clima."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Clima AC Controller",
                data=user_input,
            )

        # Get available entities
        climate_entities = self._get_climate_entities()
        sensor_entities = self._get_sensor_entities()
        binary_sensor_entities = self._get_binary_sensor_entities()

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_OUTSIDE_TEMP,
                    description={"suggested_value": ""},
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={
                "zones_info": "You'll configure your 6 zones in the next step"
            },
        )

    async def async_step_zones(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Configure individual zones."""
        if user_input is not None:
            # Store all zones data
            self.config_data[CONF_ZONES] = user_input.get(CONF_ZONES, [])
            return self.async_create_entry(
                title="Clima AC Controller",
                data=self.config_data,
            )

        # This will be handled by async_step_user for now
        return self.async_abort(reason="single_instance_allowed")

    def _get_climate_entities(self) -> Dict[str, str]:
        """Get available climate entities."""
        entities = {}
        hass = self.hass
        if hass:
            state = hass.states.async_all()
            for entity in state:
                if entity.entity_id.startswith("climate."):
                    entities[entity.entity_id] = entity.attributes.get(
                        "friendly_name", entity.entity_id
                    )
        return entities

    def _get_sensor_entities(self) -> Dict[str, str]:
        """Get available temperature sensor entities."""
        entities = {}
        hass = self.hass
        if hass:
            state = hass.states.async_all()
            for entity in state:
                if entity.entity_id.startswith("sensor."):
                    entities[entity.entity_id] = entity.attributes.get(
                        "friendly_name", entity.entity_id
                    )
        return entities

    def _get_binary_sensor_entities(self) -> Dict[str, str]:
        """Get available binary sensor entities."""
        entities = {}
        hass = self.hass
        if hass:
            state = hass.states.async_all()
            for entity in state:
                if entity.entity_id.startswith("binary_sensor."):
                    entities[entity.entity_id] = entity.attributes.get(
                        "friendly_name", entity.entity_id
                    )
        return entities

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this integration."""
        return ClimaOptionsFlow(config_entry)


class ClimaOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Clima."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_OUTSIDE_TEMP,
                    default=self.config_entry.data.get(CONF_OUTSIDE_TEMP, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
