# Clima Sidebar Integration Guide

The Clima sidebar is a reusable navigation component that can be added to any dashboard.

## Files Included

- `sidebar.css` - Sidebar styles
- `sidebar.js` - Sidebar navigation logic
- `sidebar-template.html` - HTML template to include

## How to Add Sidebar to Your Dashboard

### Step 1: Include CSS and JavaScript

In your HTML `<head>` section, add:

```html
<link rel="stylesheet" href="sidebar.css">
<script src="sidebar.js"></script>
```

### Step 2: Add Sidebar HTML

At the beginning of your `<body>`, add the sidebar before your main content:

```html
<div class="clima-container">
    <!-- Sidebar Navigation -->
    <nav class="clima-sidebar">
        <div class="clima-sidebar-header">
            <span class="clima-sidebar-icon">❄️</span>
            <span>Clima</span>
        </div>

        <ul class="clima-nav">
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="index">
                    <span class="clima-nav-icon">🏠</span>
                    Home
                </a>
            </li>
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="calibration">
                    <span class="clima-nav-icon">🌡️</span>
                    Calibration
                </a>
            </li>
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="overview">
                    <span class="clima-nav-icon">📊</span>
                    Overview
                </a>
            </li>
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="heating">
                    <span class="clima-nav-icon">🔥</span>
                    Heating
                </a>
            </li>
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="schedules">
                    <span class="clima-nav-icon">⏰</span>
                    Schedules
                </a>
            </li>
            <li class="clima-nav-item">
                <a class="clima-nav-link" data-page="energy">
                    <span class="clima-nav-icon">⚡</span>
                    Energy
                </a>
            </li>
        </ul>
    </nav>

    <!-- Main Content -->
    <div class="clima-main">
        <!-- Your dashboard content goes here -->
    </div>
</div>
```

### Step 3: Wrap Your Content

Move your existing dashboard content inside the `<div class="clima-main">` container.

## Example

Before (without sidebar):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Calibration Dashboard</title>
</head>
<body>
    <div id="content">
        <!-- Your dashboard content -->
    </div>
</body>
</html>
```

After (with sidebar):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Calibration Dashboard</title>
    <link rel="stylesheet" href="sidebar.css">
    <script src="sidebar.js"></script>
</head>
<body>
    <div class="clima-container">
        <!-- Sidebar Navigation -->
        <nav class="clima-sidebar">
            <!-- Sidebar content (see above) -->
        </nav>

        <!-- Main Content -->
        <div class="clima-main">
            <div id="content">
                <!-- Your dashboard content -->
            </div>
        </div>
    </div>
</body>
</html>
```

## Customization

### Change Sidebar Width

Edit `sidebar.css`:
```css
.clima-sidebar {
    width: 256px;  /* Change this value */
}
```

### Change Colors

Edit `sidebar.css`:
```css
.clima-nav-link.active {
    background: #fff3e0;  /* Active background */
    color: #ff6b6b;       /* Active text color */
}
```

### Add More Navigation Items

Add new items to the `<ul class="clima-nav">`:
```html
<li class="clima-nav-item">
    <a class="clima-nav-link" data-page="settings">
        <span class="clima-nav-icon">⚙️</span>
        Settings
    </a>
</li>
```

Update the page mapping in `sidebar.js`:
```javascript
const pages = {
    'settings': 'settings.html',
    // ... other pages
};
```

## Features

✅ **Responsive Design** - Works on desktop and mobile
✅ **Active Link Highlighting** - Shows current page
✅ **Smooth Navigation** - Animated transitions
✅ **Easy Integration** - Just include 2 files + HTML
✅ **Customizable** - Change colors, icons, layout
✅ **No Dependencies** - Pure CSS and JavaScript

## CSS Classes Reference

| Class | Purpose |
|-------|---------|
| `.clima-container` | Main flex container |
| `.clima-sidebar` | Sidebar navigation |
| `.clima-sidebar-header` | Sidebar title area |
| `.clima-nav` | Navigation list |
| `.clima-nav-item` | Navigation item |
| `.clima-nav-link` | Navigation link |
| `.clima-nav-link.active` | Active navigation link |
| `.clima-nav-icon` | Icon in navigation |
| `.clima-main` | Main content area |

## Testing

1. Add sidebar to one dashboard first
2. Open the dashboard in your browser
3. Test navigation links
4. Verify active link highlighting
5. Test on mobile (resize browser)

Then add to remaining dashboards!
