# Clima Quick Start Guide

Get Clima up and running in 5 minutes with **zero-config automatic discovery**.

## ⚡ Super Quick Install (3 steps, 5 minutes)

### Prerequisites
✅ Midea AC integration already installed and working  
✅ All AC units discovered in Home Assistant  

### Step 1: Copy Integration Files

```bash
# Copy to your Home Assistant config directory
cp -r /Users/estebanbascur/claude/projects/clima/custom_components/clima \
      ~/.homeassistant/custom_components/
```

Or if using Docker:
```bash
docker cp /Users/estebanbascur/claude/projects/clima/custom_components/clima \
          your-ha-container:/config/custom_components/
```

### Step 2: Restart Home Assistant

```
Settings → System → Restart Home Assistant
```

Wait 2-3 minutes for restart to complete.

### Step 3: Watch the Magic ✨

Clima automatically:
1. 🔍 **Discovers** all your AC units (climate entities)
2. 📝 **Creates helpers** for each zone you have
3. ✅ **Registers services** for control

Go to:
```
Settings → Devices & Services → Integrations
```

Look for **Clima - Multi-Zone AC Controller** ✅

Check **Settings → System → Logs** for:
```
✅ Clima integration setup complete
🔍 Found X AC unit(s)
```

**That's it!** Zero manual configuration needed.

## ✅ What Gets Auto-Created

The integration **automatically discovers** your AC units and creates helpers ONLY for zones that have them.

### Global Helpers (1 set)
- ✅ `input_boolean.calibration_learning_enabled` - Enable/disable learning
- ✅ `input_text.calibration_status` - Status display
- ✅ `input_number.calibration_tolerance` - Tolerance setting (±2°C)

### Per-Zone Helpers (created for each AC unit found)
For EACH AC unit in your system:
- ✅ `input_number.{zone}_target` - Target temperature setpoint
- ✅ `input_boolean.{zone}_calibration_locked` - Lock calibration
- ✅ `input_number.{zone}_calibration_offset` - Track offset value

**Example**: If you have 4 AC units:
- 3 global helpers
- 12 zone helpers (3 per zone × 4 zones)
- **Total: 15 helpers auto-created** ✨

## 🔍 How Auto-Discovery Works

Clima scans your Home Assistant for existing **climate entities** (AC units):

```
Home Assistant entities:
├── climate.bedroom_ac          ✅ Found! Create helpers for "bedroom"
├── climate.living_room_ac      ✅ Found! Create helpers for "living_room"
├── climate.master_ac           ✅ Found! Create helpers for "master"
└── climate.office_ac           ✅ Found! Create helpers for "office"

Helpers created:
├── input_number.bedroom_target
├── input_number.bedroom_calibration_locked
├── input_number.bedroom_calibration_offset
├── input_number.living_room_target
├── ... (repeat for each zone)
```

**No manual configuration needed!** Clima figures out what you have and sets up accordingly.

## 🆘 Troubleshooting Auto-Discovery

### No AC Units Found?

**Check Prerequisites:**
1. Is Midea AC integration installed?
2. Are all AC units discovered in Home Assistant?

**Verify:**
```
Settings → Devices & Services → Entities
Search for "climate"
Should see: climate.xxx_ac entities
```

**If missing:**
1. Install/reinstall Midea AC integration
2. Discover all AC units through Midea app
3. Restart Home Assistant
4. Then restart Clima integration

### Helpers Not Created?

Check logs:
```
Settings → System → Logs
Search for "Clima" or "clima"
```

If you see errors, try manually creating helpers:

**Settings → Devices & Services → Helpers**

For each zone with an AC unit, create:
```
Input Number: {zone}_target
  Min: 16, Max: 30, Step: 0.1, Icon: thermometer, Initial: 22

Input Boolean: {zone}_calibration_locked
  Icon: lock, Initial: OFF

Input Number: {zone}_calibration_offset  
  Min: -5, Max: 5, Step: 0.1, Icon: plus-minus, Initial: 0
```

## 📊 Access Your Dashboards

### Main Dashboard (Recommended)

Open the main hub with sidebar navigation:
```
http://your-home-assistant-ip:8123/local/index.html
```

This gives you access to all Clima features through an intuitive, organized interface.

### Individual Dashboards

Or access specific dashboards directly:

| Dashboard | Purpose | URL |
|-----------|---------|-----|
| Calibration | Temperature offset learning | `/local/calibration_dashboard.html` |
| Overview | Real-time zone monitoring | `/local/dashboard_preview.html` |
| Heating | Winter heating mode | `/local/dashboard_heating.html` |
| Schedules | Temperature scheduling | `/local/schedules.html` |
| Energy | Energy analytics | `/local/energy_analytics.html` |

---

## 📋 Next Steps

### 1. Open Main Dashboard

1. Go to: `http://your-ha-ip:8123/local/index.html`
2. Explore the sidebar navigation
3. Visit each dashboard to get familiar with features

### 2. Create Automations

Copy automations to your `automations.yaml`:

**Calibration Learning:**
```bash
# Copy calibration automations
cat /Users/estebanbascur/claude/projects/clima/example_calibration_automations.yaml >> ~/.homeassistant/automations.yaml
```

**General Automations (optional):**
```bash
# Copy general automations
cat /Users/estebanbascur/claude/projects/clima/example_automations.yaml >> ~/.homeassistant/automations.yaml
```

**Heating Automations (optional, winter):**
```bash
# Copy heating automations for winter
cat /Users/estebanbascur/claude/projects/clima/example_heating_automations.yaml >> ~/.homeassistant/automations.yaml
```

Then restart Home Assistant again.

### 3. Enable Calibration Learning

1. Open calibration dashboard
2. Toggle "Learning Status: Active"
3. Turn on your AC units
4. Let them run for 30+ minutes
5. Watch dashboard for learning progress

### 4. Lock Calibrations

Once offsets stabilize:
1. Click "Lock" for each zone
2. System uses fixed offset going forward

## 🎯 Verify Everything Works

Check in Home Assistant:

**1. Helpers Created:**
```
Settings → Devices & Services → Helpers
```
Should see all created entities.

**2. Automations Loaded:**
```
Settings → Automations & Scenes
```
Should see new Clima automations.

**3. Entities Available:**
```
Settings → Developer Tools → States
```
Search for `input_` to see helpers.

## 🚀 Dashboard Files Included

All dashboard files are included:

```
clima/
├── index.html                      Main hub with sidebar navigation
├── calibration_dashboard.html       Temperature calibration management
├── dashboard_preview.html           Zone overview and real-time monitoring
├── dashboard_heating.html           Winter heating mode controls
├── schedules.html                  Temperature scheduling interface
├── energy_analytics.html            Energy consumption analytics
```

**No manual copying needed!** HACS automatically places these in your `www` folder.

### Direct Access

After HACS installation, access dashboards at:
```
http://your-ha-ip:8123/local/index.html                    (Main Hub)
http://your-ha-ip:8123/local/calibration_dashboard.html   (Calibration)
http://your-ha-ip:8123/local/dashboard_preview.html       (Overview)
http://your-ha-ip:8123/local/dashboard_heating.html       (Heating)
http://your-ha-ip:8123/local/schedules.html               (Schedules)
http://your-ha-ip:8123/local/energy_analytics.html        (Energy)
```

## 🔍 Troubleshooting

### Helpers Not Created

Check Home Assistant logs:
```
Settings → System → Logs
Search for "clima"
```

Look for errors. If you see issues, create helpers manually (see above).

### Automations Not Running

1. Go to `Settings → Automations & Scenes`
2. Click the automation
3. Check it's **enabled** (toggle switch is on)
4. Click "Trace" to see execution history

### Can't Find Entities

```
Settings → Developer Tools → States
```

Search for `climate.` - should see your AC units:
- `climate.bedroom_ac`
- `climate.living_room_ac`
- etc.

If not found, verify your Midea/AC integration is working first.

## 📚 Documentation

For detailed information, see:
- **README.md** - Full feature overview
- **MODES.md** - Heating/cooling modes explained
- **CALIBRATION.md** - Temperature calibration guide
- **SCHEDULES.md** - Schedule automations
- **SETUP_GUIDE.md** - Detailed setup walkthrough

## 🎉 You're Done!

That's all you need to get started. Clima will:
- ✅ Auto-create all required entities
- ✅ Auto-register all services
- ✅ Auto-learn temperature offsets
- ✅ Auto-adjust AC setpoints
- ✅ Keep you comfortable year-round

## 💡 Tips

- **First Time**: Let calibration run 24+ hours to collect data
- **Seasonal**: Recalibrate every 3 months for seasonal changes
- **Locked**: Once locked, calibration won't change
- **Dashboard**: Monitor progress in calibration dashboard
- **Logs**: Check logs if something isn't working

## 🆘 Need Help?

- Check logs: `Settings → System → Logs`
- Review automations: `Settings → Automations & Scenes`
- View entities: `Settings → Developer Tools → States`
- Read docs: See "Documentation" section above

---

**Version**: 0.2.0  
**Last Updated**: 2026-04-21  
**Status**: ✅ Ready for Home Assistant
