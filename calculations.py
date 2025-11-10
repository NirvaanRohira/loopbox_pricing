"""
Financial calculation functions for Loop Box Dashboard
"""

def calculate_revenue(pricing, volume):
    """Calculate all revenue streams"""

    # Total orders
    total_orders = volume['restaurants'] * volume['orders_per_day'] * volume['operating_days']

    # Usage revenue (per-use fees)
    usage_revenue = total_orders * pricing['per_use_fee']

    # Subscription revenue (monthly fees)
    subscription_revenue = volume['restaurants'] * pricing['monthly_fee'] * (volume['operating_days'] / 30)

    # Setup revenue
    setup_revenue = volume['new_restaurants'] * pricing['setup_fee']

    # Deposit shrinkage revenue
    shrinkage_revenue = total_orders * pricing['deposit'] * volume['shrinkage']

    # Aggregator revenue (Zomato/Swiggy)
    aggregator_revenue = (volume['zomato_orders_per_day'] *
                         volume['zomato_operating_days'] *
                         pricing['green_fee'] *
                         pricing['revenue_share_pct'])

    total_revenue = (usage_revenue + subscription_revenue + setup_revenue +
                    shrinkage_revenue + aggregator_revenue)

    return {
        'total_orders': total_orders,
        'usage_revenue': usage_revenue,
        'subscription_revenue': subscription_revenue,
        'setup_revenue': setup_revenue,
        'shrinkage_revenue': shrinkage_revenue,
        'aggregator_revenue': aggregator_revenue,
        'total_revenue': total_revenue
    }


def calculate_cogs(cogs, volume, total_orders):
    """Calculate Cost of Goods Sold"""

    # Container amortization
    amortization_per_order = cogs['container_cost'] / cogs['container_lifespan']
    amortization = total_orders * amortization_per_order

    # Washing costs (only for collected containers)
    washing = total_orders * volume['collection_rate'] * cogs['wash_cost']

    # Collection/logistics costs
    collection = total_orders * cogs['collection_cost']

    # QC testing costs
    qc = cogs['qc_batch_cost'] * cogs['batches_per_month'] * (volume['operating_days'] / 30)

    total_cogs = amortization + washing + collection + qc

    return {
        'amortization': amortization,
        'washing': washing,
        'collection': collection,
        'qc': qc,
        'total_cogs': total_cogs,
        'amortization_per_order': amortization_per_order
    }


def calculate_opex(opex, volume):
    """Calculate Operating Expenses"""

    # Sales salaries
    sales_salaries = opex['num_sales_people'] * opex['avg_salary']

    # Facility costs (micro-hubs)
    months_operating = volume['operating_days'] / 30

    facility_rent = opex['num_hubs'] * opex['rent_per_hub'] * months_operating
    facility_utilities = opex['num_hubs'] * opex['utilities_per_hub'] * months_operating
    facility_labor = opex['num_hubs'] * opex['workers_per_hub'] * opex['worker_salary'] * months_operating

    facility_costs = facility_rent + facility_utilities + facility_labor

    total_opex = (opex['technology'] + opex['marketing'] + sales_salaries +
                  opex['ga'] + facility_costs)

    return {
        'technology': opex['technology'],
        'marketing': opex['marketing'],
        'sales_salaries': sales_salaries,
        'ga': opex['ga'],
        'facility_costs': facility_costs,
        'total_opex': total_opex
    }


def calculate_other_items(volume, restaurants):
    """Calculate depreciation and interest"""

    # Simplified depreciation based on scale
    if volume['operating_days'] < 365:
        depreciation = -2500000
    elif restaurants < 2000:
        depreciation = -6000000
    else:
        depreciation = -14500000

    # Simplified interest income
    if volume['operating_days'] < 365:
        interest = 250000
    elif restaurants < 2000:
        interest = 500000
    else:
        interest = 1500000

    return {
        'depreciation': depreciation,
        'interest': interest
    }


def calculate_full_income_statement(pricing, volume, cogs, opex):
    """Calculate complete income statement"""

    # Revenue
    revenue = calculate_revenue(pricing, volume)

    # COGS
    cogs_calc = calculate_cogs(cogs, volume, revenue['total_orders'])

    # Gross Profit
    gross_profit = revenue['total_revenue'] - cogs_calc['total_cogs']
    gross_margin = (gross_profit / revenue['total_revenue'] * 100) if revenue['total_revenue'] > 0 else 0

    # OpEx
    opex_calc = calculate_opex(opex, volume)

    # EBITDA
    ebitda = gross_profit - opex_calc['total_opex']
    ebitda_margin = (ebitda / revenue['total_revenue'] * 100) if revenue['total_revenue'] > 0 else 0

    # Other items
    other = calculate_other_items(volume, volume['restaurants'])

    # Net Income
    net_income = ebitda + other['depreciation'] + other['interest']
    net_margin = (net_income / revenue['total_revenue'] * 100) if revenue['total_revenue'] > 0 else 0

    return {
        'revenue': revenue,
        'cogs': cogs_calc,
        'gross_profit': gross_profit,
        'gross_margin': gross_margin,
        'opex': opex_calc,
        'ebitda': ebitda,
        'ebitda_margin': ebitda_margin,
        'other': other,
        'net_income': net_income,
        'net_margin': net_margin
    }


def calculate_unit_economics(income_statement):
    """Calculate per-order and per-restaurant metrics"""

    total_orders = income_statement['revenue']['total_orders']
    total_revenue = income_statement['revenue']['total_revenue']
    total_cogs = income_statement['cogs']['total_cogs']
    total_opex = income_statement['opex']['total_opex']

    # Per order metrics
    revenue_per_order = total_revenue / total_orders if total_orders > 0 else 0
    cogs_per_order = total_cogs / total_orders if total_orders > 0 else 0
    gross_profit_per_order = revenue_per_order - cogs_per_order
    opex_per_order = total_opex / total_orders if total_orders > 0 else 0

    return {
        'revenue_per_order': revenue_per_order,
        'cogs_per_order': cogs_per_order,
        'gross_profit_per_order': gross_profit_per_order,
        'opex_per_order': opex_per_order
    }


def format_inr_lakhs(amount):
    """Format amount in INR Lakhs (1 Lakh = 100,000)"""
    lakhs = amount / 100000
    return f"₹{lakhs:,.1f}L"


def format_inr_crores(amount):
    """Format amount in INR Crores (1 Crore = 10,000,000)"""
    crores = amount / 10000000
    return f"₹{crores:,.2f}Cr"


def format_percentage(value):
    """Format percentage with 1 decimal place"""
    return f"{value:.1f}%"


def calculate_breakeven(pricing, volume, cogs, opex):
    """Calculate break-even analysis metrics"""

    # Calculate fixed costs (annual OpEx + depreciation)
    opex_calc = calculate_opex(opex, volume)
    other = calculate_other_items(volume, volume['restaurants'])
    fixed_costs_annual = opex_calc['total_opex'] + abs(other['depreciation'])

    # Calculate variable costs per order
    amortization_per_order = cogs['container_cost'] / cogs['container_lifespan']
    wash_cost_per_order = cogs['wash_cost'] * volume['collection_rate']
    collection_cost_per_order = cogs['collection_cost']

    # QC is semi-variable, treat as fixed for simplicity
    variable_cost_per_order = (amortization_per_order +
                              wash_cost_per_order +
                              collection_cost_per_order)

    # Calculate revenue per order
    # For break-even, we consider recurring revenue sources
    revenue_per_order = pricing['per_use_fee']

    # Add monthly fee and setup fee allocated per order
    if volume['orders_per_day'] > 0 and volume['operating_days'] > 0:
        total_orders_estimate = volume['restaurants'] * volume['orders_per_day'] * volume['operating_days']
        if total_orders_estimate > 0:
            monthly_fee_per_order = (volume['restaurants'] * pricing['monthly_fee'] *
                                    (volume['operating_days'] / 30)) / total_orders_estimate
            setup_fee_per_order = (volume['new_restaurants'] * pricing['setup_fee']) / total_orders_estimate
            deposit_per_order = pricing['deposit'] * volume['shrinkage']
            revenue_per_order += monthly_fee_per_order + setup_fee_per_order + deposit_per_order

    # Add aggregator revenue per order if applicable
    if volume['zomato_orders_per_day'] > 0 and volume['zomato_operating_days'] > 0:
        total_orders_with_aggregator = (volume['restaurants'] * volume['orders_per_day'] *
                                       volume['operating_days'] +
                                       volume['zomato_orders_per_day'] * volume['zomato_operating_days'])
        aggregator_revenue_total = (volume['zomato_orders_per_day'] *
                                   volume['zomato_operating_days'] *
                                   pricing['green_fee'] *
                                   pricing['revenue_share_pct'])
        if total_orders_with_aggregator > 0:
            revenue_per_order += aggregator_revenue_total / total_orders_with_aggregator

    # Contribution margin per order
    contribution_margin_per_order = revenue_per_order - variable_cost_per_order

    # Break-even orders
    if contribution_margin_per_order > 0:
        breakeven_orders = fixed_costs_annual / contribution_margin_per_order
    else:
        breakeven_orders = float('inf')

    # Break-even restaurants
    if volume['orders_per_day'] > 0 and volume['operating_days'] > 0:
        orders_per_restaurant_annual = volume['orders_per_day'] * volume['operating_days']
        breakeven_restaurants = breakeven_orders / orders_per_restaurant_annual if orders_per_restaurant_annual > 0 else float('inf')
    else:
        breakeven_restaurants = float('inf')

    # Months to break-even (assuming linear ramp from 0 to Year 1 target)
    if volume['orders_per_day'] > 0 and volume['restaurants'] > 0:
        year1_total_orders = volume['restaurants'] * volume['orders_per_day'] * volume['operating_days']
        # Assume we reach year1 target in 12 months with linear growth
        # Average monthly orders = year1_total_orders / operating_days * 30
        avg_daily_orders = volume['restaurants'] * volume['orders_per_day']
        # Assuming linear ramp from 0, we reach full capacity at month 12
        # With linear growth: cumulative orders at month M = (avg_daily_orders * 30 * M * M) / 24
        # Solving for breakeven is complex, use simplified approach
        if year1_total_orders > 0 and contribution_margin_per_order > 0:
            # Simplified: assume constant order rate for calculation
            months_to_breakeven = (breakeven_orders / year1_total_orders) * 12
        else:
            months_to_breakeven = float('inf')
    else:
        months_to_breakeven = float('inf')

    return {
        'fixed_costs_annual': fixed_costs_annual,
        'variable_cost_per_order': variable_cost_per_order,
        'revenue_per_order': revenue_per_order,
        'contribution_margin_per_order': contribution_margin_per_order,
        'breakeven_orders': breakeven_orders,
        'breakeven_restaurants': breakeven_restaurants,
        'months_to_breakeven': months_to_breakeven
    }


def calculate_sensitivity_analysis(pricing, volume, cogs, opex):
    """Calculate sensitivity scenarios for break-even analysis"""

    # Base case
    base_breakeven = calculate_breakeven(pricing, volume, cogs, opex)

    # Scenario 1: Collection rate drops by 10%
    volume_s1 = volume.copy()
    volume_s1['collection_rate'] = max(0.5, volume['collection_rate'] - 0.10)
    s1_breakeven = calculate_breakeven(pricing, volume_s1, cogs, opex)

    # Scenario 2: Washing costs increase by 20%
    cogs_s2 = cogs.copy()
    cogs_s2['wash_cost'] = cogs['wash_cost'] * 1.20
    s2_breakeven = calculate_breakeven(pricing, volume, cogs_s2, opex)

    # Scenario 3: Per-use fee increases by ₹0.50
    pricing_s3 = pricing.copy()
    pricing_s3['per_use_fee'] = pricing['per_use_fee'] + 0.50
    s3_breakeven = calculate_breakeven(pricing_s3, volume, cogs, opex)

    # Scenario 4: Orders per restaurant drops to 40/day
    volume_s4 = volume.copy()
    volume_s4['orders_per_day'] = 40
    s4_breakeven = calculate_breakeven(pricing, volume_s4, cogs, opex)

    return {
        'base': base_breakeven,
        'collection_rate_drop': s1_breakeven,
        'wash_cost_increase': s2_breakeven,
        'per_use_fee_increase': s3_breakeven,
        'orders_per_day_drop': s4_breakeven
    }


def generate_breakeven_chart_data(pricing, volume, cogs, opex, year3_orders):
    """Generate data for break-even visualization chart"""

    breakeven = calculate_breakeven(pricing, volume, cogs, opex)

    # Generate order range from 0 to 150% of Year 3 target
    max_orders = int(year3_orders * 1.5)
    order_steps = 20  # Number of data points
    step_size = max_orders // order_steps

    orders_range = [i * step_size for i in range(order_steps + 1)]

    # Calculate total revenue and total costs for each order level
    revenue_line = []
    cost_line = []

    opex_calc = calculate_opex(opex, volume)
    other = calculate_other_items(volume, volume['restaurants'])
    fixed_costs = opex_calc['total_opex'] + abs(other['depreciation'])

    for orders in orders_range:
        # Revenue calculation (simplified - per order revenue * orders)
        total_revenue = orders * breakeven['revenue_per_order']
        revenue_line.append(total_revenue)

        # Cost calculation (fixed + variable)
        total_cost = fixed_costs + (orders * breakeven['variable_cost_per_order'])
        cost_line.append(total_cost)

    return {
        'orders_range': orders_range,
        'revenue_line': revenue_line,
        'cost_line': cost_line,
        'breakeven_point': breakeven['breakeven_orders']
    }
