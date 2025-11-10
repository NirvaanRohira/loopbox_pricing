```markdown
# Loop Box Financial Dashboard - Development Brief

## Project Overview
Build an interactive financial modeling dashboard for Loop Box, a reusable food packaging business in India. The dashboard should allow real-time manipulation of pricing, costs, and volume assumptions to forecast profitability across 3 years.

## Business Model Summary
Loop Box operates a closed-loop reusable container system for:
- **Food courts** (controlled environments)
- **Corporate cafeterias** 
- **College campuses**
- **Future:** Delivery integration with Zomato/Swiggy

**How it works:**
1. Restaurants BUY containers from Loop Box (₹150-200 per unit)
2. Customers eat and dispose in Loop Box bins (get small cash incentive ₹5-10)
3. Loop Box collects, washes, sanitizes at micro-hubs
4. Clean containers delivered back to restaurants
5. Repeat 100+ times per container

**Revenue Streams:**
- Container sales to restaurants (one-time)
- Monthly service fees (₹2,000-10,000 for collection + washing)
- Per-use fees (₹0.50-1.50 per cycle)
- Setup fees for onboarding (₹5,000-15,000)
- Customer deposit shrinkage (6-10% don't return containers)
- Future: Aggregator platform revenue share (45% of ₹4 "green fee")

## Technical Requirements

### Core Features

#### 1. Interactive Control Panel
Create sidebar with tabs for Year 1, Year 2, Year 3 containing:

**Pricing Variables:**
- Container sale price to restaurant (₹)
- Monthly service fee per restaurant (₹)
- Setup fee per new restaurant (₹)
- Per-use fee from restaurant (₹)
- Customer deposit amount (₹)
- Customer cash incentive for return (₹)
- Zomato/Swiggy green fee (₹) - Year 3 only
- Loop Box revenue share % - Year 3 only

**Volume Assumptions:**
- Total restaurants/institutions
- New restaurants added this year
- Average orders per restaurant per day
- Operating days in year
- Container collection rate % (slider 50-100%)
- Container loss/shrinkage % (slider 0-20%)
- Initial containers per restaurant
- Zomato/Swiggy daily orders (Year 3)
- Zomato/Swiggy operating days (Year 3)

**Cost Structure - COGS:**
- Container manufacturing cost (₹)
- Container lifespan (number of uses)
- Washing cost per container (₹)
- Collection/logistics cost per order (₹)
- QC testing cost per batch (₹)
- Number of batches per month

**Cost Structure - OpEx:**
- Technology & Platform (annual ₹)
- Sales & Marketing (annual ₹)
- Number of sales team members
- Average salary per sales person/year (₹)
- General & Administrative (annual ₹)
- Number of micro-hubs
- Rent per hub per month (₹)
- Equipment cost per hub (₹)
- Utilities per hub per month (₹)
- Workers per hub
- Salary per worker per month (₹)

#### 2. Main Dashboard Display

**Top Metrics Cards (3 columns):**
- Year 1: Revenue, EBITDA, Net Margin %
- Year 2: Revenue (with YoY growth %), EBITDA, Net Margin %
- Year 3: Revenue (with YoY growth %), EBITDA, Net Margin %

**Income Statement Table:**
Display side-by-side 3-year income statement with:
```
REVENUE
  Container Usage Fees
  Platform Subscriptions
  Setup Fees
  Aggregator Revenue (Zomato/Swiggy)
  Deposit Shrinkage
TOTAL REVENUE

COST OF GOODS SOLD
  Container Amortization
  Washing & Sanitation
  Collection & Logistics
  Quality Control Testing
TOTAL COGS

GROSS PROFIT
Gross Margin %

OPERATING EXPENSES
  Technology & Platform
  Sales & Marketing
  General & Administrative
  Facility Costs (Micro-hubs)
TOTAL OPEX

EBITDA
EBITDA Margin %

OTHER ITEMS
  Depreciation & Amortization
  Interest Income

NET INCOME
Net Margin %
```

All values in ₹ Lakhs (100,000s)

#### 3. Visual Analytics

**Chart 1: Revenue Growth**
- Bar chart showing Year 1, 2, 3 total revenue in ₹ Crores

**Chart 2: Margin Progression**
- Line chart with 3 lines:
  - Gross Margin %
  - EBITDA Margin %
  - Net Margin %

**Chart 3: Revenue Mix (3 pie charts side-by-side)**
- Year 1, 2, 3 breakdown of:
  - Usage Fees
  - Subscriptions
  - Setup Fees
  - Aggregator Revenue
  - Deposit Shrinkage

**Chart 4: COGS Breakdown (stacked bar or waterfall)**
- Show components: Amortization, Washing, Collection, QC

#### 4. Unit Economics Section

Display per-order metrics for each year:
- Revenue per order (₹)
- COGS per order (₹)
- Gross profit per order (₹)
- OpEx per order (₹)

Display per-restaurant metrics:
- Annual revenue per restaurant (₹)
- Monthly revenue per restaurant (₹)
- Annual orders per restaurant

#### 5. **NEW: Break-Even Analysis**

Create dedicated section showing:

**Break-Even Calculator:**
- Fixed costs (annual OpEx)
- Variable costs per order
- Contribution margin per order
- Break-even orders needed
- Break-even restaurants needed (at current order rate)
- Months to break-even (based on current ramp rate)

**Visual: Break-Even Chart**
- X-axis: Number of orders (0 to 150% of Year 3 target)
- Y-axis: ₹ (Revenue and Total Costs)
- Two lines: Total Revenue, Total Costs
- Mark intersection point as break-even

**Sensitivity Table: "What if?" scenarios**
Show break-even impact if:
- Collection rate drops by 10%
- Washing costs increase by 20%
- Per-use fee increases by ₹0.50
- Orders per restaurant drops to 40/day

#### 6. **NEW: Change History Tracker**

Add a collapsible section that logs changes:
```
Change History:
[Timestamp] | Variable Changed | Old Value | New Value | Impact on Year 3 Net Income
---
2025-11-12 14:23 | Washing Cost | ₹2.10 | ₹2.50 | -₹34.5L (-9.8%)
2025-11-12 14:25 | Per-use Fee | ₹1.00 | ₹1.20 | +₹18.2L (+5.2%)
```

Add buttons:
- "Save Current Scenario" (exports to JSON/CSV with timestamp)
- "Load Saved Scenario"
- "Compare Scenarios" (load 2-3 saved scenarios side-by-side)

#### 7. **NEW: Scenario Comparison**

Add tab for "Scenario Analysis" with 3 preset scenarios:

**Conservative:**
- Collection rate: 85%
- Orders per restaurant: 40/day
- All pricing: -10%
- All costs: +10%
- No Zomato integration

**Base Case:**
- Current assumptions (user's inputs)

**Optimistic:**
- Collection rate: 95%
- Orders per restaurant: 60/day
- Zomato integration starts Year 2 (not Year 3)
- Costs: -15% (economies of scale)

Display all 3 side-by-side with key metrics:
- Total 3-year revenue
- Year 3 EBITDA
- Cumulative cash burn
- Break-even month

#### 8. **NEW: Model Validation Checks**

Add "Health Check" section with automated flags:

**Red Flags (show warning icon):**
- Gross margin negative in Year 3
- EBITDA margin < -20% in Year 3
- Collection rate < 85%
- Revenue per order < COGS per order in Year 3
- Break-even beyond 48 months

**Yellow Flags (show caution icon):**
- Gross margin < 10% in Year 3
- Customer acquisition cost > ₹80,000
- Container utilization < 60 uses over lifespan
- OpEx > 40% of revenue in Year 3

**Green Flags (show checkmark):**
- Positive EBITDA by Year 3
- Gross margin > 20% by Year 3
- Collection rate > 90%
- Break-even within 36 months

#### 9. Export & Download

- Download Income Statement as CSV
- Download All Scenarios comparison as Excel
- Download Charts as PNG
- Export full model with inputs as JSON

## Default Values to Pre-populate

### Year 1 (FY 2026):
**Pricing:**
- Container price: ₹150
- Monthly fee: ₹5,000
- Setup fee: ₹0
- Per-use fee: ₹1.00
- Deposit: ₹15
- Incentive: ₹5

**Volume:**
- Restaurants: 300
- New restaurants: 300
- Orders/day: 50
- Operating days: 270
- Collection rate: 90%
- Shrinkage: 10%

**Costs:**
- Container cost: ₹150
- Lifespan: 100 uses
- Wash cost: ₹2.50
- Collection cost: ₹5.00
- QC batch: ₹25,000
- Batches/month: 1

**OpEx:**
- Technology: ₹70,00,000
- Marketing: ₹50,00,000
- Sales team: 5
- Salary: ₹6,00,000
- G&A: ₹70,00,000
- Hubs: 1
- Rent/hub: ₹1,50,000
- Equipment: ₹15,00,000
- Utilities: ₹1,00,000
- Workers/hub: 10
- Worker salary: ₹20,000

### Year 2 (FY 2027):
**Changes from Year 1:**
- Container price: ₹145
- Restaurants: 1,600
- New: 1,300
- Operating days: 365
- Collection rate: 92%
- Shrinkage: 8%
- Wash cost: ₹2.30
- Collection: ₹4.50
- Batches: 3
- Technology: ₹65,00,000
- Marketing: ₹1,37,00,000
- Sales team: 12
- G&A: ₹1,15,00,000
- Hubs: 3
- Setup fee: ₹8,000

### Year 3 (FY 2028):
**Additional changes:**
- Container price: ₹140
- Monthly fee: ₹5,500
- Setup fee: ₹10,000
- Green fee: ₹4.00
- Revenue share: 45%
- Zomato orders/day: 40,000
- Zomato days: 180
- Restaurants: 5,000
- New: 3,400
- Collection: 94%
- Shrinkage: 6%
- Wash: ₹2.10
- Collection: ₹4.00
- Batches: 10
- Tech: ₹1,00,00,000
- Marketing: ₹2,80,00,000
- Sales: 25
- G&A: ₹2,10,00,000
- Hubs: 10
- Workers/hub: 8
- Worker salary: ₹24,000

## Calculation Logic

### Revenue Calculations:
```python
total_orders = restaurants * orders_per_day * operating_days

usage_revenue = total_orders * per_use_fee

subscription_revenue = restaurants * monthly_fee * (operating_days / 30)

setup_revenue = new_restaurants * setup_fee

shrinkage_revenue = total_orders * deposit * shrinkage_rate

aggregator_revenue = zomato_orders * zomato_days * green_fee * revenue_share_pct

total_revenue = sum of all above
```

### COGS Calculations:
```python
amortization_per_order = container_cost / lifespan

amortization = total_orders * amortization_per_order

washing = total_orders * collection_rate * wash_cost

collection = total_orders * collection_cost

qc = qc_batch_cost * batches_per_month * (operating_days / 30)

total_cogs = amortization + washing + collection + qc

gross_profit = total_revenue - total_cogs
```

### OpEx Calculations:
```python
sales_salaries = num_sales_people * avg_salary

facility_costs = (
    (hubs * rent * (operating_days/30)) + 
    (hubs * utilities * (operating_days/30)) + 
    (hubs * workers * salary * (operating_days/30))
)

total_opex = tech + marketing + sales_salaries + ga + facility_costs

ebitda = gross_profit - total_opex
```

### Bottom Line:
```python
# Simplified depreciation
if operating_days < 365:
    depreciation = -2,500,000
elif restaurants < 2000:
    depreciation = -6,000,000
else:
    depreciation = -14,500,000

# Simplified interest
if operating_days < 365:
    interest = 250,000
elif restaurants < 2000:
    interest = 500,000
else:
    interest = 1,500,000

net_income = ebitda + depreciation + interest
```

### Break-Even Logic:
```python
fixed_costs_annual = total_opex + depreciation

variable_cost_per_order = (amortization_per_order + 
                           (wash_cost * collection_rate) + 
                           collection_cost)

contribution_margin_per_order = revenue_per_order - variable_cost_per_order

breakeven_orders = fixed_costs_annual / contribution_margin_per_order

breakeven_restaurants = breakeven_orders / (orders_per_day * operating_days)

# Assuming linear ramp-up from 0 to Year 1 target
monthly_order_growth = (year1_total_orders / operating_days) / 30
months_to_breakeven = breakeven_orders / monthly_order_growth / 30
```

## Tech Stack Recommendation

**Streamlit** (Python) - Best for:
- Fast development
- Beautiful UI out of the box
- Interactive widgets
- Easy deployment (Streamlit Cloud free tier)
- Great charting with Plotly

**Libraries needed:**
```bash
pip install streamlit pandas plotly openpyxl
```

## File Structure
```
loop-box-dashboard/
├── app.py                    # Main Streamlit application
├── calculations.py           # Financial calculation functions
├── data/
│   ├── defaults.json        # Default values for each year
│   └── saved_scenarios/     # User-saved scenarios
├── requirements.txt         # Python dependencies
└── README.md               # Setup instructions
```

## Key User Interactions to Enable

1. **Drag sliders** → See instant recalculation
2. **Click "Save Scenario"** → Download current state
3. **Upload saved scenario** → Restore previous state
4. **Toggle between scenarios** → Compare Conservative vs Optimistic
5. **Hover over charts** → See detailed tooltips
6. **Export any table** → Download as CSV/Excel
7. **Print-friendly view** → Generate PDF-ready summary

## Visual Design Notes

- **Color scheme:** Green (revenue/positive), Red (costs/negative), Blue (neutral metrics)
- **Currency format:** Always show ₹ symbol, use Indian numbering (Lakhs/Crores)
- **Margins:** Highlight when they turn positive (green badge)
- **Alerts:** Use warning icons for red flags, info icons for yellow flags
- **Mobile responsive:** Dashboard should work on tablets (min-width: 768px)

## Validation Business Logic

The model should automatically validate:

1. **Sanity checks:**
   - Revenue per order should be > 0
   - Collection rate should be 50-100%
   - Container lifespan should be 50-200 uses
   - Orders per restaurant should be 10-100/day

2. **Warning triggers:**
   - If gross margin stays negative all 3 years → "Business model not viable without major changes"
   - If break-even > 60 months → "Funding runway concerns"
   - If COGS per order > Revenue per order in Year 3 → "Unit economics broken"
   - If Zomato revenue = 0 in Year 3 but included in base model → "Critical revenue stream missing"

3. **Success indicators:**
   - Positive gross margin by Year 2
   - Positive EBITDA by Year 3
   - Collection rate sustained > 88%
   - LTV:CAC ratio > 2:1 by Year 3

## Questions to Answer with This Tool

The dashboard should help answer:
1. **At what per-use fee do we become profitable?**
2. **How many restaurants do we need to break even?**
3. **What if collection rates are only 80%?**
4. **Can we survive without Zomato partnership?**
5. **What's our biggest cost driver?** (should be obvious from charts)
6. **How much runway do we need before Series A?**
7. **What pricing changes have the biggest impact?**
8. **Is the business viable if we can't scale past 1,000 restaurants?**

## Development Phases

### Phase 1: Core (MVP)
- Control panel with all inputs
- Income statement calculations
- Basic metrics display
- Revenue and margin charts

### Phase 2: Analytics
- Unit economics section
- Break-even calculator
- COGS breakdown chart
- Revenue mix pie charts

### Phase 3: Advanced
- Change history tracker
- Scenario comparison
- Model validation checks
- Export functionality

### Phase 4: Polish
- Mobile responsiveness
- Print-friendly view
- Keyboard shortcuts
- Tour/onboarding flow

## Deployment Options

1. **Local:** `streamlit run app.py`
2. **Streamlit Cloud:** Free hosting, connect GitHub repo
3. **Heroku:** If need custom domain
4. **Docker:** For enterprise deployment

## Success Criteria

Dashboard is successful if:
- ✅ Non-technical users can adjust variables without confusion
- ✅ All calculations update in < 1 second
- ✅ Can export complete financial model to Excel
- ✅ Red flags are immediately obvious
- ✅ Can answer "what if?" questions in < 30 seconds
- ✅ Mobile-friendly for pitch meetings on tablets

---

## Reference Files

The complete Streamlit code structure is provided separately. Start with `app.py` and build calculations incrementally. Test each calculation function independently before integrating into the dashboard.

When ready to deploy, create a `requirements.txt`:
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
openpyxl>=3.1.0
```

Let me know if you need clarification on any calculations or want me to prioritize specific features!
```

---

**This markdown is ready to paste directly into Claude Code. It contains:**
✅ Complete business context
✅ All technical requirements 
✅ Default values for all 3 years
✅ Calculation logic with formulas
✅ Break-even calculator spec
✅ Change history tracker
✅ Model validation checks
✅ Scenario comparison
✅ Everything needed to build it

