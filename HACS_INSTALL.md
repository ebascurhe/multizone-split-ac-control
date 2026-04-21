# Clima HACS Installation Guide

Install Clima directly through Home Assistant Community Store (HACS).

## 🚀 Option 1: Install from Custom Repository (Quickest)

### Step 1: Add Custom Repository to HACS

1. Open Home Assistant
2. Go to **HACS** (left sidebar)
3. Click **⋮** (three dots) → **Custom repositories**
4. Paste repository URL:
   ```
   https://github.com/estebanbascur/clima
   ```
5. Category: **Integration**
6. Click **Create**

### Step 2: Download Clima

1. In HACS, search for **Clima**
2. Click the result
3. Click **Download** (bottom right)
4. Confirm download

### Step 3: Restart Home Assistant

```
Settings → System → Restart Home Assistant
```

Wait 2-3 minutes for restart.

### Step 4: Access Your Dashboards

Once installed, access the main dashboard at:
```
http://your-home-assistant-ip:8123/local/index.html
```

This home screen provides navigation to all Clima features.

### Step 5: Done! ✅

Clima is now installed and will:
- ✅ Auto-discover your AC units
- ✅ Create helper entities for each zone
- ✅ Make dashboards available
- ✅ Register control services

---

## 📋 Option 2: Submit to Official HACS (Full Distribution)

If you want Clima in the official HACS store:

### Step 1: Push to GitHub

```bash
# Initialize git repository
cd /Users/estebanbascur/claude/projects/clima
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial Clima integration release"

# Add remote (replace with your repo)
git remote add origin https://github.com/estebanbascur/clima.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create Release on GitHub

```bash
# Create a version tag
git tag v0.1.0
git push origin v0.1.0

# Or use GitHub UI:
# Releases → Create new release
# Tag: v0.1.0
# Title: Clima v0.1.0 - Initial Release
# Description: [copy from README.md]
```

### Step 3: Submit to HACS

1. Go to [HACS Repository Manager](https://my.home-assistant.io/redirect/community_store/)
2. Click **Create** (top right)
3. Fill in form:
   - **Repository**: `https://github.com/estebanbascur/clima`
   - **Category**: Integration
   - **Description**: Multi-Zone AC Controller with smart temperature calibration

4. HACS team reviews (usually 1-7 days)
5. Once approved, appears in HACS store for everyone!

---

## ✅ Repository Checklist

Your repository is HACS-ready! Verify these files exist:

```
clima/
├── custom_components/
│   └── clima/
│       ├── __init__.py           ✅ Main integration
│       ├── config_flow.py        ✅ Setup wizard
│       ├── const.py              ✅ Constants
│       ├── manifest.json         ✅ Metadata
│       ├── strings.json          ✅ Translations
│       └── calibration.py        ✅ Calibration engine
├── index.html                     ✅ Main dashboard hub
├── calibration_dashboard.html     ✅ Calibration dashboard
├── dashboard_preview.html         ✅ Overview dashboard
├── dashboard_heating.html         ✅ Heating mode dashboard
├── schedules.html                 ✅ Schedules dashboard
├── energy_analytics.html          ✅ Energy analytics dashboard
├── hacs.json                      ✅ HACS config
├── README.md                      ✅ Documentation
├── LICENSE                        ✅ MIT License
├── QUICK_START.md                ✅ Quick start guide
├── CALIBRATION.md                ✅ Calibration docs
├── MODES.md                       ✅ Heating/cooling modes
├── SCHEDULES.md                  ✅ Scheduling guide
└── .gitignore                    ✅ Git ignore file
```

---

## 📝 Final Checklist for GitHub Release

- [ ] Repository created on GitHub
- [ ] All files pushed to `main` branch
- [ ] `hacs.json` in repository root
- [ ] `manifest.json` in `custom_components/clima/`
- [ ] `README.md` with clear description
- [ ] `LICENSE` file (MIT included)
- [ ] Version tag created (v0.1.0)
- [ ] Release notes written

---

## 🎯 Installation via HACS (User Perspective)

Once in HACS, users can install with just 4 clicks:

1. **HACS** → **Integrations** → **Create Automation**
2. Search **Clima**
3. Click result → **Download**
4. **Settings** → **System** → **Restart**

Then access the dashboard:
```
http://your-ha-ip:8123/local/index.html
```

### Dashboard Features

- **Sidebar Navigation** - Easy access to all features
- **Home Overview** - Features and quick stats
- **Calibration** - Temperature offset management
- **Overview** - Real-time zone monitoring
- **Heating** - Winter mode controls
- **Schedules** - Temperature scheduling
- **Energy** - Energy analytics

---

## 🔄 Updating Clima

When you release a new version:

```bash
# Make changes
git add .
git commit -m "Release v0.2.0 - Add feature X"

# Create new version tag
git tag v0.2.0
git push origin main
git push origin v0.2.0
```

Users get notified in HACS about the update and can click **Upgrade**.

---

## 🆘 Troubleshooting

### HACS Can't Find Repo

**Fix:**
1. Verify repo is public
2. Wait 5 minutes for GitHub to index
3. Try adding again

### Download Failed

**Fix:**
1. Check manifest.json syntax
2. Verify manifest.json in correct location
3. Try removing and re-adding repo

### Integration Not Found After Install

**Fix:**
1. Clear browser cache
2. Restart Home Assistant
3. Check `/config/custom_components/clima/` exists

---

## 📚 Additional Resources

- **HACS Docs**: https://hacs.xyz/docs/
- **Integration Requirements**: https://hacs.xyz/docs/publish/integration
- **Manifest.json Spec**: https://developers.home-assistant.io/docs/creating_integration_manifest

---

## 🎉 Success!

Once in HACS, your integration is available to thousands of Home Assistant users!

**Next Steps:**
1. Push to GitHub
2. Create release
3. (Optional) Submit to official HACS
4. Watch users install Clima! 🚀
