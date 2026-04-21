# Clima - Multi-Zone AC Controller

A Home Assistant custom integration for managing multiple independent AC units across different zones/rooms with integrated temperature and window sensors.

## Features

✨ **Multi-Zone Support** - Control up to 6 independent AC units simultaneously
🌡️ **Temperature Monitoring** - Track temperature from BLE sensors per zone
🪟 **Window Detection** - Automatically detect open windows via Zigbee sensors
📊 **Outside Temperature** - Factor in external temperature for smart control
📱 **Dashboard UI** - Intuitive dashboards with Home Assistant-style sidebar navigation
🔄 **Automations** - Pre-built automation examples for common scenarios
🌐 **WiFi Based** - Works with Midea and other WiFi-connected AC units
📈 **Smart Calibration** - Automatic temperature offset learning and adjustment
⚡ **Energy Tracking** - Monitor energy consumption and efficiency

## Requirements

- Home Assistant 2024.1.0 or later
- Midea AC integration (or compatible WiFi AC units)
- Zigbee coordinator (for window sensors)
- BLE device tracker (for temperature sensors)

## Installation

### Via HACS (Recommended)

1. Go to **Settings → Devices & Services → HACS**
2. Click **Explore & Download Repositories**
3. Search for "Clima"
4. Click **Download**
5. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/clima` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Create Integration**
4. Search for "Clima" and follow the setup wizard

## Configuration

### Step 1: Add to Home Assistant

1. Go to **Settings → Devices & Services**
2. Click **Create Integration**
3. Search for "Clima"

### Step 2: Map Your Entities

The setup wizard will ask you to map:
- **AC Unit** (climate entity) - One per zone
- **Temperature Sensor** (sensor entity) - BLE temperature sensor per zone
- **Window Sensor** (binary_sensor entity) - Zigbee window contact per zone
- **Outside Temperature** (sensor entity) - Optional, global

### Example Entity Mapping

```
Zone 1 (Bedroom):
  AC Unit: climate.bedroom_ac
  Temperature: sensor.bedroom_temperature
  Window: binary_sensor.bedroom_window

Zone 2 (Living Room):
  AC Unit: climate.living_room_ac
  Temperature: sensor.living_room_temperature
  Window: binary_sensor.living_room_window

Outside:
  Temperature: sensor.outdoor_temperature
```

## Dashboard Setup

Clima includes a main dashboard with Home Assistant-style sidebar navigation that provides access to all features.

### Main Dashboard (index.html)

Access the main hub at:
```
http://your-home-assistant-ip:8123/local/index.html
```

Features:
- 🎯 **Home** - Overview and feature highlights
- 🌡️ **Calibration** - Temperature offset learning and adjustment
- 📊 **Overview** - Real-time monitoring of all zones
- 🔥 **Heating** - Winter heating mode controls
- ⏰ **Schedules** - Automated temperature scheduling
- ⚡ **Energy** - Energy consumption analytics

### Available Dashboards

- **index.html** - Main hub with sidebar navigation
- **calibration_dashboard.html** - Temperature calibration management
- **dashboard_preview.html** - Zone overview and monitoring
- **dashboard_heating.html** - Winter heating mode controls
- **schedules.html** - Temperature scheduling interface
- **energy_analytics.html** - Energy tracking and analysis

### Custom Lovelace Dashboard

To create a custom Home Assistant Lovelace dashboard:
1. Go to **Settings → Dashboards**
2. Click **Create Dashboard**
3. Use the card editor to add climate, sensor, and input entities
4. Customize layout to match your preferences

## Automations

Pre-built automation examples are included in `example_automations.yaml`. These include:

- ✅ Turn off AC when window opens
- ✅ Turn back on when window closes
- ✅ Adjust temperature based on outside conditions
- ✅ Turn off all ACs if all windows are open
- ✅ Temperature deviation alerts

Copy these to your `automations.yaml` and customize as needed.

## Services

### `clima.set_zone_temperature`

Set the target temperature for a specific zone.

```yaml
service: clima.set_zone_temperature
data:
  zone_id: "zone_1"
  temperature: 22
```

### `clima.toggle_zone`

Enable/disable AC for a specific zone.

```yaml
service: clima.toggle_zone
data:
  zone_id: "zone_1"
  enabled: true
```

## Troubleshooting

### Integration doesn't appear in setup wizard

- Ensure you've installed it correctly and restarted Home Assistant
- Check `Settings → Devices & Services → HACS` to verify installation

### Entities not appearing

- Verify your Midea, Zigbee, and BLE integrations are properly set up
- Check that entities exist in **Settings → Devices & Services → Entities**

### Automations not triggering

- Verify the entity IDs match exactly (case-sensitive)
- Check the automation logs in **Settings → System → Logs**

## Supported Devices

- **AC Units**: Midea (via official integration), and any WiFi-controlled units with Home Assistant support
- **Temperature Sensors**: Any BLE temperature sensor (Xiaomi, LYWSD, etc.)
- **Window Sensors**: Any Zigbee door/window contact sensor
- **Outside Temperature**: Any temperature sensor entity

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This integration is released under the MIT License. See LICENSE file for details.

## Support

For issues and feature requests, please open an issue on [GitHub](https://github.com/estebanbascur/clima/issues).

## Changelog

### 0.1.0 (Initial Release)

- Multi-zone AC control
- Temperature and window sensor integration
- Dashboard examples
- Automation templates
- Config flow setup wizard

## Author

Created by [@estebanbascur](https://github.com/estebanbascur)
