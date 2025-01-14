"""Support for myUplink sensors."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Parameter
from .const import DOMAIN
from .entity import MyUplinkParameterEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[BinarySensorEntity] = []

    for system in coordinator.data:
        for device in system.devices:
            for parameter in device.parameters:
                if parameter.find_fitting_entity() == Platform.BINARY_SENSOR:
                    entities.append(
                        MyUplinkParameterBinarySensorEntity(
                            coordinator, device, parameter
                        )
                    )

    async_add_entities(entities)


class MyUplinkParameterBinarySensorEntity(MyUplinkParameterEntity, BinarySensorEntity):
    """Representation of a myUplink paramater binary sensor."""

    def _update_from_parameter(self, parameter: Parameter) -> None:
        """Update attrs from parameter."""
        super()._update_from_parameter(parameter)
        self._attr_is_on = bool(int(self._parameter.value))

        if self._parameter.id == 10733:
            self._attr_is_on = not bool(int(self._parameter.value))
            self._attr_device_class = BinarySensorDeviceClass.LOCK
        elif self._parameter.id in (10905, 10906):
            self._attr_device_class = BinarySensorDeviceClass.RUNNING
