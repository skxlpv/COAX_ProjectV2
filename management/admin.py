from django.contrib import admin

from management.models import Category, Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category_name",
                    "description", "quantity",
                    "price_of_one", "full_usd")

    def full_usd(self, obj: Item) -> str:
        if obj:
            return f"{obj.full_price :.2f}"
        return ''


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
