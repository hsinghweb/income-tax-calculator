class TaxSlab2024:
    def __init__(self):
        self.slabs = [
            (0, 300000, 0),
            (300000, 700000, 0.05),
            (700000, 1000000, 0.10),
            (1000000, 1200000, 0.15),
            (1200000, 1500000, 0.20),
            (1500000, float('inf'), 0.30)
        ]
        self.rebate_limit = 700000
        self.max_rebate = 25000 