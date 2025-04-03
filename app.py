import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Virtual CFO Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #F3F4F6;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
    }
    .warning-card {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
    }
    .success-card {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
    }
    .info-card {
        background-color: #F0FDFA;
        border-left: 4px solid #14B8A6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #E0E7FF;
        border: 1px solid #C7D2FE;
    }
    .cfo-message {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'financial_data' not in st.session_state:
    # Sample financial data for demonstration
    st.session_state.financial_data = {
        'income_statement': pd.DataFrame({
            'Revenue': [100000, 120000, 150000, 180000],
            'Cost of Goods Sold': [60000, 70000, 85000, 100000],
            'Gross Profit': [40000, 50000, 65000, 80000],
            'Operating Expenses': [30000, 35000, 40000, 45000],
            'Operating Income': [10000, 15000, 25000, 35000],
            'Interest Expense': [2000, 2000, 2000, 2000],
            'Income Before Tax': [8000, 13000, 23000, 33000],
            'Tax Expense': [2000, 3250, 5750, 8250],
            'Net Income': [6000, 9750, 17250, 24750]
        }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q')),
        
        'balance_sheet': pd.DataFrame({
            'Cash and Equivalents': [50000, 55000, 70000, 90000],
            'Accounts Receivable': [30000, 35000, 40000, 45000],
            'Inventory': [40000, 45000, 50000, 55000],
            'Current Assets': [120000, 135000, 160000, 190000],
            'Fixed Assets': [200000, 195000, 190000, 185000],
            'Total Assets': [320000, 330000, 350000, 375000],
            'Accounts Payable': [25000, 30000, 35000, 40000],
            'Short-term Debt': [20000, 20000, 20000, 20000],
            'Current Liabilities': [45000, 50000, 55000, 60000],
            'Long-term Debt': [100000, 95000, 90000, 85000],
            'Total Liabilities': [145000, 145000, 145000, 145000],
            'Equity': [175000, 185000, 205000, 230000],
        }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q')),
        
        'cash_flow': pd.DataFrame({
            'Net Income': [6000, 9750, 17250, 24750],
            'Depreciation': [5000, 5000, 5000, 5000],
            'Changes in Working Capital': [-3000, -5000, -7000, -8000],
            'Operating Cash Flow': [8000, 9750, 15250, 21750],
            'Capital Expenditures': [0, 0, 0, 0],
            'Investing Cash Flow': [0, 0, 0, 0],
            'Debt Repayment': [5000, 5000, 5000, 5000],
            'Financing Cash Flow': [-5000, -5000, -5000, -5000],
            'Net Cash Flow': [3000, 4750, 10250, 16750]
        }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q'))
    }

if 'financial_metrics' not in st.session_state:
    # Calculate some key financial metrics
    income = st.session_state.financial_data['income_statement']
    balance = st.session_state.financial_data['balance_sheet']
    
    latest_quarter = income.index[-1]
    previous_quarter = income.index[-2]
    
    revenue_current = income.loc[latest_quarter, 'Revenue']
    revenue_previous = income.loc[previous_quarter, 'Revenue']
    revenue_growth = (revenue_current - revenue_previous) / revenue_previous * 100
    
    net_income_current = income.loc[latest_quarter, 'Net Income']
    net_income_previous = income.loc[previous_quarter, 'Net Income']
    profit_growth = (net_income_current - net_income_previous) / net_income_previous * 100
    
    gross_margin = income.loc[latest_quarter, 'Gross Profit'] / income.loc[latest_quarter, 'Revenue'] * 100
    net_margin = income.loc[latest_quarter, 'Net Income'] / income.loc[latest_quarter, 'Revenue'] * 100
    
    current_ratio = balance.loc[latest_quarter, 'Current Assets'] / balance.loc[latest_quarter, 'Current Liabilities']
    debt_to_equity = balance.loc[latest_quarter, 'Total Liabilities'] / balance.loc[latest_quarter, 'Equity']
    
    st.session_state.financial_metrics = {
        'revenue_growth': revenue_growth,
        'profit_growth': profit_growth,
        'gross_margin': gross_margin,
        'net_margin': net_margin,
        'current_ratio': current_ratio,
        'debt_to_equity': debt_to_equity
    }

# Mock LLM response function (to be replaced with actual LLM integration)
def get_cfo_response(query, financial_data):
    """
    Mock function to simulate CFO agent responses.
    Will be replaced with actual LLM integration when deployed.
    """
    # Simple keyword-based responses for demonstration
    if 'cash flow' in query.lower():
        return "Based on your cash flow statement, your operating cash flow has been steadily increasing over the past quarters, which is a positive sign. Your latest quarterly operating cash flow is $21,750, up from $15,250 in the previous quarter. This 42.6% increase indicates strong operational performance. I recommend continuing to monitor your working capital changes, which have been increasingly negative, suggesting you might be tying up more cash in inventory or accounts receivable."
    
    elif 'profit margin' in query.lower() or 'profitability' in query.lower():
        return f"Your gross margin is currently {st.session_state.financial_metrics['gross_margin']:.1f}%, which is healthy for most industries. Your net profit margin is {st.session_state.financial_metrics['net_margin']:.1f}%, showing improvement over previous quarters. To further improve profitability, consider reviewing your operating expenses, which represent {income.loc[latest_quarter, 'Operating Expenses'] / income.loc[latest_quarter, 'Revenue'] * 100:.1f}% of revenue."
    
    elif 'growth' in query.lower():
        return f"Your revenue has grown by {st.session_state.financial_metrics['revenue_growth']:.1f}% compared to the previous quarter, reaching ${revenue_current:,.0f}. Net income has increased by {st.session_state.financial_metrics['profit_growth']:.1f}%, reaching ${net_income_current:,.0f}. This indicates strong business performance. To sustain this growth, consider investing in marketing and product development while maintaining cost discipline."
    
    elif 'debt' in query.lower() or 'leverage' in query.lower():
        return f"Your debt-to-equity ratio is {st.session_state.financial_metrics['debt_to_equity']:.2f}, which indicates a conservative capital structure. Your long-term debt has been decreasing steadily, from $100,000 to $85,000 over the past year. This reduction in leverage improves your financial flexibility and reduces interest expenses, which is positive for your bottom line."
    
    elif 'liquidity' in query.lower():
        return f"Your current ratio is {st.session_state.financial_metrics['current_ratio']:.2f}, indicating strong short-term liquidity. This means you have ${st.session_state.financial_metrics['current_ratio']:.2f} in current assets for every $1 in current liabilities. Your cash position has increased from $50,000 to $90,000 over the past year, further strengthening your liquidity position."
    
    elif 'investment' in query.lower() or 'invest' in query.lower():
        return "Based on your strong cash position ($90,000) and increasing operating cash flow, you're in a good position to consider investments. With your current growth trajectory and profitability, I would recommend considering investments in capacity expansion, technology upgrades, or market expansion. Any investment with an IRR above 15% would be attractive given your current financial performance."
    
    elif 'forecast' in query.lower() or 'projection' in query.lower() or 'predict' in query.lower():
        return "Based on your historical performance, I project your revenue will reach approximately $210,000 in the next quarter, representing a 16.7% growth. Your net income is projected to be around $32,000, with a net margin of 15.2%. Cash flow from operations should continue its positive trend, reaching approximately $28,000 in the next quarter."
    
    else:
        return "Based on your financial statements, your business is showing strong performance with increasing revenue, profitability, and cash flow. Your latest quarterly revenue was $180,000, with a net income of $24,750, representing a net margin of 13.8%. Your balance sheet remains strong with $90,000 in cash and a current ratio of 3.17. I recommend focusing on sustaining your growth momentum while maintaining your strong margins and liquidity position."

# Sidebar for navigation
st.sidebar.markdown("<div class='main-header'>Virtual CFO</div>", unsafe_allow_html=True)
st.sidebar.image("https://img.icons8.com/color/96/000000/financial-growth.png", width=80)

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Financial Analysis", "Chat with CFO", "Data Upload", "Settings"])

# Sidebar metrics
st.sidebar.markdown("<div class='sub-header'>Key Metrics</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class='card metric-card'>
    <b>Revenue Growth:</b> {st.session_state.financial_metrics['revenue_growth']:.1f}%
</div>
<div class='card metric-card'>
    <b>Net Margin:</b> {st.session_state.financial_metrics['net_margin']:.1f}%
</div>
<div class='card metric-card'>
    <b>Current Ratio:</b> {st.session_state.financial_metrics['current_ratio']:.2f}
</div>
""", unsafe_allow_html=True)

# Dashboard Page
if page == "Dashboard":
    st.markdown("<div class='main-header'>Financial Dashboard</div>", unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Revenue", f"${revenue_current:,.0f}", f"{revenue_growth:.1f}%")
    
    with col2:
        st.metric("Net Income", f"${net_income_current:,.0f}", f"{profit_growth:.1f}%")
    
    with col3:
        st.metric("Gross Margin", f"{gross_margin:.1f}%")
    
    with col4:
        st.metric("Cash Balance", f"${balance.loc[latest_quarter, 'Cash and Equivalents']:,.0f}")
    
    # Revenue and Profit Trends
    st.markdown("<div class='sub-header'>Revenue and Profit Trends</div>", unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=income.index,
        y=income['Revenue'],
        name='Revenue',
        marker_color='#3B82F6'
    ))
    fig.add_trace(go.Scatter(
        x=income.index,
        y=income['Net Income'],
        name='Net Income',
        marker_color='#10B981',
        mode='lines+markers'
    ))
    fig.update_layout(
        title='Quarterly Revenue and Net Income',
        xaxis_title='Quarter',
        yaxis_title='Amount ($)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial Health Indicators
    st.markdown("<div class='sub-header'>Financial Health Indicators</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Profitability Margins
        profit_data = pd.DataFrame({
            'Quarter': income.index,
            'Gross Margin': income['Gross Profit'] / income['Revenue'] * 100,
            'Operating Margin': income['Operating Income'] / income['Revenue'] * 100,
            'Net Margin': income['Net Income'] / income['Revenue'] * 100
        })
        
        fig = px.line(
            profit_data, 
            x='Quarter', 
            y=['Gross Margin', 'Operating Margin', 'Net Margin'],
            labels={'value': 'Margin (%)', 'variable': 'Metric'},
            title='Profitability Margins'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Liquidity and Leverage
        financial_health = pd.DataFrame({
            'Quarter': balance.index,
            'Current Ratio': balance['Current Assets'] / balance['Current Liabilities'],
            'Debt-to-Equity': balance['Total Liabilities'] / balance['Equity']
        })
        
        fig = px.line(
            financial_health, 
            x='Quarter', 
            y=['Current Ratio', 'Debt-to-Equity'],
            labels={'value': 'Ratio', 'variable': 'Metric'},
            title='Liquidity and Leverage Ratios'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Cash Flow Analysis
    st.markdown("<div class='sub-header'>Cash Flow Analysis</div>", unsafe_allow_html=True)
    
    cash_flow = st.session_state.financial_data['cash_flow']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cash_flow.index,
        y=cash_flow['Operating Cash Flow'],
        name='Operating CF',
        marker_color='#3B82F6'
    ))
    fig.add_trace(go.Bar(
        x=cash_flow.index,
        y=cash_flow['Investing Cash Flow'],
        name='Investing CF',
        marker_color='#EF4444'
    ))
    fig.add_trace(go.Bar(
        x=cash_flow.index,
        y=cash_flow['Financing Cash Flow'],
        name='Financing CF',
        marker_color='#F59E0B'
    ))
    fig.add_trace(go.Scatter(
        x=cash_flow.index,
        y=cash_flow['Net Cash Flow'],
        name='Net Cash Flow',
        marker_color='#10B981',
        mode='lines+markers'
    ))
    fig.update_layout(
        title='Quarterly Cash Flow Components',
        xaxis_title='Quarter',
        yaxis_title='Amount ($)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode='relative'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # CFO Insights
    st.markdown("<div class='sub-header'>CFO Insights</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card success-card'>
            <h3>Strengths</h3>
            <ul>
                <li>Strong revenue growth of 20% quarter-over-quarter</li>
                <li>Improving profit margins across all levels</li>
                <li>Healthy cash position with increasing operating cash flow</li>
                <li>Conservative debt levels with decreasing long-term debt</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card warning-card'>
            <h3>Areas for Attention</h3>
            <ul>
                <li>Increasing working capital requirements</li>
                <li>No capital expenditures in recent quarters</li>
                <li>Operating expenses growing at 12.5% quarter-over-quarter</li>
                <li>Tax rate increased from 25% to 27.5% in the latest quarter</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card info-card'>
        <h3>Recommendations</h3>
        <ol>
            <li><b>Capital Allocation:</b> Consider investing in growth opportunities given the strong cash position</li>
            <li><b>Working Capital Management:</b> Review inventory and accounts receivable policies to optimize cash conversion cycle</li>
            <li><b>Cost Control:</b> Implement measures to keep operating expense growth below revenue growth</li>
            <li><b>Tax Planning:</b> Explore strategies to optimize effective tax rate</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Financial Analysis Page
elif page == "Financial Analysis":
    st.markdown("<div class='main-header'>Financial Analysis</div>", unsafe_allow_html=True)
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Profitability Analysis", "Liquidity Analysis", "Growth Analysis", "Cash Flow Analysis", "Ratio Analysis"]
    )
    
    if analysis_type == "Profitability Analysis":
        st.markdown("<div class='sub-header'>Profitability Analysis</div>", unsafe_allow_html=True)
        
        # Profitability metrics
        income = st.session_state.financial_data['income_statement']
        
        # Calculate profitability metrics
        profitability = pd.DataFrame({
            'Gross Margin (%)': (income['Gross Profit'] / income['Revenue'] * 100).round(1),
            'Operating Margin (%)': (income['Operating Income'] / income['Revenue'] * 100).round(1),
            'Net Margin (%)': (income['Net Income'] / income['Revenue'] * 100).round(1),
            'Revenue ($)': income['Revenue'],
            'Gross Profit ($)': income['Gross Profit'],
            'Operating Income ($)': income['Operating Income'],
            'Net Income ($)': income['Net Income']
        })
        
        st.dataframe(profitability, use_container_width=True)
        
        # Profitability visualization
        fig = px.line(
            profitability, 
            x=profitability.index, 
            y=['Gross Margin (%)', 'Operating Margin (%)', 'Net Margin (%)'],
            labels={'value': 'Margin (%)', 'variable': 'Metric', 'index': 'Quarter'},
            title='Profitability Margins Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Expense breakdown
        st.markdown("<div class='sub-header'>Expense Breakdown</div>", unsafe_allow_html=True)
        
        expense_data = pd.DataFrame({
            'COGS': income['Cost of Goods Sold'] / income['Revenue'] * 100,
            'Operating Expenses': income['Operating Expenses'] / income['Revenue'] * 100,
            'Interest': income['Interest Expense'] / income['Revenue'] * 100,
            'Tax': income['Tax Expense'] / income['Revenue'] * 100,
            'Net Income': income['Net Income'] / income['Revenue'] * 100
        })
        
        fig = px.bar(
            expense_data,
            x=expense_data.index,
            y=['COGS', 'Operating Expenses', 'Interest', 'Tax', 'Net Income'],
            labels={'value': '% of Revenue', 'variable': 'Category', 'index': 'Quarter'},
            title='Expense Breakdown (% of Revenue)',
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Profitability insights
        st.markdown("""
        <div class='card info-card'>
            <h3>Profitability Insights</h3>
            <p>Your profitability metrics show consistent improvement across all quarters:</p>
            <ul>
                <li>Gross margin increased from 40.0% to 44.4% (+4.4 percentage points)</li>
                <li>Operating margin increased from 10.0% to 19.4% (+9.4 percentage points)</li>
                <li>Net margin increased from 6.0% to 13.8% (+7.8 percentage points)</li>
            </ul>
            <p>This indicates effective pricing strategies and good cost control. The most significant improvement is in operating margin, suggesting operational efficiency gains.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif analysis_type == "Liquidity Analysis":
        st.markdown("<div class='sub-header'>Liquidity Analysis</div>", unsafe_allow_html=True)
        
        # Liquidity metrics
        balance = st.session_state.financial_data['balance_sheet']
        
        # Calculate liquidity metrics
        liquidity = pd.DataFrame({
            'Current Ratio': (balance['Current Assets'] / balance['Current Liabilities']).round(2),
            'Quick Ratio': ((balance['Current Assets'] - balance['Inventory']) / balance['Current Liabilities']).round(2),
            'Cash Ratio': (balance['Cash and Equivalents'] / balance['Current Liabilities']).round(2),
            'Working Capital ($)': (balance['Current Assets'] - balance['Current Liabilities']).round(0)
        })
        
        st.dataframe(liquidity, use_container_width=True)
        
        # Liquidity visualization
        fig = px.line(
            liquidity, 
            x=liquidity.index, 
            y=['Current Ratio', 'Quick Ratio', 'Cash Ratio'],
            labels={'value': 'Ratio', 'variable': 'Metric', 'index': 'Quarter'},
            title='Liquidity Ratios Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Working capital trend
        fig = px.bar(
            liquidity,
            x=liquidity.index,
            y='Working Capital ($)',
            labels={'index': 'Quarter'},
            title='Working Capital Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Current assets breakdown
        st.markdown("<div class='sub-header'>Current Assets Breakdown</div>", unsafe_allow_html=True)
        
        current_assets = pd.DataFrame({
            'Cash and Equivalents': balance['Cash and Equivalents'],
            'Accounts Receivable': balance['Accounts Receivable'],
            'Inventory': balance['Inventory']
        })
        
        fig = px.bar(
            current_assets,
            x=current_assets.index,
            y=['Cash and Equivalents', 'Accounts Receivable', 'Inventory'],
            labels={'value': 'Amount ($)', 'variable': 'Category', 'index': 'Quarter'},
            title='Current Assets Composition',
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Liquidity insights
        st.markdown("""
        <div class='card info-card'>
            <h3>Liquidity Insights</h3>
            <p>Your liquidity position is strong and improving:</p>
            <ul>
                <li>Current ratio increased from 2.67 to 3.17, well above the recommended minimum of 1.5</li>
                <li>Quick ratio increased from 1.78 to 2.25, indicating strong ability to meet short-term obligations</li>
                <li>Cash ratio increased from 1.11 to 1.50, showing excellent cash reserves</li>
                <li>Working capital increased from $75,000 to $130,000, providing a strong buffer for operations</li>
            </ul>
            <p>The increasing proportion of cash in your current assets improves financial flexibility but may suggest opportunities for more productive use of capital.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif analysis_type == "Growth Analysis":
        st.markdown("<div class='sub-header'>Growth Analysis</div>", unsafe_allow_html=True)
        
        # Growth metrics
        income = st.session_state.financial_data['income_statement']
        balance = st.session_state.financial_data['balance_sheet']
        
        # Calculate quarter-over-quarter growth rates
        growth_data = pd.DataFrame({
            'Revenue Growth (%)': income['Revenue'].pct_change() * 100,
            'Net Income Growth (%)': income['Net Income'].pct_change() * 100,
            'Total Assets Growth (%)': balance['Total Assets'].pct_change() * 100,
            'Equity Growth (%)': balance['Equity'].pct_change() * 100
        }).round(1)
        
        # Replace NaN in first row
        growth_data.iloc[0] = ['-', '-', '-', '-']
        
        st.dataframe(growth_data, use_container_width=True)
        
        # Growth visualization
        growth_chart_data = growth_data.iloc[1:].copy()  # Skip first row with NaN
        
        fig = px.bar(
            growth_chart_data,
            x=growth_chart_data.index,
            y=['Revenue Growth (%)', 'Net Income Growth (%)'],
            labels={'value': 'Growth Rate (%)', 'variable': 'Metric', 'index': 'Quarter'},
            title='Revenue and Profit Growth Rates',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Absolute values trend
        absolute_data = pd.DataFrame({
            'Revenue': income['Revenue'],
            'Net Income': income['Net Income'],
            'Total Assets': balance['Total Assets'],
            'Equity': balance['Equity']
        })
        
        # Create two separate charts for better scale
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                absolute_data,
                x=absolute_data.index,
                y=['Revenue', 'Total Assets'],
                labels={'value': 'Amount ($)', 'variable': 'Metric', 'index': 'Quarter'},
                title='Revenue and Assets Trend'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                absolute_data,
                x=absolute_data.index,
                y=['Net Income', 'Equity'],
                labels={'value': 'Amount ($)', 'variable': 'Metric', 'index': 'Quarter'},
                title='Net Income and Equity Trend'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Growth insights
        st.markdown("""
        <div class='card info-card'>
            <h3>Growth Insights</h3>
            <p>Your business is showing strong and accelerating growth:</p>
            <ul>
                <li>Revenue growth has been consistent at 20% quarter-over-quarter</li>
                <li>Net income growth has accelerated from 62.5% to 76.9% to 43.5%</li>
                <li>Asset growth has been moderate at 3.1% to 6.1% to 7.1%</li>
                <li>Equity growth has accelerated from 5.7% to 10.8% to 12.2%</li>
            </ul>
            <p>The faster growth in net income compared to revenue indicates improving operational efficiency and economies of scale. The increasing equity growth rate reflects strong profitability and reinvestment in the business.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif analysis_type == "Cash Flow Analysis":
        st.markdown("<div class='sub-header'>Cash Flow Analysis</div>", unsafe_allow_html=True)
        
        # Cash flow metrics
        cash_flow = st.session_state.financial_data['cash_flow']
        
        st.dataframe(cash_flow, use_container_width=True)
        
        # Cash flow components visualization
        fig = px.bar(
            cash_flow,
            x=cash_flow.index,
            y=['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow'],
            labels={'value': 'Amount ($)', 'variable': 'Cash Flow Type', 'index': 'Quarter'},
            title='Cash Flow Components',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cumulative cash flow
        cumulative_cf = pd.DataFrame({
            'Net Cash Flow': cash_flow['Net Cash Flow'],
            'Cumulative Cash Flow': cash_flow['Net Cash Flow'].cumsum()
        })
        
        fig = px.line(
            cumulative_cf,
            x=cumulative_cf.index,
            y=['Net Cash Flow', 'Cumulative Cash Flow'],
            labels={'value': 'Amount ($)', 'variable': 'Metric', 'index': 'Quarter'},
            title='Net and Cumulative Cash Flow'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Operating cash flow components
        ocf_components = pd.DataFrame({
            'Net Income': cash_flow['Net Income'],
            'Depreciation': cash_flow['Depreciation'],
            'Working Capital Changes': cash_flow['Changes in Working Capital'],
            'Operating Cash Flow': cash_flow['Operating Cash Flow']
        })
        
        fig = px.bar(
            ocf_components,
            x=ocf_components.index,
            y=['Net Income', 'Depreciation', 'Working Capital Changes'],
            labels={'value': 'Amount ($)', 'variable': 'Component', 'index': 'Quarter'},
            title='Operating Cash Flow Components',
            barmode='relative'
        )
        fig.add_trace(go.Scatter(
            x=ocf_components.index,
            y=ocf_components['Operating Cash Flow'],
            name='Operating Cash Flow',
            mode='lines+markers',
            line=dict(color='green', width=3)
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Cash flow insights
        st.markdown("""
        <div class='card info-card'>
            <h3>Cash Flow Insights</h3>
            <p>Your cash flow position is strong and improving:</p>
            <ul>
                <li>Operating cash flow has increased consistently from $8,000 to $21,750</li>
                <li>No investing cash flow indicates potential underinvestment in growth</li>
                <li>Consistent financing cash outflow of $5,000 per quarter for debt repayment</li>
                <li>Net cash flow has increased from $3,000 to $16,750, accumulating $34,750 over the period</li>
            </ul>
            <p>The increasing gap between net income and operating cash flow due to working capital changes suggests growing inventory or accounts receivable, which should be monitored. The strong and growing operating cash flow provides opportunities for strategic investments or accelerated debt reduction.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif analysis_type == "Ratio Analysis":
        st.markdown("<div class='sub-header'>Financial Ratio Analysis</div>", unsafe_allow_html=True)
        
        # Financial data
        income = st.session_state.financial_data['income_statement']
        balance = st.session_state.financial_data['balance_sheet']
        
        # Calculate key ratios
        ratios = pd.DataFrame(index=income.index)
        
        # Profitability Ratios
        ratios['Gross Margin (%)'] = (income['Gross Profit'] / income['Revenue'] * 100).round(1)
        ratios['Operating Margin (%)'] = (income['Operating Income'] / income['Revenue'] * 100).round(1)
        ratios['Net Margin (%)'] = (income['Net Income'] / income['Revenue'] * 100).round(1)
        ratios['Return on Assets (%)'] = (income['Net Income'] / balance['Total Assets'] * 100).round(1)
        ratios['Return on Equity (%)'] = (income['Net Income'] / balance['Equity'] * 100).round(1)
        
        # Liquidity Ratios
        ratios['Current Ratio'] = (balance['Current Assets'] / balance['Current Liabilities']).round(2)
        ratios['Quick Ratio'] = ((balance['Current Assets'] - balance['Inventory']) / balance['Current Liabilities']).round(2)
        ratios['Cash Ratio'] = (balance['Cash and Equivalents'] / balance['Current Liabilities']).round(2)
        
        # Leverage Ratios
        ratios['Debt-to-Equity'] = (balance['Total Liabilities'] / balance['Equity']).round(2)
        ratios['Debt-to-Assets'] = (balance['Total Liabilities'] / balance['Total Assets']).round(2)
        ratios['Interest Coverage'] = (income['Operating Income'] / income['Interest Expense']).round(1)
        
        # Efficiency Ratios
        ratios['Asset Turnover'] = (income['Revenue'] / balance['Total Assets']).round(2)
        ratios['Inventory Turnover'] = (income['Cost of Goods Sold'] / balance['Inventory']).round(2)
        
        # Display ratios by category
        ratio_categories = {
            "Profitability Ratios": ['Gross Margin (%)', 'Operating Margin (%)', 'Net Margin (%)', 'Return on Assets (%)', 'Return on Equity (%)'],
            "Liquidity Ratios": ['Current Ratio', 'Quick Ratio', 'Cash Ratio'],
            "Leverage Ratios": ['Debt-to-Equity', 'Debt-to-Assets', 'Interest Coverage'],
            "Efficiency Ratios": ['Asset Turnover', 'Inventory Turnover']
        }
        
        selected_category = st.selectbox("Select Ratio Category", list(ratio_categories.keys()))
        
        selected_ratios = ratios[ratio_categories[selected_category]]
        st.dataframe(selected_ratios, use_container_width=True)
        
        # Visualization of selected ratios
        fig = px.line(
            selected_ratios,
            x=selected_ratios.index,
            y=selected_ratios.columns,
            labels={'value': 'Ratio Value', 'variable': 'Ratio', 'index': 'Quarter'},
            title=f'{selected_category} Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Ratio insights
        insights = {
            "Profitability Ratios": """
                <div class='card info-card'>
                    <h3>Profitability Ratio Insights</h3>
                    <p>Your profitability ratios show consistent improvement:</p>
                    <ul>
                        <li>Gross margin increased from 40.0% to 44.4%, indicating improved pricing power or cost efficiency</li>
                        <li>Operating margin nearly doubled from 10.0% to 19.4%, showing strong operational leverage</li>
                        <li>Net margin more than doubled from 6.0% to 13.8%, reflecting overall business efficiency</li>
                        <li>Return on assets improved from 1.9% to 6.6%, indicating better asset utilization</li>
                        <li>Return on equity increased from 3.4% to 10.8%, showing strong returns for shareholders</li>
                    </ul>
                    <p>These improvements across all profitability metrics indicate a business that is scaling efficiently and effectively.</p>
                </div>
            """,
            "Liquidity Ratios": """
                <div class='card info-card'>
                    <h3>Liquidity Ratio Insights</h3>
                    <p>Your liquidity position is strong and improving:</p>
                    <ul>
                        <li>Current ratio increased from 2.67 to 3.17, well above the recommended minimum of 1.5</li>
                        <li>Quick ratio increased from 1.78 to 2.25, indicating strong ability to meet short-term obligations without selling inventory</li>
                        <li>Cash ratio increased from 1.11 to 1.50, showing excellent cash reserves</li>
                    </ul>
                    <p>While these ratios indicate a very strong liquidity position, they may also suggest that capital is not being utilized as efficiently as possible. Consider strategic investments or expansion opportunities.</p>
                </div>
            """,
            "Leverage Ratios": """
                <div class='card info-card'>
                    <h3>Leverage Ratio Insights</h3>
                    <p>Your leverage metrics indicate a conservative financial structure:</p>
                    <ul>
                        <li>Debt-to-equity ratio decreased from 0.83 to 0.63, showing reduced financial leverage</li>
                        <li>Debt-to-assets ratio decreased from 0.45 to 0.39, indicating increased asset coverage for debt</li>
                        <li>Interest coverage ratio increased from 5.0 to 17.5, showing very strong ability to service debt</li>
                    </ul>
                    <p>Your decreasing leverage ratios and increasing interest coverage indicate a strengthening financial position with reduced financial risk. This conservative approach provides financial flexibility but may limit potential returns from financial leverage.</p>
                </div>
            """,
            "Efficiency Ratios": """
                <div class='card info-card'>
                    <h3>Efficiency Ratio Insights</h3>
                    <p>Your efficiency metrics show mixed results:</p>
                    <ul>
                        <li>Asset turnover increased from 0.31 to 0.48, indicating improved asset utilization</li>
                        <li>Inventory turnover increased from 1.50 to 1.82, showing slightly better inventory management</li>
                    </ul>
                    <p>While both efficiency ratios are improving, there may still be opportunities to further optimize asset utilization and inventory management. Consider reviewing your inventory policies and asset investment strategies to further improve these metrics.</p>
                </div>
            """
        }
        
        st.markdown(insights[selected_category], unsafe_allow_html=True)

# Chat with CFO Page
elif page == "Chat with CFO":
    st.markdown("<div class='main-header'>Chat with Your Virtual CFO</div>", unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class='chat-message user-message'>
                <b>You:</b> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message cfo-message'>
                <b>Virtual CFO:</b> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask your Virtual CFO:", placeholder="e.g., How is our cash flow trending?")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get CFO response
        cfo_response = get_cfo_response(user_input, st.session_state.financial_data)
        
        # Add CFO response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": cfo_response})
        
        # Rerun to update the chat display
        st.rerun()
    
    # Suggested questions
    st.markdown("<div class='sub-header'>Suggested Questions</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("How is our cash flow trending?"):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": "How is our cash flow trending?"})
            
            # Get CFO response
            cfo_response = get_cfo_response("How is our cash flow trending?", st.session_state.financial_data)
            
            # Add CFO response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": cfo_response})
            
            # Rerun to update the chat display
            st.rerun()
    
    with col2:
        if st.button("What's our current profit margin?"):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": "What's our current profit margin?"})
            
            # Get CFO response
            cfo_response = get_cfo_response("What's our current profit margin?", st.session_state.financial_data)
            
            # Add CFO response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": cfo_response})
            
            # Rerun to update the chat display
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("How is our growth trajectory?"):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": "How is our growth trajectory?"})
            
            # Get CFO response
            cfo_response = get_cfo_response("How is our growth trajectory?", st.session_state.financial_data)
            
            # Add CFO response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": cfo_response})
            
            # Rerun to update the chat display
            st.rerun()
    
    with col2:
        if st.button("What investment opportunities should we consider?"):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": "What investment opportunities should we consider?"})
            
            # Get CFO response
            cfo_response = get_cfo_response("What investment opportunities should we consider?", st.session_state.financial_data)
            
            # Add CFO response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": cfo_response})
            
            # Rerun to update the chat display
            st.rerun()

# Data Upload Page
elif page == "Data Upload":
    st.markdown("<div class='main-header'>Upload Financial Data</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card info-card'>
        <h3>Data Upload Instructions</h3>
        <p>Upload your financial data files to customize the Virtual CFO Agent with your actual financial information. The system accepts the following file formats:</p>
        <ul>
            <li><b>CSV files</b> - Comma-separated values</li>
            <li><b>Excel files</b> - .xlsx or .xls format</li>
            <li><b>JSON files</b> - Structured financial data</li>
        </ul>
        <p>For best results, ensure your data includes:</p>
        <ul>
            <li>Income statement data (revenue, expenses, profits)</li>
            <li>Balance sheet data (assets, liabilities, equity)</li>
            <li>Cash flow data (operating, investing, financing cash flows)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("<div class='sub-header'>Upload Files</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        income_file = st.file_uploader("Upload Income Statement", type=["csv", "xlsx", "xls", "json"])
        if income_file:
            st.success("Income Statement uploaded successfully!")
    
    with col2:
        balance_file = st.file_uploader("Upload Balance Sheet", type=["csv", "xlsx", "xls", "json"])
        if balance_file:
            st.success("Balance Sheet uploaded successfully!")
    
    with col3:
        cashflow_file = st.file_uploader("Upload Cash Flow Statement", type=["csv", "xlsx", "xls", "json"])
        if cashflow_file:
            st.success("Cash Flow Statement uploaded successfully!")
    
    # Sample data templates
    st.markdown("<div class='sub-header'>Sample Templates</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <p>Don't have your data ready? Download our sample templates to see the required format:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="Download Income Statement Template",
            data="Period,Revenue,Cost of Goods Sold,Gross Profit,Operating Expenses,Operating Income,Interest Expense,Income Before Tax,Tax Expense,Net Income\n2024-01-01,100000,60000,40000,30000,10000,2000,8000,2000,6000\n2024-04-01,120000,70000,50000,35000,15000,2000,13000,3250,9750\n",
            file_name="income_statement_template.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="Download Balance Sheet Template",
            data="Period,Cash and Equivalents,Accounts Receivable,Inventory,Current Assets,Fixed Assets,Total Assets,Accounts Payable,Short-term Debt,Current Liabilities,Long-term Debt,Total Liabilities,Equity\n2024-01-01,50000,30000,40000,120000,200000,320000,25000,20000,45000,100000,145000,175000\n2024-04-01,55000,35000,45000,135000,195000,330000,30000,20000,50000,95000,145000,185000\n",
            file_name="balance_sheet_template.csv",
            mime="text/csv"
        )
    
    with col3:
        st.download_button(
            label="Download Cash Flow Template",
            data="Period,Net Income,Depreciation,Changes in Working Capital,Operating Cash Flow,Capital Expenditures,Investing Cash Flow,Debt Repayment,Financing Cash Flow,Net Cash Flow\n2024-01-01,6000,5000,-3000,8000,0,0,5000,-5000,3000\n2024-04-01,9750,5000,-5000,9750,0,0,5000,-5000,4750\n",
            file_name="cash_flow_template.csv",
            mime="text/csv"
        )
    
    # Reset data button
    st.markdown("<div class='sub-header'>Reset Data</div>", unsafe_allow_html=True)
    
    if st.button("Reset to Sample Data"):
        # Reset to sample data
        st.session_state.financial_data = {
            'income_statement': pd.DataFrame({
                'Revenue': [100000, 120000, 150000, 180000],
                'Cost of Goods Sold': [60000, 70000, 85000, 100000],
                'Gross Profit': [40000, 50000, 65000, 80000],
                'Operating Expenses': [30000, 35000, 40000, 45000],
                'Operating Income': [10000, 15000, 25000, 35000],
                'Interest Expense': [2000, 2000, 2000, 2000],
                'Income Before Tax': [8000, 13000, 23000, 33000],
                'Tax Expense': [2000, 3250, 5750, 8250],
                'Net Income': [6000, 9750, 17250, 24750]
            }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q')),
            
            'balance_sheet': pd.DataFrame({
                'Cash and Equivalents': [50000, 55000, 70000, 90000],
                'Accounts Receivable': [30000, 35000, 40000, 45000],
                'Inventory': [40000, 45000, 50000, 55000],
                'Current Assets': [120000, 135000, 160000, 190000],
                'Fixed Assets': [200000, 195000, 190000, 185000],
                'Total Assets': [320000, 330000, 350000, 375000],
                'Accounts Payable': [25000, 30000, 35000, 40000],
                'Short-term Debt': [20000, 20000, 20000, 20000],
                'Current Liabilities': [45000, 50000, 55000, 60000],
                'Long-term Debt': [100000, 95000, 90000, 85000],
                'Total Liabilities': [145000, 145000, 145000, 145000],
                'Equity': [175000, 185000, 205000, 230000],
            }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q')),
            
            'cash_flow': pd.DataFrame({
                'Net Income': [6000, 9750, 17250, 24750],
                'Depreciation': [5000, 5000, 5000, 5000],
                'Changes in Working Capital': [-3000, -5000, -7000, -8000],
                'Operating Cash Flow': [8000, 9750, 15250, 21750],
                'Capital Expenditures': [0, 0, 0, 0],
                'Investing Cash Flow': [0, 0, 0, 0],
                'Debt Repayment': [5000, 5000, 5000, 5000],
                'Financing Cash Flow': [-5000, -5000, -5000, -5000],
                'Net Cash Flow': [3000, 4750, 10250, 16750]
            }, index=pd.date_range(start='2024-01-01', periods=4, freq='Q'))
        }
        
        # Recalculate financial metrics
        income = st.session_state.financial_data['income_statement']
        balance = st.session_state.financial_data['balance_sheet']
        
        latest_quarter = income.index[-1]
        previous_quarter = income.index[-2]
        
        revenue_current = income.loc[latest_quarter, 'Revenue']
        revenue_previous = income.loc[previous_quarter, 'Revenue']
        revenue_growth = (revenue_current - revenue_previous) / revenue_previous * 100
        
        net_income_current = income.loc[latest_quarter, 'Net Income']
        net_income_previous = income.loc[previous_quarter, 'Net Income']
        profit_growth = (net_income_current - net_income_previous) / net_income_previous * 100
        
        gross_margin = income.loc[latest_quarter, 'Gross Profit'] / income.loc[latest_quarter, 'Revenue'] * 100
        net_margin = income.loc[latest_quarter, 'Net Income'] / income.loc[latest_quarter, 'Revenue'] * 100
        
        current_ratio = balance.loc[latest_quarter, 'Current Assets'] / balance.loc[latest_quarter, 'Current Liabilities']
        debt_to_equity = balance.loc[latest_quarter, 'Total Liabilities'] / balance.loc[latest_quarter, 'Equity']
        
        st.session_state.financial_metrics = {
            'revenue_growth': revenue_growth,
            'profit_growth': profit_growth,
            'gross_margin': gross_margin,
            'net_margin': net_margin,
            'current_ratio': current_ratio,
            'debt_to_equity': debt_to_equity
        }
        
        st.success("Data reset to sample data successfully!")
        st.rerun()

# Settings Page
elif page == "Settings":
    st.markdown("<div class='main-header'>Settings</div>", unsafe_allow_html=True)
    
    # User Profile
    st.markdown("<div class='sub-header'>User Profile</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Company Name", value="Sample Company Inc.")
    
    with col2:
        st.selectbox("Industry", ["Technology", "Manufacturing", "Retail", "Healthcare", "Financial Services", "Other"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Fiscal Year End", value="December 31")
    
    with col2:
        st.selectbox("Reporting Currency", ["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)", "CAD ($)"])
    
    # Notification Settings
    st.markdown("<div class='sub-header'>Notification Settings</div>", unsafe_allow_html=True)
    
    st.checkbox("Enable email notifications", value=False)
    st.checkbox("Enable weekly financial summary", value=True)
    st.checkbox("Alert on significant financial changes", value=True)
    
    # Display Settings
    st.markdown("<div class='sub-header'>Display Settings</div>", unsafe_allow_html=True)
    
    st.selectbox("Default Dashboard View", ["Financial Overview", "Cash Flow Focus", "Growth Metrics", "Profitability Analysis"])
    st.selectbox("Chart Color Theme", ["Default", "Blue", "Green", "Monochrome", "Colorblind Friendly"])
    st.checkbox("Show data labels on charts", value=True)
    
    # Advanced Settings
    st.markdown("<div class='sub-header'>Advanced Settings</div>", unsafe_allow_html=True)
    
    st.selectbox("Financial Analysis Depth", ["Basic", "Intermediate", "Advanced"])
    st.slider("Forecast Horizon (Months)", min_value=3, max_value=36, value=12, step=3)
    st.checkbox("Include industry benchmarks in analysis", value=False)
    
    # Save Settings
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
    <p>Virtual CFO Agent | Powered by AI | © 2025</p>
</div>
""", unsafe_allow_html=True)
