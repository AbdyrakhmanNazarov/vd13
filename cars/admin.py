from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Cars, Group, ClientReview

# -------------------- Форма для Cars --------------------
class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"


# -------------------- Админ для Cars --------------------
class CarsAdmin(admin.ModelAdmin):
    form = CarsForm  # используем кастомную форму
    readonly_fields = ("join_date", "updated_date")
    list_display = (
        "id",
        "number_plate",
        "is_active",
        "phone_number",
        "owner",
        "avatar_preview",
    )
    list_display_links = ("id", "number_plate")
    list_filter = ("is_active", "group")
    search_fields = ("owner",)
    list_editable = ("phone_number", "owner")
    list_per_page = 10
    save_on_top = True

    # Метод для отображения миниатюры аватара
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = "Аватар"


# -------------------- Админ для Group --------------------
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    list_per_page = 10


# -------------------- Админ для ClientReview --------------------
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "rating_stars", "is_active", "created_at")
    list_filter = ("is_active", "rating")
    search_fields = ("name", "email", "review")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 10

    # Красивое отображение рейтинга звезд
    def rating_stars(self, obj):
        return format_html("{}".format("★" * obj.rating + "☆" * (5 - obj.rating)))
    rating_stars.short_description = "Рейтинг"


# -------------------- Регистрация моделей --------------------
admin.site.register(Cars, CarsAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ClientReview, ClientReviewAdmin)
