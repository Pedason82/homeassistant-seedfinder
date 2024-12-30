"""Config flow for OpenPlantBook integration."""

from __future__ import annotations

import logging
import os
from typing import Any, Optional, Dict

import voluptuous as vol

from homeassistant import config_entries, core
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    FLOW_DOWNLOAD_IMAGES,
    FLOW_DOWNLOAD_PATH,
    DEFAULT_IMAGE_PATH,
    OPB_INFO_MESSAGE,
    OPB_CURRENT_INFO_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenPlantBook."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Skip upgrade message for new installations
            user_input[OPB_INFO_MESSAGE] = OPB_CURRENT_INFO_MESSAGE
            return self.async_create_entry(title="Seedfinder", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @core.callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        FLOW_DOWNLOAD_IMAGES,
                        default=self.config_entry.options.get(FLOW_DOWNLOAD_IMAGES, False),
                    ): bool,
                    vol.Optional(
                        FLOW_DOWNLOAD_PATH,
                        default=self.config_entry.options.get(FLOW_DOWNLOAD_PATH, ""),
                    ): str,
                }
            ),
        )
