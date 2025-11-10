# 🔄 Loop Box Financial Dashboard

An interactive 3-year financial modeling dashboard for Loop Box, a reusable food packaging business in India.

![Dashboard Preview](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)

## 🌟 Features

### Phase 1 (MVP) - ✅ Complete
- **Interactive Control Panel**: Adjust pricing, volume, and cost variables for each of 3 years
- **Real-time Calculations**: All metrics update instantly as you modify inputs
- **Comprehensive Income Statement**: Side-by-side 3-year view with all revenue and expense categories
- **Key Metrics Dashboard**: Revenue, EBITDA, and Net Margin with YoY growth tracking
- **Visual Analytics**:
  - Revenue growth bar chart
  - Margin progression line chart (Gross, EBITDA, Net)
  - Revenue mix pie charts for each year
- **Unit Economics**: Per-order and per-restaurant profitability metrics

### Phase 2 (Advanced Analytics) - ✅ Complete
- **Break-Even Analysis**:
  - Fixed costs, variable costs, and contribution margin calculations
  - Break-even orders and restaurants needed
  - Months to break-even projection
  - Visual break-even chart with revenue vs. cost lines
- **Sensitivity Analysis**:
  - "What if?" scenarios for key variables
  - Collection rate, wash cost, per-use fee, and order volume impacts
  - Side-by-side comparison table
- **COGS Breakdown Chart**: Stacked bar visualization showing cost drivers across 3 years
- **Change History Tracker**:
  - Automatic logging of all variable changes
  - Impact analysis on Year 3 Net Income
  - Export to CSV functionality
- **Scenario Management**:
  - Save current model assumptions
  - Load previously saved scenarios
  - Easy comparison between different versions

## 📊 Business Model

Loop Box operates a closed-loop reusable container system for food courts, corporate cafeterias, and college campuses:

1. Restaurants buy containers from Loop Box (₹150-200)
2. Customers receive cash incentives for returns (₹5-10)
3. Loop Box collects, washes, and sanitizes at micro-hubs
4. Clean containers delivered back to restaurants
5. Each container reused 100+ times

**Revenue Streams:**
- Container sales (one-time)
- Monthly service fees
- Per-use fees
- Setup fees
- Customer deposit shrinkage
- Future: Aggregator platform revenue (Zomato/Swiggy)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd "Pricing model dashboard"
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # Activate on macOS/Linux:
   source venv/bin/activate

   # Activate on Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is the easiest way to deploy and share your dashboard publicly.

1. **Create a GitHub repository**
   - Push your code to GitHub (make sure `.gitignore` is set up correctly)

2. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy**
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Share**
   - You'll get a public URL like: `https://your-app-name.streamlit.app`
   - Share this link with anyone!

### Option 2: Render (FREE tier available)

1. Create account at [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Option 3: Railway (FREE tier with limits)

1. Sign up at [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Railway auto-detects Streamlit apps
4. Deploy with one click

### ⚠️ Important: Why Not Netlify?

Netlify is designed for **static websites** (HTML/CSS/JavaScript), while this is a **Python web application** that requires a server to run. Use Streamlit Cloud, Render, or Railway instead for Python apps.

## 📁 Project Structure

```
loop-box-dashboard/
├── app.py                    # Main Streamlit application
├── calculations.py           # Financial calculation functions
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── data/
    ├── defaults.json        # Default values for Years 1-3
    └── saved_scenarios/     # User-saved scenarios (future)
```

## 🎯 How to Use

1. **Save/Load Scenarios**: At the top of sidebar
   - Enter a scenario name and click "Save" to preserve current settings
   - Click "Load" to restore a previously saved scenario
   - Great for comparing different business assumptions

2. **Adjust Variables**: Use the sidebar tabs to modify:
   - **Pricing**: Container prices, fees, incentives
   - **Volume**: Restaurants, orders/day, collection rates
   - **COGS**: Manufacturing, washing, logistics costs
   - **OpEx**: Technology, marketing, facilities

3. **Switch Between Years**: Use tabs in the sidebar for Year 1, 2, and 3

4. **Analyze Results**: Main dashboard shows:
   - Top-line metrics with YoY growth
   - Full income statement
   - Visual charts (revenue, margins, COGS breakdown)
   - Unit economics

5. **Break-Even Analysis**: Scroll down to see:
   - How many orders/restaurants needed to break even
   - Contribution margin per order
   - Months to reach profitability
   - Visual break-even chart

6. **Sensitivity Analysis**: Test "what if" scenarios:
   - What if collection rate drops to 80%?
   - What if washing costs increase 20%?
   - What if we can't partner with Zomato?
   - What pricing achieves profitability?

7. **Track Changes**: View change history to see:
   - All variables you've adjusted
   - Impact of each change on Year 3 Net Income
   - Download history as CSV for records

## 💡 Key Questions This Dashboard Answers

- ✅ At what per-use fee do we become profitable?
- ✅ How many restaurants do we need to break even?
- ✅ What if collection rates are only 80%?
- ✅ Can we survive without Zomato partnership?
- ✅ What's our biggest cost driver?
- ✅ What pricing changes have the biggest impact?

## 🔧 Customization

### Modify Default Values
Edit `data/defaults.json` to change the starting values for any year.

### Add New Calculations
Edit `calculations.py` to add new financial formulas.

### Adjust Styling
Modify the CSS in `app.py` under the `st.markdown()` section at the top.

## 📈 Future Enhancements (Roadmap)

- [x] **Phase 1**: Core MVP - Income statement, charts, unit economics ✅
- [x] **Phase 2**: Break-even analysis, COGS breakdown, change history, scenario management ✅
- [ ] **Phase 3**: Scenario comparison (side-by-side), pre-configured scenarios (Conservative/Optimistic)
- [ ] **Phase 4**: Model validation checks with red/yellow/green flags, export to Excel
- [ ] **Phase 5**: Mobile optimization, print-friendly view, keyboard shortcuts

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Make sure you're in the right directory
cd "Pricing model dashboard"

# Verify Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Import errors
Make sure `calculations.py` and `data/defaults.json` are in the same directory as `app.py`.

### Charts not displaying
Update plotly: `pip install plotly --upgrade`

## 📞 Support

For issues or questions about:
- **The dashboard**: Check this README or open an issue
- **Streamlit**: Visit [docs.streamlit.io](https://docs.streamlit.io)
- **Deployment**: See platform-specific docs above

## 📄 License

This project is proprietary to Loop Box / Friendlier India.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) - Web framework
- [Plotly](https://plotly.com) - Interactive charts
- [Pandas](https://pandas.pydata.org) - Data manipulation

---

**Made with ❤️ for Loop Box** | Last updated: November 2025
