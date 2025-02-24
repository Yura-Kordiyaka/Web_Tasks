from typing import Protocol


class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> None:
        pass


class CreditCardPayment:
    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using Credit Card")


class PayPalPayment:
    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using PayPal")


class ShoppingCart:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def checkout(self, amount: float):
        self.strategy.pay(amount)


cart = ShoppingCart(CreditCardPayment())
cart.checkout(100.0)

cart.strategy = PayPalPayment()
cart.checkout(50.0)
