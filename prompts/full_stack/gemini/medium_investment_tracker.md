Create a **Privacy-First Investment Portfolio Tracker** that runs locally and gives users control over their financial data.

**Core Features:**
1.  **Asset Management**: Users can add assets (Stocks, Crypto, ETFs) manually or import them via CSV.
2.  **Performance Visualization**: A dashboard showing "Total Portfolio Value" over time and a pie chart for "Asset Allocation".
3.  **Transaction Ledger**: A table view of all buy/sell orders with calculated Realized and Unrealized P/L.
4.  **Market Data Stub**: Since real-time financial APIs are expensive, implement a background worker that fetches mocked prices or uses a free tier API (like Yahoo Finance via `yfinance` python library) to update asset values once a day.
5.  **Watchlist**: A sidebar to track potential investments.

**Technical Requirements:**
-   Install a charting library (Chart.js, Recharts, or Apache ECharts) for performance visualization.
-   Install `yfinance` for market data retrieval (or use a free tier API).
-   All financial math (weighted average price, ROI) must happen on the backend and be tested thoroughly.

## UI Design
Build a modern, professional interface with:
- Clean, minimal design with proper spacing
- Modern color palette (primary/secondary/accent colors)
- Responsive layout that works on mobile and desktop
- Professional typography (readable fonts, clear hierarchy)
- Smooth transitions and hover effects
- Consistent component styling throughout
- Proper form validation with user feedback
- Loading states for async operations
