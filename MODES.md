# Clima Heating & Cooling Modes

Clima supports both **heating mode** (winter) and **cooling mode** (summer), allowing you to use your AC units year-round for optimal comfort.

## Mode Overview

### ❄️ Cooling Mode (Summer)
- Target: Lower indoor temperature
- Use: Spring, summer, fall peak hours
- Setpoint: Typically 18-24°C
- Power indicator color: 🔵 Blue
- Example: "Keep house at 22°C during hot days"

### 🔥 Heating Mode (Winter)
- Target: Raise indoor temperature
- Use: Fall, winter, early spring
- Setpoint: Typically 18-23°C
- Power indicator color: 🟠 Orange
- Example: "Warm up bedroom to 21°C on cold mornings"

---

## Switching Modes

### Manual Mode Switching

**In Dashboard:**
1. Open Climate Dashboard
2. Each zone card has mode buttons:
   - ❄️ **Cool** - Cooling mode
   - 🔥 **Heat** - Heating mode
3. Click the button to switch

**In Home Assistant:**
```yaml
# Set zone to heating mode
service: climate.set_hvac_mode
target:
  entity_id: climate.bedroom_ac
data:
  hvac_mode: heat

# Set zone to cooling mode
service: climate.set_hvac_mode
target:
  entity_id: climate.bedroom_ac
data:
  hvac_mode: cool
```

### Automatic Mode Switching

**Based on Outside Temperature:**
```yaml
# Switch to heating when cold
- alias: "Auto: Switch to heating (<10°C)"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    below: 10
    for:
      days: 3
  action:
    - service: climate.set_hvac_mode
      target:
        entity_id: climate.bedroom_ac
      data:
        hvac_mode: heat

# Switch to cooling when warm
- alias: "Auto: Switch to cooling (>20°C)"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    above: 20
    for:
      days: 3
  action:
    - service: climate.set_hvac_mode
      target:
        entity_id: climate.bedroom_ac
      data:
        hvac_mode: cool
```

**Based on Season:**
```yaml
# Winter heating (Dec-Feb)
- alias: "Seasonal: Winter heating mode"
  trigger:
    platform: numeric_state
    entity_id: sensor.month
    value_template: "{{ now().month }}"
    below: 3
  action:
    - service: climate.set_hvac_mode
      target:
        entity_id: climate.bedroom_ac
      data:
        hvac_mode: heat

# Summer cooling (Jun-Aug)
- alias: "Seasonal: Summer cooling mode"
  trigger:
    platform: numeric_state
    entity_id: sensor.month
    value_template: "{{ now().month }}"
    above: 5
  action:
    - service: climate.set_hvac_mode
      target:
        entity_id: climate.bedroom_ac
      data:
        hvac_mode: cool
```

---

## Temperature Setpoints by Mode

### Heating Setpoints (Winter)
```
Living Areas:     20-22°C
Bedrooms:         19-21°C  
Office:           19-21°C
Basement/Extra:   15-18°C (freeze protection minimum)

Outside Temp     Recommended Setpoint
<-5°C            23°C (freeze protection mode)
-5 to 0°C        23°C (very cold)
0 to 10°C        22°C (cold)
10 to 15°C       21°C (cool)
15 to 20°C       20°C (mild, transition)
```

### Cooling Setpoints (Summer)
```
Living Areas:     22-24°C
Bedrooms:         20-22°C
Office:           20-21°C
Basement/Extra:   Not needed (cooler naturally)

Outside Temp     Recommended Setpoint
>35°C            24°C (extreme heat)
30-35°C          23°C (very hot)
25-30°C          22°C (hot)
20-25°C          21°C (warm)
<20°C            Off (too cool outside)
```

---

## Winter Heating Guide

### Heating Seasons
- **Late Fall** (Oct-Nov): Transition to heating as temps drop
- **Winter** (Dec-Feb): Primary heating season
- **Early Spring** (Mar): Continue heating until stable warm days

### Best Heating Practices

**1. Freeze Protection**
- Maintain minimum 15°C in all areas
- Prevent water pipe freezing
- Automatic in extreme cold (<-5°C)

```yaml
- alias: "Freeze Protection Minimum"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    below: 0
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: 15
        hvac_mode: heat
```

**2. Energy Efficiency**
- Heat only occupied zones during the day
- Lower temps (18-19°C) overnight in bedrooms
- Close doors to unused rooms

```yaml
- alias: "Efficient Heating: Night mode"
  trigger:
    platform: time
    at: "23:00:00"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 16  # Save energy
        hvac_mode: heat
```

**3. Humidity Control**
- Keep humidity 30-50% to prevent mold and condensation
- Heating lowers humidity naturally
- Boost heat slightly if humidity >70%

```yaml
- alias: "Humidity Control During Heating"
  trigger:
    platform: numeric_state
    entity_id: sensor.indoor_humidity
    above: 70
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: 23  # Slightly higher
        hvac_mode: heat
```

**4. Window Management**
- Keep windows closed during heating
- Disable heating if windows are open
- Resume when windows close

```yaml
- alias: "Stop Heating When Window Opens"
  trigger:
    platform: state
    entity_id: binary_sensor.bedroom_window
    to: "on"
  action:
    - service: climate.turn_off
      target:
        entity_id: climate.bedroom_ac
    - service: notify.notify
      data:
        message: "Heating disabled - window open"
```

---

## Summer Cooling Guide

### Cooling Seasons
- **Late Spring** (May): Start cooling as temps rise
- **Summer** (Jun-Aug): Peak cooling season
- **Early Fall** (Sep): Continue until stable cool days

### Best Cooling Practices

**1. Peak Load Management**
- Pre-cool in early morning before peak heat
- Raise setpoint slightly during peak hours (2-5 PM)
- Use deeper cooling only when necessary

```yaml
- alias: "Smart Cooling: Peak hours adjustment"
  trigger:
    platform: time
    at: "14:00:00"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 24  # Slightly higher during peak
        hvac_mode: cool

- alias: "Smart Cooling: Reset after peak"
  trigger:
    platform: time
    at: "17:00:00"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 22  # Back to normal
        hvac_mode: cool
```

**2. Natural Cooling**
- Close blinds/curtains during hot hours
- Cross-ventilate at night if outside <22°C
- Turn off AC during cool mornings

```yaml
- alias: "Natural Cooling: Turn off AC at night"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    below: 20
    at_night: true
  action:
    - service: homeassistant.turn_off
      target:
        entity_id: climate.living_room_ac
```

**3. Window Smart Control**
- Open windows when it's cooler outside
- Close windows before heating outside air
- Smart window control reduces AC load

```yaml
- alias: "Smart Cooling: Open window when cooler"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    below: "{{ states('sensor.indoor_temp') | float - 2 }}"
  action:
    - service: notify.notify
      data:
        message: "Outside temp is cooler - consider opening windows"
```

---

## Mode-Specific Automations

### Winter Heating Automations
See `example_heating_automations.yaml` for complete examples:
- Morning heating start
- Freeze protection
- Adaptive heating (outside temp based)
- Window open detection
- Workday/weekend schedules
- Humidity control

### Summer Cooling Automations
See `example_automations.yaml` for complete examples:
- Auto off when window opens
- Temperature-based adjustment
- Peak hour load shifting
- All windows open safety
- Presence-based control

---

## Energy Consumption: Heat vs Cool

**Typical Winter Usage (6°C outside, 22°C target):**
```
Per Zone Per Day:  5-8 kWh
Total (6 zones):   30-48 kWh
Monthly:           900-1440 kWh
Cost (~$0.24/kWh): $216-345
```

**Typical Summer Usage (35°C outside, 22°C target):**
```
Per Zone Per Day:  4-6 kWh
Total (6 zones):   24-36 kWh
Monthly:           720-1080 kWh
Cost (~$0.24/kWh): $173-260
```

**Factors affecting consumption:**
- Outdoor temperature difference
- Insulation quality
- Zone occupancy
- Setpoint temperature
- Operating hours

---

## Troubleshooting Mode Issues

### Heating Not Working
**Check:**
1. Mode is set to "heat": `climate.bedroom_ac` has `hvac_mode: heat`
2. Temperature setpoint > current temp
3. Unit is powered on
4. AC supports heating (heat pump required)

**Fix:**
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.bedroom_ac
data:
  hvac_mode: heat
```

### Cooling Not Working
**Check:**
1. Mode is set to "cool": `climate.bedroom_ac` has `hvac_mode: cool`
2. Temperature setpoint < current temp
3. Unit is powered on
4. AC has cooling capability

**Fix:**
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.bedroom_ac
data:
  hvac_mode: cool
```

### Mode Not Switching
**Check:**
1. Automation is enabled
2. Conditions are met (outside temp, time, etc.)
3. Entity ID is correct
4. AC supports the requested mode

**Debug:**
```yaml
service: notify.notify
data:
  message: "Mode: {{ state_attr('climate.bedroom_ac', 'hvac_mode') }} | Temp: {{ states('sensor.bedroom_temperature') }}"
```

### Wrong Mode Active
**Check:**
1. Manual mode button (conflicts with automations)
2. Multiple automations fighting for control
3. User manually override recent changes

**Prevent:**
Use `conditions` to ensure only one automation triggers at a time:
```yaml
condition:
  - condition: state
    entity_id: input_boolean.manual_heating_mode
    state: "off"  # Only auto if manual is off
```

---

## Best Practices Summary

✅ **DO:**
- Use automations for seasonal transitions
- Maintain consistent setpoints
- Use freeze protection in winter
- Monitor power consumption
- Test mode switches manually first

❌ **DON'T:**
- Leave windows open in cooling mode
- Use heating in 25°C+ temperatures
- Set extreme setpoints (>28°C or <16°C)
- Run multiple conflicting automations
- Ignore freeze protection warnings

---

## Resources

- **Climate Entity Docs**: https://www.home-assistant.io/integrations/climate/
- **HVAC Modes**: https://www.home-assistant.io/integrations/climate/#hvac-modes
- **Midea Integration**: https://www.home-assistant.io/integrations/midea_ac/

---

## Support

Questions about modes?
- Check Home Assistant logs: `Settings → System → Logs`
- Review current mode: `{{ state_attr('climate.bedroom_ac', 'hvac_mode') }}`
- Report issues: https://github.com/estebanbascur/clima/issues
