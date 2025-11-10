# NeuroTrade FGI Dashboard - Setup Guide

## 🚀 Quick Start

### Step 1: Start Flask Backend

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the Flask backend:
   ```bash
   python app.py
   ```
   The backend will start on `http://localhost:5000`

### Step 2: Install React Dependencies

1. Open a **new** terminal/command prompt
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   npm install
   ```
   This will install all required packages (React, Recharts, Tailwind, etc.)

### Step 3: Start React Development Server

1. In the same terminal where you ran `npm install`
2. Start the React app:
   ```bash
   npm start
   ```
   Or on Windows, you can use:
   ```bash
   start_react.bat
   ```

3. The dashboard will automatically open in your browser at `http://localhost:3000`

## 📋 Prerequisites

- **Node.js** 16.0 or higher
- **npm** (comes with Node.js)
- **Python** 3.7 or higher
- **pip** (Python package manager)

### Check Your Versions

```bash
node --version    # Should be 16.0+
npm --version     # Should be 7.0+
python --version  # Should be 3.7+
```

## 🔧 Installation Details

### Backend (Flask)

The Flask backend is already set up. Just ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

### Frontend (React)

The React app uses:
- **React** 18.2 - UI framework
- **Recharts** 2.10 - Chart library
- **Tailwind CSS** 3.4 - Styling
- **Framer Motion** 10.16 - Animations
- **Axios** 1.6 - HTTP client

All dependencies are listed in `package.json` and will be installed automatically with `npm install`.

## 🎯 Usage

1. **Enter Stock Ticker**: Type a stock symbol (e.g., TSLA, AAPL, MSFT) in the ticker input field
2. **Select Refresh Interval**: Choose how often data updates (1s, 10s, or 1min)
3. **Toggle High-Frequency Mode**: Enable for simulated tick-by-tick data
4. **View Charts**: 
   - **Left Chart**: Stock price with EMA (12 and 26 period) overlay
   - **Right Chart**: Fear & Greed Index over time
5. **Monitor Signals**: Check the bottom panel for:
   - Real-time metrics (PM_t, OM_t, Vol_t, FI_t, GI_t)
   - Emotion zone (Fear/Greed/Neutral)
   - Trading signals (Buy/Sell/Hold)
6. **Export Data**: Click "Export CSV" to download data for analysis

## 🐛 Troubleshooting

### React app won't start

**Error**: `'npm' is not recognized`
- **Solution**: Install Node.js from https://nodejs.org/

**Error**: `Cannot find module 'react'`
- **Solution**: Run `npm install` in the project directory

**Error**: Port 3000 already in use
- **Solution**: 
  - Close other applications using port 3000, or
  - Set a different port: `PORT=3001 npm start`

### Backend connection issues

**Error**: `Network Error` or `Failed to fetch`
- **Solution**: 
  - Ensure Flask backend is running on port 5000
  - Check `http://localhost:5000/api/stocks` in browser
  - Verify CORS is enabled in Flask (should be automatic)

### Charts not displaying

**Issue**: Charts show "No data available"
- **Solution**: 
  - Ensure stock ticker is valid (e.g., TSLA, AAPL)
  - Check browser console for errors
  - Verify backend API is responding
  - Some tickers may need at least 26 data points

### High-frequency mode issues

**Issue**: Data not updating in high-frequency mode
- **Solution**: 
  - Check network tab in browser DevTools
  - Ensure refresh interval is set appropriately
  - Backend may be rate-limited; try longer intervals

## 📁 Project Structure

```
ISEF/
├── app.py                    # Flask backend
├── package.json              # React dependencies
├── requirements.txt          # Python dependencies
├── tailwind.config.js        # Tailwind CSS config
├── start_react.bat           # Windows startup script
│
├── src/                      # React source code
│   ├── App.jsx              # Main app component
│   ├── index.js             # React entry point
│   ├── index.css            # Global styles
│   ├── components/          # React components
│   │   ├── StockChart.jsx
│   │   ├── FearGreedChart.jsx
│   │   └── SignalPanel.jsx
│   ├── api/                 # API services
│   │   └── fetchData.js
│   └── utils/               # Utilities
│       └── fgiCalculator.js
│
├── public/                   # Static files
│   └── index.html
│
└── templates/               # Flask templates
    ├── index.html           # Original trading app
    └── fgi_dashboard.html    # FGI dashboard redirect
```

## 🔄 Development Workflow

1. **Backend Changes**: 
   - Edit `app.py`
   - Flask auto-reloads (if debug=True)
   - No restart needed

2. **Frontend Changes**:
   - Edit files in `src/`
   - React hot-reloads automatically
   - Changes appear instantly in browser

3. **Style Changes**:
   - Edit `tailwind.config.js` for theme
   - Edit `src/index.css` for global styles
   - Component styles in component files

## 🎨 Customization

### Change API Endpoint

Edit `src/api/fetchData.js`:
```javascript
const API_BASE_URL = 'http://your-backend-url:5000';
```

Or set environment variable:
```bash
REACT_APP_API_URL=http://localhost:5000 npm start
```

### Adjust EMA Periods

Edit `src/App.jsx`:
```jsx
<StockChart data={stockData} shortPeriod={12} longPeriod={26} />
```

### Modify FGI Constants

Edit `src/utils/fgiCalculator.js`:
```javascript
const K_P = 2.5;  // Price momentum
const K_O = 2.0;  // Order momentum
const K_V = 1.5;  // Volatility
```

## 📦 Building for Production

To create an optimized production build:

```bash
npm run build
```

This creates a `build/` folder with optimized files. You can serve these files with any static file server or integrate with Flask.

## 🆘 Getting Help

1. Check browser console (F12) for errors
2. Check Flask terminal for backend errors
3. Verify all dependencies are installed
4. Ensure both servers are running
5. Review README_FGI.md for detailed documentation

## ✅ Verification Checklist

- [ ] Node.js and npm installed
- [ ] Python 3.7+ installed
- [ ] Flask dependencies installed (`pip install -r requirements.txt`)
- [ ] React dependencies installed (`npm install`)
- [ ] Flask backend running on port 5000
- [ ] React app running on port 3000
- [ ] Can access `http://localhost:5000/api/stocks`
- [ ] Can access `http://localhost:3000`
- [ ] Dashboard loads and displays charts

## 🎉 Success!

If you see the NeuroTrade FGI Dashboard with:
- Stock price chart on the left
- Fear & Greed Index chart on the right
- Real-time metrics panel at the bottom

Then everything is working correctly! 🚀

