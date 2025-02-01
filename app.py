import streamlit as st
from src.tax_calculator import TaxCalculator
from src.tax_slabs.tax_slab_2024 import TaxSlab2024
from src.tax_slabs.tax_slab_2025 import TaxSlab2025
from src.utils.helpers import format_currency
import pandas as pd

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        /* Main title styling */
        .main-title {
            color: #1E88E5;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            padding: 1rem;
            background: linear-gradient(to right, #E3F2FD, #FFFFFF);
            border-radius: 10px;
        }
        
        /* Subtitle styling */
        .subtitle {
            color: #424242;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        /* Section headers */
        .section-header {
            color: #1565C0;
            font-size: 1.5rem;
            padding: 0.5rem 0;
            border-bottom: 2px solid #1565C0;
            margin: 1.5rem 0;
        }
        
        /* Table styling */
        .stDataFrame {
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Calculator box */
        .calculator-box {
            background-color: #F5F5F5;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        /* Results section */
        .results-box {
            background: linear-gradient(to right, #E8F5E9, #FFFFFF);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        /* Tax breakdown text */
        .tax-breakdown {
            color: #424242;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        /* Highlight important numbers */
        .highlight-number {
            color: #1E88E5;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

def display_tax_slabs():
    st.markdown('<h2 class="section-header">Tax Slab Details - New Tax Regime</h2>', unsafe_allow_html=True)
    
    # Create DataFrame for FY 2024-25
    slab_2024 = TaxSlab2024()
    data_2024 = []
    for lower, upper, rate in slab_2024.slabs:
        data_2024.append({
            'Income Range': f"₹{lower:,} to {'∞' if upper == float('inf') else f'₹{upper:,}'}",
            'Tax Rate': f"{rate*100}%"
        })
    data_2024.append({
        'Income Range': 'Tax Rebate',
        'Tax Rate': '₹25,000 (If income ≤ ₹7,00,000)'
    })
    
    # Create DataFrame for FY 2025-26
    slab_2025 = TaxSlab2025()
    data_2025 = []
    for lower, upper, rate in slab_2025.slabs:
        data_2025.append({
            'Income Range': f"₹{lower:,} to {'∞' if upper == float('inf') else f'₹{upper:,}'}",
            'Tax Rate': f"{rate*100}%"
        })
    data_2025.append({
        'Income Range': 'Tax Rebate',
        'Tax Rate': '₹60,000 (If income ≤ ₹12,00,000)'
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #1565C0;">FY 2024-25</h3>', unsafe_allow_html=True)
        st.table(pd.DataFrame(data_2024))
        
    with col2:
        st.markdown('<h3 style="color: #1565C0;">FY 2025-26</h3>', unsafe_allow_html=True)
        st.table(pd.DataFrame(data_2025))

def calculate_and_display_tax(income):
    calculator_2024 = TaxCalculator(2024)
    calculator_2025 = TaxCalculator(2025)
    
    result_2024 = calculator_2024.calculate_tax(income)
    result_2025 = calculator_2025.calculate_tax(income)
    
    # Display Summary Comparison
    st.markdown('<div class="results-box">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Tax Comparison Summary</h2>', unsafe_allow_html=True)
    
    comparison_data = {
        'Details': [
            'Taxable Income',
            'Total Tax',
            'Tax Rebate',
            'Final Tax Payable',
            'Annual In-Hand Salary',
            'Monthly In-Hand Salary'
        ],
        'FY 2024-25': [
            format_currency(result_2024['taxable_income']),
            format_currency(result_2024['total_tax']),
            format_currency(result_2024['rebate']),
            format_currency(result_2024['final_tax']),
            format_currency(result_2024['annual_in_hand']),
            format_currency(result_2024['monthly_in_hand'])
        ],
        'FY 2025-26': [
            format_currency(result_2025['taxable_income']),
            format_currency(result_2025['total_tax']),
            format_currency(result_2025['rebate']),
            format_currency(result_2025['final_tax']),
            format_currency(result_2025['annual_in_hand']),
            format_currency(result_2025['monthly_in_hand'])
        ]
    }
    
    st.table(pd.DataFrame(comparison_data))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Detailed Calculations
    st.markdown('<h2 class="section-header">Detailed Tax Calculation</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background-color: #F5F5F5; padding: 1rem; border-radius: 10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1565C0;">FY 2024-25:</h3>', unsafe_allow_html=True)
        for breakup in result_2024['tax_breakup']:
            st.markdown(f'<p class="tax-breakdown">{breakup}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="tax-breakdown"><b>Total Tax before rebate:</b> <span class="highlight-number">₹{result_2024["total_tax"]:,.2f}</span></p>', unsafe_allow_html=True)
        if result_2024['rebate'] > 0:
            st.markdown(f'<p class="tax-breakdown"><b>Tax Rebate Applied:</b> <span class="highlight-number">₹{result_2024["rebate"]:,.2f}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="tax-breakdown"><b>Final Tax Payable:</b> <span class="highlight-number">₹{result_2024["final_tax"]:,.2f}</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="background-color: #F5F5F5; padding: 1rem; border-radius: 10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1565C0;">FY 2025-26:</h3>', unsafe_allow_html=True)
        for breakup in result_2025['tax_breakup']:
            st.markdown(f'<p class="tax-breakdown">{breakup}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="tax-breakdown"><b>Total Tax before rebate:</b> <span class="highlight-number">₹{result_2025["total_tax"]:,.2f}</span></p>', unsafe_allow_html=True)
        if result_2025['rebate'] > 0:
            st.markdown(f'<p class="tax-breakdown"><b>Tax Rebate Applied:</b> <span class="highlight-number">₹{result_2025["rebate"]:,.2f}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="tax-breakdown"><b>Final Tax Payable:</b> <span class="highlight-number">₹{result_2025["final_tax"]:,.2f}</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Income Tax Calculator - New Tax Regime",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_css()
    
    st.markdown('<h1 class="main-title">Income Tax Calculator - New Tax Regime</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Compare your tax liability under FY 2024-25 and FY 2025-26 tax slabs</p>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Calculate Your Tax</h2>', unsafe_allow_html=True)
    income = st.number_input(
        "Enter your taxable income (₹)",
        min_value=0.0,
        max_value=100000000.0,
        value=500000.0,
        step=10000.0,
        format="%f"
    )
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Calculate Tax", use_container_width=True):
            calculate_and_display_tax(income)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a separator
    st.markdown("---")
    
    # Display Tax Slabs at the bottom
    st.markdown('<h2 class="section-header">Reference: Tax Slab Details</h2>', unsafe_allow_html=True)
    display_tax_slabs()

if __name__ == "__main__":
    main() 