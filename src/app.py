import streamlit as st
from tax_calculator import TaxCalculator, print_tax_slabs
from tax_slabs.tax_slab_2024 import TaxSlab2024
from tax_slabs.tax_slab_2025 import TaxSlab2025
import pandas as pd

def format_currency(amount):
    return f"₹{amount:,.2f}"

def display_tax_slabs():
    st.header("Tax Slab Details - New Tax Regime")
    
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
        st.subheader("FY 2024-25")
        st.table(pd.DataFrame(data_2024))
        
    with col2:
        st.subheader("FY 2025-26")
        st.table(pd.DataFrame(data_2025))

def calculate_and_display_tax(income):
    calculator_2024 = TaxCalculator(2024)
    calculator_2025 = TaxCalculator(2025)
    
    result_2024 = calculator_2024.calculate_tax(income)
    result_2025 = calculator_2025.calculate_tax(income)
    
    # Display Summary Comparison
    st.subheader("Tax Comparison Summary")
    
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
    
    # Display Detailed Calculations
    st.subheader("Detailed Tax Calculation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("FY 2024-25:")
        for breakup in result_2024['tax_breakup']:
            st.write(breakup)
        st.write(f"**Total Tax before rebate:** ₹{result_2024['total_tax']:,.2f}")
        if result_2024['rebate'] > 0:
            st.write(f"**Tax Rebate Applied:** ₹{result_2024['rebate']:,.2f}")
        st.write(f"**Final Tax Payable:** ₹{result_2024['final_tax']:,.2f}")
    
    with col2:
        st.write("FY 2025-26:")
        for breakup in result_2025['tax_breakup']:
            st.write(breakup)
        st.write(f"**Total Tax before rebate:** ₹{result_2025['total_tax']:,.2f}")
        if result_2025['rebate'] > 0:
            st.write(f"**Tax Rebate Applied:** ₹{result_2025['rebate']:,.2f}")
        st.write(f"**Final Tax Payable:** ₹{result_2025['final_tax']:,.2f}")

def main():
    st.set_page_config(
        page_title="Income Tax Calculator - New Tax Regime",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("Income Tax Calculator - New Tax Regime")
    st.write("Compare your tax liability under FY 2024-25 and FY 2025-26 tax slabs")
    
    # Display Tax Slabs
    display_tax_slabs()
    
    # Input Section
    st.header("Calculate Your Tax")
    income = st.number_input(
        "Enter your taxable income (₹)",
        min_value=0.0,
        max_value=100000000.0,
        value=500000.0,
        step=10000.0,
        format="%f"
    )
    
    if st.button("Calculate Tax"):
        calculate_and_display_tax(income)

if __name__ == "__main__":
    main() 