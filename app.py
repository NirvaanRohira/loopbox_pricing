"""
Loop Box Financial Dashboard
Interactive 3-year financial modeling tool with Phase 2 features
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime
from calculations import (
    calculate_full_income_statement,
    calculate_unit_economics,
    calculate_breakeven,
    calculate_sensitivity_analysis,
    generate_breakeven_chart_data,
    format_inr_lakhs,
    format_inr_crores,
    format_percentage
)

# Page configuration
st.set_page_config(
    page_title="Loop Box Financial Dashboard",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .change-history {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Load default values
@st.cache_data
def load_defaults():
    with open('data/defaults.json', 'r') as f:
        return json.load(f)

defaults = load_defaults()

# Initialize session state
if 'year_data' not in st.session_state:
    st.session_state.year_data = {
        'year1': defaults['year1'].copy(),
        'year2': defaults['year2'].copy(),
        'year3': defaults['year3'].copy()
    }

if 'change_history' not in st.session_state:
    st.session_state.change_history = []

if 'previous_year3_net_income' not in st.session_state:
    st.session_state.previous_year3_net_income = None

# Helper function to track changes
def track_change(variable_name, old_value, new_value, year):
    """Track changes to variables and their impact on Year 3 Net Income"""
    if old_value != new_value:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate Year 3 net income after change
        year3_data = st.session_state.year_data['year3']
        is_calc = calculate_full_income_statement(
            year3_data['pricing'],
            year3_data['volume'],
            year3_data['cogs'],
            year3_data['opex']
        )
        new_net_income = is_calc['net_income']

        # Calculate impact
        if st.session_state.previous_year3_net_income is not None:
            impact_abs = new_net_income - st.session_state.previous_year3_net_income
            impact_pct = (impact_abs / abs(st.session_state.previous_year3_net_income) * 100) if st.session_state.previous_year3_net_income != 0 else 0

            st.session_state.change_history.append({
                'timestamp': timestamp,
                'variable': variable_name,
                'year': year,
                'old_value': old_value,
                'new_value': new_value,
                'impact_abs': impact_abs,
                'impact_pct': impact_pct
            })

        st.session_state.previous_year3_net_income = new_net_income

# Save scenario to file
def save_scenario(scenario_name):
    """Save current scenario to JSON file"""
    scenario_data = {
        'name': scenario_name,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'year_data': st.session_state.year_data
    }

    os.makedirs('data/saved_scenarios', exist_ok=True)
    filename = f"data/saved_scenarios/{scenario_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, 'w') as f:
        json.dump(scenario_data, f, indent=2)

    return filename

# Load scenario from file
def load_scenario(filepath):
    """Load scenario from JSON file"""
    with open(filepath, 'r') as f:
        scenario_data = json.load(f)

    st.session_state.year_data = scenario_data['year_data']
    st.session_state.change_history = []
    st.session_state.previous_year3_net_income = None

# Get list of saved scenarios
def get_saved_scenarios():
    """Get list of saved scenario files"""
    scenario_dir = 'data/saved_scenarios'
    if os.path.exists(scenario_dir):
        files = [f for f in os.listdir(scenario_dir) if f.endswith('.json')]
        return sorted(files, reverse=True)
    return []

# Title
st.title("🔄 Loop Box Financial Dashboard")
st.markdown("**Interactive 3-Year Financial Model for Reusable Food Packaging** | Phase 2")

# Sidebar - Control Panel
with st.sidebar:
    st.header("📊 Control Panel")

    # Scenario management
    st.markdown("---")
    st.subheader("💾 Scenario Management")

    scenario_name = st.text_input("Scenario Name", value="Scenario_1")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True):
            filename = save_scenario(scenario_name)
            st.success(f"Saved!")

    with col2:
        saved_scenarios = get_saved_scenarios()
        if saved_scenarios:
            if st.button("🔄 Load", use_container_width=True):
                st.session_state.show_load_dialog = True

    if hasattr(st.session_state, 'show_load_dialog') and st.session_state.show_load_dialog:
        selected_scenario = st.selectbox("Select Scenario", saved_scenarios)
        if st.button("Load Selected"):
            load_scenario(f"data/saved_scenarios/{selected_scenario}")
            st.session_state.show_load_dialog = False
            st.rerun()

    st.markdown("---")

    # Auto-cascade option
    st.subheader("⚙️ Settings")
    auto_cascade = st.checkbox(
        "Auto-cascade Year 1 to Year 2 & 3",
        value=False,
        help="When enabled, changes to Year 1 will automatically apply growth rates to Years 2 & 3"
    )

    debug_mode = st.checkbox(
        "Debug Mode",
        value=False,
        help="Show calculation details and error information"
    )

    if auto_cascade:
        st.info("📊 Auto-cascade enabled: Year 2 & 3 will inherit Year 1 changes with growth adjustments")

    st.markdown("---")
    st.markdown("Adjust variables for each year")

    # Apply auto-cascade BEFORE rendering tabs (uses previous Year 1 values)
    if auto_cascade:
        year1 = st.session_state.year_data['year1']
        year2 = st.session_state.year_data['year2']
        year3 = st.session_state.year_data['year3']

        # Cascade pricing (with slight reductions for scale)
        year2['pricing']['container_price'] = int(year1['pricing']['container_price'] * 0.97)
        year3['pricing']['container_price'] = int(year2['pricing']['container_price'] * 0.97)

        year2['pricing']['monthly_fee'] = year1['pricing']['monthly_fee']
        year3['pricing']['monthly_fee'] = int(year1['pricing']['monthly_fee'] * 1.10)

        year2['pricing']['per_use_fee'] = year1['pricing']['per_use_fee']
        year3['pricing']['per_use_fee'] = year1['pricing']['per_use_fee']

        year2['pricing']['deposit'] = year1['pricing']['deposit']
        year3['pricing']['deposit'] = year1['pricing']['deposit']

        year2['pricing']['incentive'] = year1['pricing']['incentive']
        year3['pricing']['incentive'] = year1['pricing']['incentive']

        # Cascade COGS (with efficiency improvements)
        year2['cogs']['wash_cost'] = year1['cogs']['wash_cost'] * 0.92
        year3['cogs']['wash_cost'] = year2['cogs']['wash_cost'] * 0.91

        year2['cogs']['collection_cost'] = year1['cogs']['collection_cost'] * 0.90
        year3['cogs']['collection_cost'] = year2['cogs']['collection_cost'] * 0.89

        year2['cogs']['container_cost'] = year1['cogs']['container_cost']
        year3['cogs']['container_cost'] = year1['cogs']['container_cost']

        year2['cogs']['container_lifespan'] = year1['cogs']['container_lifespan']
        year3['cogs']['container_lifespan'] = year1['cogs']['container_lifespan']

        year2['cogs']['qc_batch_cost'] = year1['cogs']['qc_batch_cost']
        year3['cogs']['qc_batch_cost'] = year1['cogs']['qc_batch_cost']

        year2['cogs']['batches_per_month'] = year1['cogs']['batches_per_month']
        year3['cogs']['batches_per_month'] = year1['cogs']['batches_per_month']

        # NOTE: Volume and OpEx are NOT cascaded - each year has different scale
        # These should be set independently in defaults.json

    # Determine if Year 2/3 should be read-only
    year2_disabled = auto_cascade
    year3_disabled = auto_cascade

    if auto_cascade:
        st.warning("⚠️ Year 2 & 3 tabs are read-only (auto-calculated from Year 1)")

    year_tabs = st.tabs(["Year 1", "Year 2", "Year 3"])

    for idx, (year_key, tab) in enumerate(zip(['year1', 'year2', 'year3'], year_tabs)):
        with tab:
            year_data = st.session_state.year_data[year_key]

            # Determine if this year should be disabled
            is_disabled = False
            if year_key == 'year2' and year2_disabled:
                is_disabled = True
            elif year_key == 'year3' and year3_disabled:
                is_disabled = True

            st.subheader("💰 Pricing")
            year_data['pricing']['container_price'] = st.number_input(
                "Container Price (₹)", value=year_data['pricing']['container_price'],
                min_value=50, max_value=500, step=5, key=f"{year_key}_container_price",
                disabled=is_disabled
            )
            year_data['pricing']['monthly_fee'] = st.number_input(
                "Monthly Service Fee (₹)", value=year_data['pricing']['monthly_fee'],
                min_value=0, max_value=50000, step=500, key=f"{year_key}_monthly_fee"
            )
            year_data['pricing']['setup_fee'] = st.number_input(
                "Setup Fee (₹)", value=year_data['pricing']['setup_fee'],
                min_value=0, max_value=50000, step=1000, key=f"{year_key}_setup_fee"
            )
            year_data['pricing']['per_use_fee'] = st.number_input(
                "Per-Use Fee (₹)", value=year_data['pricing']['per_use_fee'],
                min_value=0.0, max_value=10.0, step=0.10, key=f"{year_key}_per_use_fee"
            )
            year_data['pricing']['deposit'] = st.number_input(
                "Customer Deposit (₹)", value=year_data['pricing']['deposit'],
                min_value=0, max_value=100, step=5, key=f"{year_key}_deposit"
            )
            year_data['pricing']['incentive'] = st.number_input(
                "Return Incentive (₹)", value=year_data['pricing']['incentive'],
                min_value=0, max_value=50, step=1, key=f"{year_key}_incentive"
            )

            if year_key == 'year3':
                st.markdown("**🚀 Aggregator (Zomato/Swiggy)**")
                year_data['pricing']['green_fee'] = st.number_input(
                    "Green Fee (₹)", value=year_data['pricing']['green_fee'],
                    min_value=0.0, max_value=20.0, step=0.50, key=f"{year_key}_green_fee"
                )
                year_data['pricing']['revenue_share_pct'] = st.slider(
                    "Revenue Share %", value=year_data['pricing']['revenue_share_pct'],
                    min_value=0.0, max_value=1.0, step=0.05, key=f"{year_key}_revenue_share"
                )

            st.subheader("📈 Volume")
            year_data['volume']['restaurants'] = st.number_input(
                "Total Restaurants", value=year_data['volume']['restaurants'],
                min_value=1, max_value=50000, step=50, key=f"{year_key}_restaurants"
            )
            year_data['volume']['new_restaurants'] = st.number_input(
                "New Restaurants Added", value=year_data['volume']['new_restaurants'],
                min_value=0, max_value=50000, step=50, key=f"{year_key}_new_restaurants"
            )
            year_data['volume']['orders_per_day'] = st.number_input(
                "Orders/Restaurant/Day", value=year_data['volume']['orders_per_day'],
                min_value=10, max_value=200, step=5, key=f"{year_key}_orders_per_day"
            )
            year_data['volume']['operating_days'] = st.number_input(
                "Operating Days", value=year_data['volume']['operating_days'],
                min_value=200, max_value=365, step=5, key=f"{year_key}_operating_days"
            )
            year_data['volume']['collection_rate'] = st.slider(
                "Collection Rate %", value=year_data['volume']['collection_rate'],
                min_value=0.5, max_value=1.0, step=0.01, key=f"{year_key}_collection_rate"
            )
            year_data['volume']['shrinkage'] = st.slider(
                "Shrinkage %", value=year_data['volume']['shrinkage'],
                min_value=0.0, max_value=0.20, step=0.01, key=f"{year_key}_shrinkage"
            )

            if year_key == 'year3':
                st.markdown("**🚀 Aggregator Volume**")
                year_data['volume']['zomato_orders_per_day'] = st.number_input(
                    "Zomato/Swiggy Orders/Day", value=year_data['volume']['zomato_orders_per_day'],
                    min_value=0, max_value=200000, step=1000, key=f"{year_key}_zomato_orders"
                )
                year_data['volume']['zomato_operating_days'] = st.number_input(
                    "Zomato/Swiggy Days", value=year_data['volume']['zomato_operating_days'],
                    min_value=0, max_value=365, step=10, key=f"{year_key}_zomato_days"
                )

            st.subheader("💸 COGS")
            year_data['cogs']['container_cost'] = st.number_input(
                "Container Cost (₹)", value=year_data['cogs']['container_cost'],
                min_value=50, max_value=500, step=5, key=f"{year_key}_container_cost"
            )
            year_data['cogs']['container_lifespan'] = st.number_input(
                "Container Lifespan (uses)", value=year_data['cogs']['container_lifespan'],
                min_value=50, max_value=300, step=10, key=f"{year_key}_lifespan"
            )
            year_data['cogs']['wash_cost'] = st.number_input(
                "Wash Cost/Container (₹)", value=year_data['cogs']['wash_cost'],
                min_value=0.5, max_value=20.0, step=0.10, key=f"{year_key}_wash_cost"
            )
            year_data['cogs']['collection_cost'] = st.number_input(
                "Collection Cost/Order (₹)", value=year_data['cogs']['collection_cost'],
                min_value=0.5, max_value=50.0, step=0.50, key=f"{year_key}_collection_cost"
            )
            year_data['cogs']['qc_batch_cost'] = st.number_input(
                "QC Batch Cost (₹)", value=year_data['cogs']['qc_batch_cost'],
                min_value=1000, max_value=100000, step=1000, key=f"{year_key}_qc_batch"
            )
            year_data['cogs']['batches_per_month'] = st.number_input(
                "Batches/Month", value=year_data['cogs']['batches_per_month'],
                min_value=1, max_value=50, step=1, key=f"{year_key}_batches"
            )

            st.subheader("🏢 OpEx")
            year_data['opex']['technology'] = st.number_input(
                "Technology (₹/year)", value=year_data['opex']['technology'],
                min_value=0, max_value=50000000, step=100000, key=f"{year_key}_tech"
            )
            year_data['opex']['marketing'] = st.number_input(
                "Marketing (₹/year)", value=year_data['opex']['marketing'],
                min_value=0, max_value=100000000, step=100000, key=f"{year_key}_marketing"
            )
            year_data['opex']['num_sales_people'] = st.number_input(
                "Sales Team Size", value=year_data['opex']['num_sales_people'],
                min_value=0, max_value=100, step=1, key=f"{year_key}_sales_people"
            )
            year_data['opex']['avg_salary'] = st.number_input(
                "Avg Salary/Person (₹/year)", value=year_data['opex']['avg_salary'],
                min_value=100000, max_value=5000000, step=50000, key=f"{year_key}_salary"
            )
            year_data['opex']['ga'] = st.number_input(
                "G&A (₹/year)", value=year_data['opex']['ga'],
                min_value=0, max_value=100000000, step=100000, key=f"{year_key}_ga"
            )
            year_data['opex']['num_hubs'] = st.number_input(
                "Number of Micro-Hubs", value=year_data['opex']['num_hubs'],
                min_value=1, max_value=100, step=1, key=f"{year_key}_hubs"
            )
            year_data['opex']['rent_per_hub'] = st.number_input(
                "Rent/Hub/Month (₹)", value=year_data['opex']['rent_per_hub'],
                min_value=10000, max_value=1000000, step=10000, key=f"{year_key}_rent"
            )
            year_data['opex']['utilities_per_hub'] = st.number_input(
                "Utilities/Hub/Month (₹)", value=year_data['opex']['utilities_per_hub'],
                min_value=5000, max_value=500000, step=5000, key=f"{year_key}_utilities"
            )
            year_data['opex']['workers_per_hub'] = st.number_input(
                "Workers/Hub", value=year_data['opex']['workers_per_hub'],
                min_value=1, max_value=50, step=1, key=f"{year_key}_workers"
            )
            year_data['opex']['worker_salary'] = st.number_input(
                "Worker Salary/Month (₹)", value=year_data['opex']['worker_salary'],
                min_value=5000, max_value=100000, step=1000, key=f"{year_key}_worker_salary"
            )

# Calculate income statements for all years
income_statements = {}
for year_key in ['year1', 'year2', 'year3']:
    year_data = st.session_state.year_data[year_key]
    income_statements[year_key] = calculate_full_income_statement(
        year_data['pricing'],
        year_data['volume'],
        year_data['cogs'],
        year_data['opex']
    )

# Update previous Year 3 net income for change tracking
if st.session_state.previous_year3_net_income is None:
    st.session_state.previous_year3_net_income = income_statements['year3']['net_income']

# Debug information
if debug_mode:
    with st.expander("🔍 Debug Information", expanded=False):
        st.write("**Year 1 Total Orders:**", income_statements['year1']['revenue']['total_orders'])
        st.write("**Year 2 Total Orders:**", income_statements['year2']['revenue']['total_orders'])
        st.write("**Year 3 Total Orders:**", income_statements['year3']['revenue']['total_orders'])
        try:
            import plotly
            st.write("**Plotly Version:**", plotly.__version__)
        except:
            st.write("**Plotly Version:**", "Unable to determine")
        st.write("**Auto-cascade Enabled:**", auto_cascade)
        st.write("**Year 2 Container Price (after cascade):**", st.session_state.year_data['year2']['pricing']['container_price'])
        st.write("**Year 3 Container Price (after cascade):**", st.session_state.year_data['year3']['pricing']['container_price'])

# Main Dashboard
st.markdown("---")

# Top Metrics Cards
st.header("📊 Key Metrics")
cols = st.columns(3)

years = ['year1', 'year2', 'year3']
year_labels = ['Year 1 (FY 2026)', 'Year 2 (FY 2027)', 'Year 3 (FY 2028)']

for idx, (col, year_key, year_label) in enumerate(zip(cols, years, year_labels)):
    with col:
        is_data = income_statements[year_key]

        # Calculate YoY growth for Year 2 and 3
        if idx > 0:
            prev_revenue = income_statements[years[idx-1]]['revenue']['total_revenue']
            current_revenue = is_data['revenue']['total_revenue']
            yoy_growth = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            revenue_label = f"Revenue (↑{yoy_growth:.1f}% YoY)" if yoy_growth >= 0 else f"Revenue (↓{abs(yoy_growth):.1f}% YoY)"
        else:
            revenue_label = "Revenue"

        st.metric(
            label=f"**{year_label}**",
            value=format_inr_crores(is_data['revenue']['total_revenue']),
            delta=None
        )

        ebitda_color = "🟢" if is_data['ebitda'] > 0 else "🔴"
        st.markdown(f"**EBITDA:** {ebitda_color} {format_inr_lakhs(is_data['ebitda'])}")

        margin_color = "🟢" if is_data['net_margin'] > 0 else "🔴"
        st.markdown(f"**Net Margin:** {margin_color} {format_percentage(is_data['net_margin'])}")

st.markdown("---")

# Income Statement
st.header("💰 Income Statement (3-Year View)")

# Create dataframe for income statement
is_data = {
    'Line Item': [
        'REVENUE',
        '  Container Usage Fees',
        '  Platform Subscriptions',
        '  Setup Fees',
        '  Aggregator Revenue',
        '  Deposit Shrinkage',
        'TOTAL REVENUE',
        '',
        'COST OF GOODS SOLD',
        '  Container Amortization',
        '  Washing & Sanitation',
        '  Collection & Logistics',
        '  Quality Control Testing',
        'TOTAL COGS',
        '',
        'GROSS PROFIT',
        'Gross Margin %',
        '',
        'OPERATING EXPENSES',
        '  Technology & Platform',
        '  Sales & Marketing',
        '  General & Administrative',
        '  Facility Costs (Micro-hubs)',
        'TOTAL OPEX',
        '',
        'EBITDA',
        'EBITDA Margin %',
        '',
        'OTHER ITEMS',
        '  Depreciation & Amortization',
        '  Interest Income',
        '',
        'NET INCOME',
        'Net Margin %'
    ]
}

for year_key, year_label in zip(years, year_labels):
    is_calc = income_statements[year_key]

    values = [
        '',  # REVENUE header
        format_inr_lakhs(is_calc['revenue']['usage_revenue']),
        format_inr_lakhs(is_calc['revenue']['subscription_revenue']),
        format_inr_lakhs(is_calc['revenue']['setup_revenue']),
        format_inr_lakhs(is_calc['revenue']['aggregator_revenue']),
        format_inr_lakhs(is_calc['revenue']['shrinkage_revenue']),
        format_inr_lakhs(is_calc['revenue']['total_revenue']),
        '',  # blank
        '',  # COGS header
        format_inr_lakhs(is_calc['cogs']['amortization']),
        format_inr_lakhs(is_calc['cogs']['washing']),
        format_inr_lakhs(is_calc['cogs']['collection']),
        format_inr_lakhs(is_calc['cogs']['qc']),
        format_inr_lakhs(is_calc['cogs']['total_cogs']),
        '',  # blank
        format_inr_lakhs(is_calc['gross_profit']),
        format_percentage(is_calc['gross_margin']),
        '',  # blank
        '',  # OPEX header
        format_inr_lakhs(is_calc['opex']['technology']),
        format_inr_lakhs(is_calc['opex']['marketing'] + is_calc['opex']['sales_salaries']),
        format_inr_lakhs(is_calc['opex']['ga']),
        format_inr_lakhs(is_calc['opex']['facility_costs']),
        format_inr_lakhs(is_calc['opex']['total_opex']),
        '',  # blank
        format_inr_lakhs(is_calc['ebitda']),
        format_percentage(is_calc['ebitda_margin']),
        '',  # blank
        '',  # OTHER header
        format_inr_lakhs(is_calc['other']['depreciation']),
        format_inr_lakhs(is_calc['other']['interest']),
        '',  # blank
        format_inr_lakhs(is_calc['net_income']),
        format_percentage(is_calc['net_margin'])
    ]

    is_data[year_label] = values

df_income_statement = pd.DataFrame(is_data)
st.dataframe(df_income_statement, use_container_width=True, hide_index=True)

st.markdown("---")

# Charts Section
st.header("📈 Visual Analytics")

col1, col2 = st.columns(2)

with col1:
    # Revenue Growth Chart
    st.subheader("Revenue Growth (3 Years)")

    try:
        revenue_data = {
            'Year': year_labels,
            'Revenue (₹ Crores)': [
                income_statements['year1']['revenue']['total_revenue'] / 10000000,
                income_statements['year2']['revenue']['total_revenue'] / 10000000,
                income_statements['year3']['revenue']['total_revenue'] / 10000000
            ]
        }

        fig_revenue = go.Figure(data=[
            go.Bar(
                x=revenue_data['Year'],
                y=revenue_data['Revenue (₹ Crores)'],
                marker_color=['#3498db', '#2ecc71', '#9b59b6'],
                text=[f"₹{val:.2f}Cr" for val in revenue_data['Revenue (₹ Crores)']],
                textposition='outside'
            )
        ])

        fig_revenue.update_layout(
            yaxis_title="Revenue (₹ Crores)",
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig_revenue, use_container_width=True, key="revenue_chart")
    except Exception as e:
        st.error(f"Error rendering revenue chart: {str(e)}")
        if debug_mode:
            st.exception(e)

with col2:
    # Margin Progression Chart
    st.subheader("Margin Progression")

    margin_data = {
        'Year': year_labels,
        'Gross Margin': [
            income_statements['year1']['gross_margin'],
            income_statements['year2']['gross_margin'],
            income_statements['year3']['gross_margin']
        ],
        'EBITDA Margin': [
            income_statements['year1']['ebitda_margin'],
            income_statements['year2']['ebitda_margin'],
            income_statements['year3']['ebitda_margin']
        ],
        'Net Margin': [
            income_statements['year1']['net_margin'],
            income_statements['year2']['net_margin'],
            income_statements['year3']['net_margin']
        ]
    }

    fig_margins = go.Figure()

    fig_margins.add_trace(go.Scatter(
        x=margin_data['Year'],
        y=margin_data['Gross Margin'],
        mode='lines+markers',
        name='Gross Margin %',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=10)
    ))

    fig_margins.add_trace(go.Scatter(
        x=margin_data['Year'],
        y=margin_data['EBITDA Margin'],
        mode='lines+markers',
        name='EBITDA Margin %',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10)
    ))

    fig_margins.add_trace(go.Scatter(
        x=margin_data['Year'],
        y=margin_data['Net Margin'],
        mode='lines+markers',
        name='Net Margin %',
        line=dict(color='#9b59b6', width=3),
        marker=dict(size=10)
    ))

    fig_margins.update_layout(
        yaxis_title="Margin (%)",
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig_margins, use_container_width=True)

# COGS Breakdown Chart (Phase 2)
st.subheader("💸 COGS Breakdown (3 Years)")

cogs_breakdown_data = {
    'Year': year_labels,
    'Amortization': [
        income_statements['year1']['cogs']['amortization'] / 100000,
        income_statements['year2']['cogs']['amortization'] / 100000,
        income_statements['year3']['cogs']['amortization'] / 100000
    ],
    'Washing': [
        income_statements['year1']['cogs']['washing'] / 100000,
        income_statements['year2']['cogs']['washing'] / 100000,
        income_statements['year3']['cogs']['washing'] / 100000
    ],
    'Collection': [
        income_statements['year1']['cogs']['collection'] / 100000,
        income_statements['year2']['cogs']['collection'] / 100000,
        income_statements['year3']['cogs']['collection'] / 100000
    ],
    'QC Testing': [
        income_statements['year1']['cogs']['qc'] / 100000,
        income_statements['year2']['cogs']['qc'] / 100000,
        income_statements['year3']['cogs']['qc'] / 100000
    ]
}

fig_cogs = go.Figure(data=[
    go.Bar(name='Amortization', x=cogs_breakdown_data['Year'], y=cogs_breakdown_data['Amortization'], marker_color='#e74c3c'),
    go.Bar(name='Washing', x=cogs_breakdown_data['Year'], y=cogs_breakdown_data['Washing'], marker_color='#3498db'),
    go.Bar(name='Collection', x=cogs_breakdown_data['Year'], y=cogs_breakdown_data['Collection'], marker_color='#f39c12'),
    go.Bar(name='QC Testing', x=cogs_breakdown_data['Year'], y=cogs_breakdown_data['QC Testing'], marker_color='#95a5a6')
])

fig_cogs.update_layout(
    barmode='stack',
    yaxis_title='Cost (₹ Lakhs)',
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_cogs, use_container_width=True)

# Revenue Mix Pie Charts
st.subheader("Revenue Mix by Year")
pie_cols = st.columns(3)

for idx, (col, year_key, year_label) in enumerate(zip(pie_cols, years, year_labels)):
    with col:
        is_calc = income_statements[year_key]

        labels = ['Usage Fees', 'Subscriptions', 'Setup Fees', 'Aggregator', 'Deposit Shrinkage']
        values = [
            is_calc['revenue']['usage_revenue'],
            is_calc['revenue']['subscription_revenue'],
            is_calc['revenue']['setup_revenue'],
            is_calc['revenue']['aggregator_revenue'],
            is_calc['revenue']['shrinkage_revenue']
        ]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker_colors=['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c']
        )])

        fig_pie.update_layout(
            title=year_label,
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )

        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Unit Economics Section
st.header("📊 Unit Economics")

unit_cols = st.columns(3)

for col, year_key, year_label in zip(unit_cols, years, year_labels):
    with col:
        is_calc = income_statements[year_key]
        unit_econ = calculate_unit_economics(is_calc)

        st.subheader(year_label)

        st.markdown("**Per Order Metrics:**")
        st.markdown(f"• Revenue/Order: ₹{unit_econ['revenue_per_order']:.2f}")
        st.markdown(f"• COGS/Order: ₹{unit_econ['cogs_per_order']:.2f}")
        st.markdown(f"• Gross Profit/Order: ₹{unit_econ['gross_profit_per_order']:.2f}")
        st.markdown(f"• OpEx/Order: ₹{unit_econ['opex_per_order']:.2f}")

        st.markdown("**Per Restaurant Metrics:**")
        year_data = st.session_state.year_data[year_key]
        annual_revenue_per_restaurant = is_calc['revenue']['total_revenue'] / year_data['volume']['restaurants']
        annual_orders_per_restaurant = year_data['volume']['orders_per_day'] * year_data['volume']['operating_days']

        st.markdown(f"• Annual Revenue: {format_inr_lakhs(annual_revenue_per_restaurant)}")
        st.markdown(f"• Monthly Revenue: {format_inr_lakhs(annual_revenue_per_restaurant/12)}")
        st.markdown(f"• Annual Orders: {annual_orders_per_restaurant:,.0f}")

st.markdown("---")

# PHASE 2: Break-Even Analysis
st.header("🎯 Break-Even Analysis")

# Calculate break-even for Year 3 (most relevant)
year3_data = st.session_state.year_data['year3']
breakeven = calculate_breakeven(
    year3_data['pricing'],
    year3_data['volume'],
    year3_data['cogs'],
    year3_data['opex']
)

# Break-even metrics
be_cols = st.columns(4)

with be_cols[0]:
    st.metric("Fixed Costs (Annual)", format_inr_lakhs(breakeven['fixed_costs_annual']))

with be_cols[1]:
    st.metric("Variable Cost/Order", f"₹{breakeven['variable_cost_per_order']:.2f}")

with be_cols[2]:
    st.metric("Revenue/Order", f"₹{breakeven['revenue_per_order']:.2f}")

with be_cols[3]:
    st.metric("Contribution Margin/Order", f"₹{breakeven['contribution_margin_per_order']:.2f}")

st.markdown("")

be_cols2 = st.columns(3)

with be_cols2[0]:
    be_orders = breakeven['breakeven_orders']
    if be_orders != float('inf'):
        st.metric("Break-Even Orders Needed", f"{be_orders:,.0f}")
    else:
        st.metric("Break-Even Orders Needed", "∞ (Negative margin)")

with be_cols2[1]:
    be_restaurants = breakeven['breakeven_restaurants']
    if be_restaurants != float('inf'):
        st.metric("Break-Even Restaurants", f"{be_restaurants:,.0f}")
    else:
        st.metric("Break-Even Restaurants", "∞ (Negative margin)")

with be_cols2[2]:
    be_months = breakeven['months_to_breakeven']
    if be_months != float('inf'):
        st.metric("Months to Break-Even", f"{be_months:.1f}")
    else:
        st.metric("Months to Break-Even", "∞ (Negative margin)")

st.markdown("---")

# Break-Even Chart
st.subheader("📉 Break-Even Visualization")

year3_total_orders = year3_data['volume']['restaurants'] * year3_data['volume']['orders_per_day'] * year3_data['volume']['operating_days']
chart_data = generate_breakeven_chart_data(
    year3_data['pricing'],
    year3_data['volume'],
    year3_data['cogs'],
    year3_data['opex'],
    year3_total_orders
)

fig_breakeven = go.Figure()

# Revenue line
fig_breakeven.add_trace(go.Scatter(
    x=chart_data['orders_range'],
    y=chart_data['revenue_line'],
    mode='lines',
    name='Total Revenue',
    line=dict(color='#2ecc71', width=3)
))

# Cost line
fig_breakeven.add_trace(go.Scatter(
    x=chart_data['orders_range'],
    y=chart_data['cost_line'],
    mode='lines',
    name='Total Costs',
    line=dict(color='#e74c3c', width=3)
))

# Break-even point marker
if chart_data['breakeven_point'] != float('inf'):
    be_revenue = chart_data['breakeven_point'] * breakeven['revenue_per_order']
    fig_breakeven.add_trace(go.Scatter(
        x=[chart_data['breakeven_point']],
        y=[be_revenue],
        mode='markers',
        name='Break-Even Point',
        marker=dict(size=15, color='#f39c12', symbol='star')
    ))

fig_breakeven.update_layout(
    xaxis_title='Number of Orders',
    yaxis_title='Amount (₹)',
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_breakeven, use_container_width=True)

st.markdown("---")

# Sensitivity Analysis
st.subheader("🔍 Sensitivity Analysis - Break-Even Impact")

sensitivity = calculate_sensitivity_analysis(
    year3_data['pricing'],
    year3_data['volume'],
    year3_data['cogs'],
    year3_data['opex']
)

sensitivity_df = pd.DataFrame({
    'Scenario': [
        'Base Case',
        'Collection Rate -10%',
        'Wash Cost +20%',
        'Per-Use Fee +₹0.50',
        'Orders/Day = 40'
    ],
    'Break-Even Orders': [
        f"{sensitivity['base']['breakeven_orders']:,.0f}" if sensitivity['base']['breakeven_orders'] != float('inf') else '∞',
        f"{sensitivity['collection_rate_drop']['breakeven_orders']:,.0f}" if sensitivity['collection_rate_drop']['breakeven_orders'] != float('inf') else '∞',
        f"{sensitivity['wash_cost_increase']['breakeven_orders']:,.0f}" if sensitivity['wash_cost_increase']['breakeven_orders'] != float('inf') else '∞',
        f"{sensitivity['per_use_fee_increase']['breakeven_orders']:,.0f}" if sensitivity['per_use_fee_increase']['breakeven_orders'] != float('inf') else '∞',
        f"{sensitivity['orders_per_day_drop']['breakeven_orders']:,.0f}" if sensitivity['orders_per_day_drop']['breakeven_orders'] != float('inf') else '∞'
    ],
    'Break-Even Restaurants': [
        f"{sensitivity['base']['breakeven_restaurants']:,.0f}" if sensitivity['base']['breakeven_restaurants'] != float('inf') else '∞',
        f"{sensitivity['collection_rate_drop']['breakeven_restaurants']:,.0f}" if sensitivity['collection_rate_drop']['breakeven_restaurants'] != float('inf') else '∞',
        f"{sensitivity['wash_cost_increase']['breakeven_restaurants']:,.0f}" if sensitivity['wash_cost_increase']['breakeven_restaurants'] != float('inf') else '∞',
        f"{sensitivity['per_use_fee_increase']['breakeven_restaurants']:,.0f}" if sensitivity['per_use_fee_increase']['breakeven_restaurants'] != float('inf') else '∞',
        f"{sensitivity['orders_per_day_drop']['breakeven_restaurants']:,.0f}" if sensitivity['orders_per_day_drop']['breakeven_restaurants'] != float('inf') else '∞'
    ],
    'Months to Break-Even': [
        f"{sensitivity['base']['months_to_breakeven']:.1f}" if sensitivity['base']['months_to_breakeven'] != float('inf') else '∞',
        f"{sensitivity['collection_rate_drop']['months_to_breakeven']:.1f}" if sensitivity['collection_rate_drop']['months_to_breakeven'] != float('inf') else '∞',
        f"{sensitivity['wash_cost_increase']['months_to_breakeven']:.1f}" if sensitivity['wash_cost_increase']['months_to_breakeven'] != float('inf') else '∞',
        f"{sensitivity['per_use_fee_increase']['months_to_breakeven']:.1f}" if sensitivity['per_use_fee_increase']['months_to_breakeven'] != float('inf') else '∞',
        f"{sensitivity['orders_per_day_drop']['months_to_breakeven']:.1f}" if sensitivity['orders_per_day_drop']['months_to_breakeven'] != float('inf') else '∞'
    ]
})

st.dataframe(sensitivity_df, use_container_width=True, hide_index=True)

st.markdown("---")

# PHASE 2: Change History Tracker
st.header("📜 Change History")

with st.expander("View Change History", expanded=False):
    if len(st.session_state.change_history) > 0:
        history_df = pd.DataFrame(st.session_state.change_history)

        # Format the dataframe
        history_df['impact_display'] = history_df.apply(
            lambda row: f"{format_inr_lakhs(row['impact_abs'])} ({'+' if row['impact_pct'] >= 0 else ''}{row['impact_pct']:.1f}%)",
            axis=1
        )

        display_df = history_df[['timestamp', 'year', 'variable', 'old_value', 'new_value', 'impact_display']]
        display_df.columns = ['Timestamp', 'Year', 'Variable', 'Old Value', 'New Value', 'Impact on Year 3 Net Income']

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Download as CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History as CSV",
            data=csv,
            file_name=f"change_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear History"):
            st.session_state.change_history = []
            st.rerun()
    else:
        st.info("No changes tracked yet. Adjust variables in the sidebar to see change impacts.")

st.markdown("---")

# Footer
st.markdown("---")
st.markdown("**Loop Box Financial Dashboard - Phase 2** | Built with Streamlit")
st.markdown("💡 *Adjust variables in the sidebar to see real-time updates and track changes*")
