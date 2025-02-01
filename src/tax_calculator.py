from tax_slabs.tax_slab_2024 import TaxSlab2024
from tax_slabs.tax_slab_2025 import TaxSlab2025

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

def main():
    print("Tax Calculator")
    print("1. Calculate tax for FY 2024-25")
    print("2. Calculate tax for FY2025-26")
    
    choice = int(input("Enter your choice (1/2): "))
    income = float(input("Enter your taxable income: ₹"))
    
    regime_year = 2024 if choice == 1 else 2025
    calculator = TaxCalculator(regime_year)
    result = calculator.calculate_tax(income)
    
    print("\nTax Calculation Details:")
    print(f"Taxable Income: ₹{result['taxable_income']:,.2f}")
    print("\nTax Calculation Breakup:")
    for breakup in result['tax_breakup']:
        print(breakup)
    
    if result['rebate'] > 0:
        print(f"\nTax Rebate: ₹{result['rebate']:,.2f}")
    
    print(f"\nFinal Tax Payable: ₹{result['final_tax']:,.2f}")
    print(f"Annual In-Hand Salary: ₹{result['annual_in_hand']:,.2f}")
    print(f"Monthly In-Hand Salary: ₹{result['monthly_in_hand']:,.2f}")

if __name__ == "__main__":
    main() 