# Smart Home Device Simulator

## Overview
This is a web-based device simulator that allows you to interact with your smart home system. It connects to the Django backend API and provides real-time device control, energy monitoring, and demo scenarios.

## Features

### 🏠 Smart Home Management
- Create and select smart homes
- View and manage rooms
- Control devices in real-time

### ⚡ Real-Time Energy Dashboard
- Live energy consumption monitoring
- Solar generation simulation
- Net energy usage calculation
- Efficiency scoring

### 🎭 Demo Scenarios
- **Morning Routine**: Simulate waking up (lights, coffee maker, bathroom fan)
- **Energy Saving Mode**: Turn off non-essential devices
- **Realistic Usage**: Time-based device activity patterns
- **Random Activity**: Simulate unpredictable device usage

### 💡 Energy Efficiency
- Real-time efficiency tips
- Device-specific energy details
- Cost estimates
- Optimization recommendations

## How to Access

### Option 1: Using the Python Server (Recommended)
1. Make sure the Django backend is running:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Start the device simulator server:
   ```bash
   cd device-simulator
   python serve.py
   ```

3. Open your browser to: http://localhost:8080

### Option 2: Direct File Access
- Open `index.html` directly in your browser
- Note: May have CORS issues depending on your browser settings

## Usage Instructions

### 1. Login
- Create an account or login with existing credentials
- The simulator uses the same authentication as the main application

### 2. Create/Select Smart Home
- Create a new smart home or select an existing one
- New homes automatically get demo devices in the Living Room

### 3. Control Devices
- Toggle devices on/off with the buttons
- Adjust analogue devices (like dimmers) with sliders
- View energy details for individual devices

### 4. Monitor Energy
- Real-time dashboard shows current consumption and generation
- Efficiency tips appear based on your usage patterns
- Energy metrics update automatically

### 5. Run Demo Scenarios
- Use the scenario buttons to demonstrate different usage patterns
- Watch energy consumption change in real-time
- Perfect for presentations and demonstrations

## Demo Flow Suggestions

### For Presentations:
1. **Start Fresh**: Create a new smart home
2. **Show Baseline**: Display initial energy dashboard
3. **Morning Routine**: Run the morning scenario and show energy increase
4. **Individual Control**: Manually toggle some devices
5. **Energy Saving**: Run energy saving mode and show the reduction
6. **Efficiency Tips**: Point out the dynamic tips that appear

### For Testing:
1. **Random Activity**: Use the random activity button to simulate usage
2. **Device Details**: Click energy details on various devices
3. **Real-time Updates**: Watch the dashboard update as you change devices
4. **Scenarios**: Test different scenarios at different times of day

## Technical Details

### API Integration
The simulator connects to these Django API endpoints:
- `/api/auth/login/` - Authentication
- `/api/smarthomes/` - Smart home management
- `/api/devices/` - Device control
- `/api/demo/energy-dashboard/` - Real-time energy data
- `/api/demo/run-scenario/` - Demo scenarios
- `/api/demo/device/<id>/energy/` - Device energy details

### Auto-Refresh
- Device states refresh every 10 seconds
- Energy dashboard updates when devices change
- Manual refresh buttons available

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript must be enabled
- Local storage used for authentication tokens

## Troubleshooting

### Connection Issues
- Ensure Django backend is running on http://127.0.0.1:8000
- Check console for CORS errors
- Try using the Python server instead of direct file access

### Authentication Problems
- Clear browser storage/cookies
- Create a new account in the main application first
- Check that credentials are correct

### Energy Data Not Loading
- Ensure you've selected a smart home
- Check that devices exist in the home
- Try refreshing the energy dashboard manually

## Development Notes

### Adding New Features
- Device simulator uses vanilla JavaScript
- API calls are handled in the `apiCall()` function
- New demo scenarios can be added to the backend and UI

### Customization
- CSS can be modified for different themes
- Additional energy metrics can be added to the dashboard
- New device control types can be added

Enjoy demonstrating your smart home system! 🏠⚡
