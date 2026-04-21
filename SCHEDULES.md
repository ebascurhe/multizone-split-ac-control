# Clima Schedules Guide

Create automated AC schedules to control your zones at specific times. Schedules work with Home Assistant automations to provide powerful scheduling capabilities.

## Quick Start

### 1. Open Schedule Manager
```bash
open schedules.html
```

### 2. Create Your First Schedule
- Click **+ Create Schedule**
- Select a zone
- Set days of week (e.g., Mon-Fri for work days)
- Define time periods with temperatures
- Click **Save**

### 3. Enable Automations
Copy the examples from `example_schedules.yaml` into your Home Assistant automations and customize as needed.

---

## Schedule Types

### Simple Time-Based
Turn AC on/off at specific times with a fixed temperature.

**Example: Office 9 AM - 6 PM at 21°C**
```yaml
- alias: "Office: Work hours cooling"
  trigger:
    platform: time
    at: "09:00:00"
  action:
    - service: climate.turn_on
      target:
        entity_id: climate.office_ac
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 21
```

### Multi-Period Schedules
Different temperatures at different times of day.

**Example: Bedroom with morning (22°C) and evening (20°C) settings**
```yaml
- alias: "Bedroom: Morning cooling"
  trigger:
    platform: time
    at: "08:00:00"
  action:
    - service: climate.turn_on
      target:
        entity_id: climate.bedroom_ac
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: 22

- alias: "Bedroom: Evening cooling"
  trigger:
    platform: time
    at: "20:00:00"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: 20
```

### Workday-Based
Run schedules only on workdays or weekends.

**Example: Office only on workdays**
```yaml
- alias: "Office: Weekday cooling"
  trigger:
    platform: time
    at: "09:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday  # Requires Workday integration
      state: "on"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 21
```

### Presence-Based
Respond to people arriving home or leaving.

**Example: Away mode**
```yaml
- alias: "Climate: Away mode"
  trigger:
    platform: state
    entity_id: group.all_people
    to: "not_home"
  action:
    - service: homeassistant.turn_off
      target:
        entity_id: climate.living_room_ac
```

### Temperature-Adaptive
Adjust setpoints based on outside temperature.

**Example: Hot day adjustment**
```yaml
- alias: "Climate: Adjust for hot outside"
  trigger:
    platform: numeric_state
    entity_id: sensor.outdoor_temp
    above: 30
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 23  # Higher setpoint on hot days
```

---

## Preset Schedules

### 🏢 Office Hours
- **Weekdays**: Cool 9 AM - 6 PM at 21°C
- **Weekends**: Off
- **Best for**: Home offices, commercial spaces

### 🏠 Home Default
- **Living areas**: 8 AM - 11 PM at 22°C
- **Bedrooms**: 8 PM - 7 AM at 20°C
- **Off**: During the day on weekdays
- **Best for**: Residential homes

### ⚡ Energy Saver
- **Minimal cooling**: Only 7-9 AM and 7-9 PM
- **Higher temps**: 24-25°C during peak hours
- **Off**: Rest of the day
- **Best for**: Budget-conscious users

### ❄️ Always Cool
- **24/7 cooling** at consistent temperature
- **All days** of the week
- **No breaks** or adjustments
- **Best for**: Temperature-sensitive areas, data centers

---

## Advanced Scheduling

### Combining Conditions
Run automations only when multiple conditions are met.

```yaml
- alias: "Office: Cool only when occupied"
  trigger:
    platform: time
    at: "09:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "on"
    - condition: device_tracker.john_location
      state: "home"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 21
```

### Time-Range Conditions
Only trigger schedules within a specific time range.

```yaml
- alias: "Living Room: Afternoon boost"
  trigger:
    platform: time
    at: "14:00:00"
  condition:
    - condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 19  # Extra cool in afternoon
```

### Dynamic Temperature
Set temperature based on sensor values.

```yaml
- alias: "Climate: Dynamic temp adjustment"
  trigger:
    platform: numeric_state
    entity_id: sensor.current_humidity
    above: 70
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: "{{ 19 if states('sensor.current_humidity') | float > 80 else 21 }}"
```

---

## Best Practices

### 1. **Stagger Times**
Don't start multiple ACs at the exact same time to avoid power spikes:
```yaml
# Good: Staggered starts
- time: "08:00:00"  # Zone 1
- time: "08:05:00"  # Zone 2
- time: "08:10:00"  # Zone 3

# Bad: All at once
- time: "08:00:00"  # All zones
```

### 2. **Use Workday Sensor**
Install the Workday integration to automatically handle holidays:
```yaml
condition:
  - condition: state
    entity_id: binary_sensor.workday
    state: "on"
```

### 3. **Gradual Temperature Changes**
Use small steps rather than large jumps:
```yaml
# Good: Gradual
- 22°C at 8 AM
- 21°C at 12 PM
- 22°C at 6 PM

# Less efficient: Large jumps
- 22°C at 8 AM
- 18°C at 12 PM (too cold, energy wasted)
```

### 4. **Group Related Automations**
Use zones consistently across automations:
```yaml
# Create groups for easy management
group:
  climate_living_areas:
    entities:
      - climate.living_room_ac
      - climate.office_ac
  
  climate_bedrooms:
    entities:
      - climate.bedroom_ac
      - climate.master_bedroom_ac

# Then use in automations
action:
  - service: climate.set_temperature
    target:
      entity_id: group.climate_living_areas
    data:
      temperature: 21
```

### 5. **Test Before Deployment**
Create test automations during off-peak hours:
```yaml
- alias: "[TEST] Living Room Schedule"
  trigger:
    platform: time
    at: "14:30:00"  # Test time during the day
  action:
    # ... test action
```

### 6. **Monitor Energy Impact**
Track consumption changes after adding schedules:
- Check daily kWh consumption
- Compare with previous months
- Adjust temperatures if needed

### 7. **Use Automation Docs**
Document your schedule logic:
```yaml
- alias: "Office: Work hours cooling"
  description: |
    Cool office during work hours (9 AM - 6 PM)
    Workdays only. Temperature: 21°C
    Purpose: Balance comfort and energy savings
  trigger:
    platform: time
    at: "09:00:00"
  # ...
```

---

## Troubleshooting

### Schedule Not Triggering

**Problem**: Automation doesn't run at the scheduled time.

**Solutions**:
1. Check Home Assistant logs: `Settings → System → Logs`
2. Verify trigger time is correct (24-hour format)
3. Check entity IDs are correct
4. Test with a manual trigger: Click "Execute" on automation

### Temperature Not Changing

**Problem**: AC is on but temperature isn't updating.

**Solutions**:
1. Verify AC entity exists: `Settings → Devices & Services → Entities`
2. Check AC is in "climate" domain (not "switch")
3. Test manually: Use climate card to change temp
4. Check for conflicting automations

### Schedules Conflict

**Problem**: Multiple schedules changing temps at same time.

**Solutions**:
1. Review all automations (use automation editor)
2. Stagger trigger times by a few minutes
3. Use conditions to prevent overlaps:
   ```yaml
   condition:
     - condition: not
       conditions:
         - condition: state
           entity_id: automation.other_office_automation
           state: "on"
   ```

### Performance Issues

**Problem**: Too many automations causing delays.

**Solutions**:
1. Group automations:
   ```yaml
   id: office_morning_routine
   ```
2. Use `wait_template` instead of multiple automations
3. Consolidate related automations

---

## Example Daily Schedule

Here's a complete example for a home setup:

```yaml
# Morning routine (7 AM - 9 AM)
- alias: "Morning: Prepare house"
  trigger:
    platform: time
    at: "07:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "on"
  action:
    - service: climate.turn_on
      target:
        entity_id:
          - climate.living_room_ac
          - climate.office_ac
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 21

# Work hours (9 AM - 5 PM)
- alias: "Work: Peak cooling"
  trigger:
    platform: time
    at: "09:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "on"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.office_ac
      data:
        temperature: 20

# Evening (5 PM - 11 PM)
- alias: "Evening: Living areas"
  trigger:
    platform: time
    at: "17:00:00"
  action:
    - service: climate.turn_on
      target:
        entity_id: climate.living_room_ac
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 21

# Night (11 PM - 7 AM)
- alias: "Night: Bedroom only"
  trigger:
    platform: time
    at: "23:00:00"
  action:
    - service: homeassistant.turn_off
      target:
        entity_id:
          - climate.living_room_ac
          - climate.office_ac
    - service: climate.turn_on
      target:
        entity_id: climate.bedroom_ac
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: 20

# Weekend (different schedule)
- alias: "Weekend: Relaxed cooling"
  trigger:
    platform: time
    at: "09:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "off"
  action:
    - service: climate.turn_on
      target:
        entity_id:
          - climate.living_room_ac
          - climate.bedroom_ac
    - service: climate.set_temperature
      target:
        entity_id:
          - climate.living_room_ac
          - climate.bedroom_ac
      data:
        temperature: 22
```

---

## Resources

- **Home Assistant Automations**: https://www.home-assistant.io/docs/automation/
- **Workday Integration**: https://www.home-assistant.io/integrations/workday/
- **Time Trigger**: https://www.home-assistant.io/integrations/time/
- **Condition Templates**: https://www.home-assistant.io/docs/automation/templating/

---

## Support

For issues or questions about Clima schedules:
- Check logs: `Settings → System → Logs`
- Review automation editor: `Settings → Automations & Scenes`
- Test manually using climate card
- Report issues: https://github.com/estebanbascur/clima/issues
