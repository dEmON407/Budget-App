class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            description = f"{item['description'][:23]:23}"
            amount = f"{item['amount']:>7.2f}"
            items += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

def create_spend_chart(categories):
    # Calculate the total spend and spend per category
    total_spend = 0
    category_spend = []
    for category in categories:
        spend = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        category_spend.append((category.name, spend))
        total_spend += spend

    # Calculate the percentage spent for each category
    percentages = [(name, int((spend / total_spend) * 100)) for name, spend in category_spend]

    # Create the bar chart
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for name, percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    # Create the names vertically
    max_length = max(len(name) for name, _ in percentages)
    for i in range(max_length):
        chart += "     "
        for name, _ in percentages:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   "
        chart += "\n"

    return chart.rstrip("\n")

# Example usage
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)

auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)
print(auto)
print(create_spend_chart([food, clothing, auto]))