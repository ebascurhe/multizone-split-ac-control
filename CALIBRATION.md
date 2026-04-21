# Temperature Calibration System

The Clima temperature calibration system automatically learns the offset between your AC unit's temperature setpoint and your external sensor readings, then automatically adjusts the setpoint to reach your target temperature.

## 🎯 Why Calibration Matters

Different AC units and sensor placements create temperature variations:

**Example:**
- You set AC to 22°C (setpoint)
- Your external sensor reads 20°C (actual room temp)
- Difference = 2°C offset

**Without calibration:**
- You think the room is 22°C, but it's actually 20°C
- You stay cold!

**With calibration:**
- System learns: This zone needs +2°C adjustment
- Next time you want 22°C, system sets AC to 24°C
- Your external sensor reads 22°C ✅ Perfect!

## How It Works

### Learning Phase (Automatic)

1. **Collection**: System records AC setpoint vs. external sensor for each zone
2. **Analysis**: After 5+ samples, system calculates average offset
3. **Learning**: If offset is consistent, system learns it
4. **Stabilization**: System continues collecting samples to refine offset

### Application Phase (Automatic)

1. **Target Set**: You set desired temperature (22°C)
2. **Adjustment**: System adds learned offset (+2°C = 24°C)
3. **Setpoint**: AC unit receives adjusted setpoint (24°C)
4. **Result**: External sensor reads target temp (22°C) ✅

### Locking Phase (Manual)

When you're satisfied with calibration:
1. Click **Lock** on the calibration dashboard
2. System stops learning for that zone
3. Uses fixed offset going forward
4. No drift or unwanted adjustments

## Dashboard

**Open the calibration dashboard:**
```bash
open /Users/estebanbascur/claude/projects/clima/calibration_dashboard.html
```

### Dashboard Features

- ✅ View current offset for each zone
- ✅ See learning status (Learning/Ready/Locked)
- ✅ Monitor number of samples collected
- ✅ View min/max/average offset ranges
- ✅ Lock/unlock calibration
- ✅ Reset individual zones
- ✅ Enable/disable global learning

### Reading the Dashboard

**Status Indicators:**
- 🟢 **Ready**: Calibration complete, accurate, and unlocked
- 🟠 **Learning**: Still collecting samples to refine offset
- 🔒 **Locked**: Calibration complete and locked (no further learning)
- ⏳ **Not Calibrated**: No data yet, waiting to collect samples

**Metrics Shown:**
- **Current Offset**: Applied adjustment (e.g., +0.5°C, -1.2°C)
- **Status**: Learning/Ready/Locked with sample count
- **Range**: Min/Max/Avg from all collected samples

## Configuration

### Required Helpers

Create these in Home Assistant **Settings → Devices & Services → Helpers**:

**Input Boolean:**
```yaml
input_boolean:
  calibration_learning_enabled:
    name: Calibration Learning
    icon: mdi:lightbulb-auto

  calibration_debug_mode:
    name: Calibration Debug Mode
    icon: mdi:bug
```

**Input Number (one per zone):**
```yaml
input_number:
  bedroom_target:
    name: Bedroom Target Temperature
    unit_of_measurement: "°C"
    min: 16
    max: 30
    step: 0.1
    icon: mdi:thermometer

  living_room_target:
    name: Living Room Target Temperature
    unit_of_measurement: "°C"
    min: 16
    max: 30
    step: 0.1
    icon: mdi:thermometer
  
  # ... repeat for other zones
```

**Sensors (for tracking):**
```yaml
template:
  - sensor:
      - name: "Last Recalibration Date"
        unique_id: "last_recalibration"
        state: "{{ now().isoformat() }}"

      - name: "Bedroom Calibration Variance"
        unique_id: "bedroom_cal_variance"
        unit_of_measurement: "°C"
        state: |
          {%- set offset = state_attr('climate.bedroom_ac', 'current_offset') | float(0) -%}
          {{ offset | abs }}
```

## Automations

Add calibration automations to `automations.yaml`:

```yaml
# Main calibration learning cycle
- alias: "Calibration: Learning cycle"
  trigger:
    platform: time_pattern
    minutes: "/1"  # Run every minute
  condition:
    - condition: state
      entity_id: input_boolean.calibration_learning_enabled
      state: "on"
    - condition: state
      entity_id: climate.bedroom_ac
      state:
        - "cooling"
        - "heating"
  action:
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        # Adjust setpoint based on learned offset
        temperature: |
          {%- set target = states('input_number.bedroom_target') | float(22) -%}
          {%- set offset = state_attr('climate.bedroom_ac', 'current_offset') | float(0) -%}
          {{ target + offset }}
```

See `example_calibration_automations.yaml` for complete automation examples.

## Usage Guide

### Initial Setup (First Time)

1. **Enable Learning Mode**
   - Open calibration dashboard
   - Toggle "Learning Status: Active"

2. **Run AC Units**
   - Turn on all AC units
   - Let them run for 30+ minutes
   - System collects temperature readings

3. **Monitor Progress**
   - Watch dashboard for "Learning..." status
   - Each zone needs 5+ samples
   - Offsets should stabilize after 10+ samples

4. **Lock When Ready**
   - Once "Ready" status appears
   - Offset values stop changing
   - Click "Lock" to finalize calibration

### Ongoing Use

**Manual Adjustment:**
```yaml
# Set temperature via helper
service: input_number.set_value
target:
  entity_id: input_number.bedroom_target
data:
  value: 22
```

System automatically adjusts AC setpoint:
- Target: 22°C
- Learned offset: +1°C
- AC setpoint: 23°C
- External sensor: reads 22°C ✅

**Checking Status:**
```yaml
# View current offset
{{ state_attr('climate.bedroom_ac', 'current_offset') }}
# Returns: +1.0 (or -0.5, etc.)
```

### Seasonal Recalibration

Every 3 months, recalibrate:

1. **Reset Learning**
   - Open dashboard
   - Click "Reset All" OR "Reset" per zone
   - Clears old calibration data

2. **Re-enable Learning**
   - Toggle learning mode on
   - Run AC for 30+ minutes
   - System learns new offsets

3. **Lock New Calibration**
   - Once stable, lock again

**Why seasonal?**
- AC efficiency changes with season
- Room characteristics change
- Dust buildup in filters
- External temperature ranges differ

## Tolerance & Thresholds

### Tolerance Setting (±2°C)

The system allows a tolerance window:
- If offset is within ±2°C → Considered acceptable
- If offset exceeds ±2°C → Continues learning

**Change tolerance:**
```yaml
# In calibration dashboard: Tolerance field
# Or via automation:
service: input_number.set_value
target:
  entity_id: input_number.calibration_tolerance
data:
  value: 2.0  # ±2°C
```

### Learning Threshold (0.5°C)

System only updates offset if change is ≥0.5°C:
- Prevents noise and small fluctuations
- Waits for significant changes to apply
- More stable long-term offset

## Troubleshooting

### Calibration Not Working

**Check:**
1. Learning mode is enabled
2. AC unit is running
3. External sensor is powered on
4. Automation is triggered

**Fix:**
```yaml
# Check current state
{{ states('climate.bedroom_ac') }}  # Should be "heating" or "cooling"
{{ states('sensor.bedroom_temperature') }}  # Should have a value
{{ states('input_boolean.calibration_learning_enabled') }}  # Should be "on"
```

### Offset Not Updating

**Check:**
1. Sample count < 5 (need more data)
2. Offset changes < 0.5°C (too small)
3. Calibration is locked (can't update)

**Fix:**
- If locked: Click "Unlock" to resume learning
- If few samples: Run AC longer
- If changes too small: Adjust tolerance

### Erratic Offset Values

**Possible causes:**
1. External sensor fluctuating (move away from AC vent)
2. AC unit cycling (normal, but wait for more samples)
3. Sensor malfunction (check sensor battery)

**Fix:**
- Reposition external sensor: Center of room, away from drafts
- Wait for 10+ samples: More data = more stable
- Replace sensor battery if needed

### Zone Won't Reach Target

**Check:**
1. Setpoint in valid range (16-30°C)
2. AC unit is functioning properly
3. Zone insulation adequate

**Debug:**
```yaml
service: notify.notify
data:
  message: |
    Zone: {{ state_attr('climate.bedroom_ac', 'friendly_name') }}
    AC Setpoint: {{ state_attr('climate.bedroom_ac', 'temperature') }}°C
    External: {{ states('sensor.bedroom_temperature') }}°C
    Offset: {{ state_attr('climate.bedroom_ac', 'current_offset') }}°C
    Target: {{ states('input_number.bedroom_target') }}°C
```

## Best Practices

### ✅ DO

- **Collect plenty of data**: Run for 30+ minutes before locking
- **Place sensor correctly**: Center of room, not near AC/drafts
- **Lock when stable**: Prevents accidental drift
- **Recalibrate seasonally**: AC efficiency changes with season
- **Monitor automations**: Ensure they run as expected
- **Check logs**: Look for automation errors

### ❌ DON'T

- **Change setpoint constantly**: Let system stabilize first
- **Place sensor in AC outlet**: Will read cold air, not room temp
- **Expect immediate accuracy**: Takes 10-20 samples to stabilize
- **Ignore divergence alerts**: >2.5°C offset suggests a problem
- **Lock too early**: Wait for at least 5-10 samples
- **Disable learning without reason**: You might need recalibration

## Advanced Topics

### Manual Offset Entry

If you know the offset (e.g., from manual testing):

```yaml
# Set known offset directly
service: climate.set_temperature
target:
  entity_id: climate.bedroom_ac
data:
    # Manually configure offset
    extra_data:
      calibration_offset: 1.5
```

### Multiple Sensors Per Zone

If you have multiple sensors in one zone:

```yaml
# Average them
- name: "Bedroom Temperature Average"
  unique_id: "bedroom_temp_avg"
  unit_of_measurement: "°C"
  state: |
    {%- set sensor1 = states('sensor.bedroom_temp_1') | float(20) -%}
    {%- set sensor2 = states('sensor.bedroom_temp_2') | float(20) -%}
    {{ ((sensor1 + sensor2) / 2) | round(1) }}
```

### Offset Limits

Prevent unreasonable offsets:

```yaml
# Cap offset to ±3°C
- service: climate.set_temperature
  target:
    entity_id: climate.bedroom_ac
  data:
    temperature: |
      {%- set target = 22 -%}
      {%- set offset = state_attr('climate.bedroom_ac', 'current_offset') | float(0) -%}
      {%- set offset_capped = [offset, -3] | max | min(3) -%}
      {{ target + offset_capped }}
```

## Examples

### Simple 2-Room Setup

```yaml
# Helpers
input_number:
  living_room_target:
    min: 16
    max: 30
  bedroom_target:
    min: 16
    max: 30

input_boolean:
  calibration_learning_enabled:

# Automations
- alias: "Calibration: Learning loop"
  trigger:
    platform: time_pattern
    minutes: "/2"
  condition:
    - condition: state
      entity_id: input_boolean.calibration_learning_enabled
      state: "on"
  action:
    # Adjust living room
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: |
          {%- set target = states('input_number.living_room_target') | float(22) -%}
          {%- set offset = state_attr('climate.living_room_ac', 'current_offset') | float(0) -%}
          {{ target + offset }}
    
    # Adjust bedroom
    - service: climate.set_temperature
      target:
        entity_id: climate.bedroom_ac
      data:
        temperature: |
          {%- set target = states('input_number.bedroom_target') | float(21) -%}
          {%- set offset = state_attr('climate.bedroom_ac', 'current_offset') | float(0) -%}
          {{ target + offset }}
```

### 6-Room Setup (Your Case)

See `example_calibration_automations.yaml` for complete 6-zone example with learning, logging, and alerts.

## Support

- **Dashboard**: `calibration_dashboard.html`
- **Automations**: `example_calibration_automations.yaml`
- **Code**: `custom_components/clima/calibration.py`

Questions?
- Check logs: Settings → System → Logs
- Review dashboard for real-time status
- Test manual setpoint adjustments

---

**Remember**: Calibration is automatic and learns over time. Be patient with the first 24 hours of data collection, then lock for consistency!
