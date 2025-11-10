# NeuroTrade FGI Dashboard

A high-frequency interactive web dashboard that visualizes individual-stock Fear Index (FI_t) and Greed Index (GI_t) based on EMA momentum, order imbalance, and volatility.

## 🧠 Features

- **Real-time Fear & Greed Index Calculation**
  - Price Momentum (PM_t) based on short/long-term EMA
  - Order Momentum (OM_t) from simulated buy-sell imbalance
  - Volatility (Vol_t) from rolling standard deviation
  - Fear Index (FI_t) and Greed Index (GI_t) using sigmoid functions

- **Interactive Visualizations**
  - Stock price chart with EMA overlay (12-period and 26-period)
  - Dual line chart for FI_t and GI_t with color-coded zones
  - Real-time metrics panel showing all calculated values
  - Emotion zone indicators (Fear/Greed/Neutral)

- **High-Frequency Data Simulation**
  - Tick-by-tick data generation
  - Configurable refresh intervals (1s, 10s, 1min)
  - High-frequency mode toggle

- **Professional UI**
  - Dark mode with neural-network inspired gradient background
  - Smooth animations using Framer Motion
  - Responsive design with Tailwind CSS
  - Glass-morphism effects

## 📊 Core Formulas

### Price Momentum
```
PM_t = (EMA_sp(t) - EMA_lp(t)) / EMA_lp(t)
```
where EMA_sp = 12-period EMA, EMA_lp = 26-period EMA

### Order Momentum
```
OM_t = EMA_so(t) - EMA_lo(t)
```
where EMA_so/lo = short/long-term EMA of order imbalance

### Volatility
```
Vol_t = rolling std dev of log returns (annualized)
V_0 = mean(Vol_t)
```

### Fear & Greed Indices
```
FI_t = 100 * [1/(1+exp(k_p*PM_t))] * [1/(1+exp(k_o*OM_t))] * [1/(1+exp(-k_v*(Vol_t - V_0)))]
GI_t = 100 * [1/(1+exp(-k_p*PM_t))] * [1/(1+exp(-k_o*OM_t))] * [1/(1+exp(k_v*(Vol_t - V_0)))]
```
Constants: k_p=2.5, k_o=2.0, k_v=1.5

### Emotion Zones
- **FI_t > 70** → Fear Zone (Buy Signal)
- **GI_t > 70** → Greed Zone (Sell Signal)
- **Otherwise** → Neutral (Hold)

## 🚀 Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.7+ (for Flask backend)
- Flask backend running on port 5000

### Setup React App

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## 📁 Project Structure

```
neurotrade-fgi-dashboard/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── StockChart.jsx      # Stock price chart with EMA
│   │   ├── FearGreedChart.jsx  # FI/GI dual chart
│   │   └── SignalPanel.jsx    # Real-time metrics panel
│   ├── api/
│   │   └── fetchData.js        # API service for stock data
│   ├── utils/
│   │   └── fgiCalculator.js   # FGI calculation logic
│   ├── App.jsx                # Main app component
│   ├── index.js               # React entry point
│   └── index.css              # Tailwind CSS styles
├── package.json
├── tailwind.config.js
└── README_FGI.md
```

## 🎯 Usage

1. **Enter Stock Ticker**: Type a stock symbol (e.g., TSLA, AAPL) in the ticker input
2. **Select Refresh Interval**: Choose update frequency (1s, 10s, or 1min)
3. **Toggle High-Frequency Mode**: Enable for tick-by-tick simulation
4. **View Charts**: 
   - Left: Stock price with EMA overlay
   - Right: Fear & Greed Index over time
5. **Monitor Signals**: Check the Signal Panel for emotion zones and trading signals
6. **Export Data**: Click "Export CSV" to download data for offline analysis

## 🔧 Configuration

### API Endpoint
Set the backend API URL in `.env`:
```
REACT_APP_API_URL=http://localhost:5000
```

### EMA Periods
Default: Short=12, Long=26
Modify in `App.jsx`:
```jsx
<StockChart data={stockData} shortPeriod={12} longPeriod={26} />
```

### FGI Constants
Modify in `src/utils/fgiCalculator.js`:
```javascript
const K_P = 2.5;  // Price momentum constant
const K_O = 2.0;  // Order momentum constant
const K_V = 1.5;  // Volatility constant
```

## 🎨 Customization

### Theme Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  'neural-blue': '#667eea',
  'neural-purple': '#764ba2',
  'fear-red': '#ef4444',
  'greed-green': '#10b981',
}
```

### Chart Styles
Modify components in `src/components/` to customize chart appearance.

## 📈 Data Flow

1. User inputs ticker symbol
2. Frontend fetches time series data from Flask backend
3. Prices are extracted and passed to FGI calculator
4. EMA, PM_t, OM_t, Vol_t are calculated
5. FI_t and GI_t are computed using sigmoid functions
6. Charts update with new data
7. Signal panel displays current metrics and emotion zone

## 🔬 Technical Details

- **Framework**: React 18.2
- **Charts**: Recharts 2.10
- **Styling**: Tailwind CSS 3.4
- **Animations**: Framer Motion 10.16
- **HTTP Client**: Axios 1.6

## 🐛 Troubleshooting

### Charts not displaying
- Ensure stock data has at least 26 data points
- Check browser console for errors
- Verify API endpoint is accessible

### High-frequency mode not working
- Check network tab for API calls
- Ensure backend supports the endpoint
- Try reducing refresh interval

### FGI values seem incorrect
- Verify data has sufficient history (26+ points)
- Check EMA periods are appropriate for data frequency
- Review calculation constants (K_P, K_O, K_V)

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, please check the main project README or open an issue on GitHub.
