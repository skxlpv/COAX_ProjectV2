from decimal import Decimal

from django.contrib import admin

from management.models import Category, Item
from forex_python.converter import CurrencyRates


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category_name",
                    "description", "quantity",
                    "price_of_one", "item_price_EUR",
                    "full_USD", "full_EUR",)

    def full_USD(self, obj: Item) -> str:
        return f"{obj.full_price :.2f}"

    def full_EUR(self, obj: Item) -> str:
        CurrencyRate = CurrencyRates()
        rate = CurrencyRate.get_rate('USD', 'EUR')
        return f"{(obj.full_price * Decimal(rate)):.2f}"

    def price_of_one(self, obj: Item) -> str:
        return f"{obj.price_of_one}"

    def item_price_EUR(self, obj: Item) -> str:
        CurrencyRate = CurrencyRates()
        rate = CurrencyRate.get_rate('USD', 'EUR')
        return f"{(obj.price_of_one * Decimal(rate)):.2f}"


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
