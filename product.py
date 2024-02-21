from datetime import date, timedelta

class Product:
    def __init__(self, name, dates=[date.today()], price=0, c_volume=0):
        self.name = name
        self.dates = dates
        self.compute_avg_duration()
        self.ending = (self.dates[-1] + timedelta(days=self.avg_duration))
        self.price = price
        self.price_per_month = self.price * (30.5 / self.avg_duration) if self.avg_duration else 0
        self.c_volume = c_volume

    def add_date(self, date=date.today()):
        """Accepts a date in a datetime.date object and adds it into the dates list."""
        self.dates.append(date)
        self.dates.sort()

        self.compute_avg_duration()
        self.ending = (self.dates[-1] + timedelta(days=self.avg_duration))

    def compute_duration(self, date1, date2):
        delta = abs(date2 - date1)
        return delta.days
    
    def compute_avg_duration(self):
        if len(self.dates) < 2:
            self.avg_duration = 0
        else:
            total_duration = self.compute_duration(self.dates[0], self.dates[-1])
            self.avg_duration = int(total_duration / (len(self.dates) - 1))
        
if __name__ == "__main__":
    product = Product("Shampoo", [
        date(2023, 6, 20),
        date(2023, 8, 29),
        date(2023, 10, 8),
        date(2023, 11, 16)
    ])

    print(product.ending)