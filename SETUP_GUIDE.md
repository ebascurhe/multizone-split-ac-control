# Clima Setup Guide

This guide will help you set up the Clima integration in your Home Assistant instance.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Midea AC integration installed and connected to all 6 units
- [ ] Zigbee coordinator set up with window contact sensors
- [ ] BLE adapter configured with temperature sensors
- [ ] Home Assistant 2024.1.0 or later
- [ ] All entities visible in **Settings → Devices & Services → Entities**

## Step-by-Step Setup

### 1. Install Clima

#### Option A: Via HACS
```
Settings → Devices & Services → HACS → Explore & Download → Search "Clima" → Download
```

#### Option B: Manual
Copy `custom_components/clima` to your `~/.homeassistant/custom_components/` folder.

**Restart Home Assistant** after installation.

### 2. Verify Your Entities

Before configuring Clima, verify all your entities exist:

1. Go to **Settings → Devices & Services → Entities**
2. Search for each entity type:
   - Climate: `climate.zone_*_ac` (6 units)
   - Sensor: `sensor.zone_*_temperature` (6 sensors)
   - Binary Sensor: `binary_sensor.zone_*_window` (6 sensors)
   - Sensor: `sensor.outdoor_temperature` (outside temperature)

**Note:** Entity names may differ. Write down the exact entity IDs - you'll need them in the next step.

### 3. Create Clima Integration

1. Go to **Settings → Devices & Services**
2. Click **Create Integration** (bottom right)
3. Search for "Clima"
4. Select "Clima - Multi-Zone AC Controller"
5. Choose your outside temperature sensor (optional)
6. Click "Create"

### 4. Configure Your Zones

After creating the integration, you'll need to configure each zone:

```yaml
Zone 1: Bedroom
  AC Unit: climate.bedroom_ac
  Temperature Sensor: sensor.bedroom_temperature
  Window Sensor: binary_sensor.bedroom_window

Zone 2: Living Room
  AC Unit: climate.living_room_ac
  Temperature Sensor: sensor.living_room_temperature
  Window Sensor: binary_sensor.living_room_window

[Continue for zones 3-6]
```

### 5. Create Dashboard

1. Go to **Settings → Dashboards**
2. Create a new dashboard named "Climate"
3. Click **Edit Dashboard**
4. Use the YAML from `example_lovelace_dashboard.yaml`
5. Replace entity IDs with your actual entities
6. Save

### 6. Set Up Automations (Optional)

1. Go to **Settings → Automations & Scenes**
2. Create new automations from `example_automations.yaml`
3. Update entity IDs to match your setup
4. Test each automation

## Example Entity Mapping

Here's a complete example mapping for a 6-zone setup:

```
CLIMATE ENTITIES (AC Units):
- climate.sala_ac          → Zone 1: Sala
- climate.cocina_ac        → Zone 2: Kitchen
- climate.principal_ac     → Zone 3: Master Bedroom
- climate.guest_ac         → Zone 4: Guest Room
- climate.office_ac        → Zone 5: Office
- climate.laundry_ac       → Zone 6: Laundry

TEMPERATURE SENSORS (BLE):
- sensor.sala_temp         → Zone 1
- sensor.cocina_temp       → Zone 2
- sensor.principal_temp    → Zone 3
- sensor.guest_temp        → Zone 4
- sensor.office_temp       → Zone 5
- sensor.laundry_temp      → Zone 6

WINDOW SENSORS (Zigbee):
- binary_sensor.sala_window         → Zone 1
- binary_sensor.cocina_window       → Zone 2
- binary_sensor.principal_window    → Zone 3
- binary_sensor.guest_window        → Zone 4
- binary_sensor.office_window       → Zone 5
- binary_sensor.laundry_window      → Zone 6

OUTSIDE TEMPERATURE:
- sensor.outdoor_temp
```

## Troubleshooting

### Integration not appearing in setup wizard

**Solution:**
- Verify installation: Check if `custom_components/clima/` exists
- Restart Home Assistant completely (not just reload)
- Clear browser cache

### "Unknown entity" errors in logs

**Solution:**
- Verify entity IDs exist in **Entities** list
- Check for typos (entity IDs are case-sensitive)
- Update YAML files with correct entity IDs

### Automations not triggering

**Solution:**
- Verify entity IDs match exactly
- Check **Settings → System → Logs** for errors
- Test automation manually by clicking "Execute"

### Zone not responding to commands

**Solution:**
- Verify Midea integration is working
- Test AC unit directly through Midea app
- Check Home Assistant logs for errors
- Restart Midea integration

## Next Steps

1. ✅ Install Clima
2. ✅ Configure zones
3. ✅ Create dashboard
4. ✅ Set up automations
5. Create custom automations for your needs
6. Share feedback or report issues

## Getting Help

- **Documentation:** Check README.md for detailed information
- **Issues:** Report bugs at https://github.com/estebanbascur/clima/issues
- **Home Assistant Forums:** Post in the Home Assistant community forum
- **Home Assistant Logs:** Always include relevant logs when asking for help

Happy controlling! 🌡️❄️
