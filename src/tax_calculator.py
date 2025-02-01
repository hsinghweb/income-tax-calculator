from tax_slabs.tax_slab_2024 import TaxSlab2024
from tax_slabs.tax_slab_2025 import TaxSlab2025
from utils.helpers import format_currency

class TaxCalculator:
    def __init__(self, regime_year):
        self.tax_slab = TaxSlab2024() if regime_year == 2024 else TaxSlab2025()

    def calculate_tax(self, income):
        tax = 0
        remaining_income = income
        tax_breakup = []

        for lower_limit, upper_limit, rate in self.tax_slab.slabs:
            if remaining_income > lower_limit:
                taxable_amount = min(remaining_income - lower_limit, upper_limit - lower_limit)
                tax_for_slab = taxable_amount * rate
                tax += tax_for_slab
                
                if rate > 0:
                    tax_breakup.append(
                        f"Income from {lower_limit:,} to {min(remaining_income, upper_limit):,} @ {rate*100}% = ₹{tax_for_slab:,.2f}"
                    )

        # Apply tax rebate if applicable
        rebate = 0
        if income <= self.tax_slab.rebate_limit:
            rebate = min(tax, self.tax_slab.max_rebate)

        final_tax = max(0, tax - rebate)
        
        return {
            'taxable_income': income,
            'tax_breakup': tax_breakup,
            'total_tax': tax,
            'rebate': rebate,
            'final_tax': final_tax,
            'annual_in_hand': income - final_tax,
            'monthly_in_hand': (income - final_tax) / 12
        }

def print_tax_comparison(income):
    calculator_2024 = TaxCalculator(2024)
    calculator_2025 = TaxCalculator(2025)
    
    result_2024 = calculator_2024.calculate_tax(income)
    result_2025 = calculator_2025.calculate_tax(income)
    
    print("\n" + "="*80)
    print(f"Tax Comparison for Income: {format_currency(income)}")
    print("="*80)
    
    # Print table header
    print(f"{'Details':<30} | {'FY 2024-25':<20} | {'FY 2025-26':<20}")
    print("-"*80)
    
    # Print table rows
    rows = [
        ("Taxable Income", result_2024['taxable_income'], result_2025['taxable_income']),
        ("Total Tax", result_2024['total_tax'], result_2025['total_tax']),
        ("Tax Rebate", result_2024['rebate'], result_2025['rebate']),
        ("Final Tax Payable", result_2024['final_tax'], result_2025['final_tax']),
        ("Annual In-Hand Salary", result_2024['annual_in_hand'], result_2025['annual_in_hand']),
        ("Monthly In-Hand Salary", result_2024['monthly_in_hand'], result_2025['monthly_in_hand'])
    ]
    
    for label, val_2024, val_2025 in rows:
        print(f"{label:<30} | {format_currency(val_2024):<20} | {format_currency(val_2025):<20}")
    
    print("\nDetailed Tax Calculation for FY 2024-25:")
    for breakup in result_2024['tax_breakup']:
        print(breakup)
        
    print("\nDetailed Tax Calculation for FY 2025-26:")
    for breakup in result_2025['tax_breakup']:
        print(breakup)

def main():
    print("Income Tax Calculator - New Tax Regime")
    income = float(input("Enter your taxable income: ₹"))
    print_tax_comparison(income)

if __name__ == "__main__":
    main() 