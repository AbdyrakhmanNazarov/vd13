from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.html import mark_safe
from django_resized import ResizedImageField

# ======================== Категории авто ========================
class Group(models.Model):
    name = models.CharField(
        max_length=100, default="Без имени", verbose_name="Название категории"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# ======================== Машины ========================
class Cars(models.Model):
    TYPE_ENGINE_CHOICES = [
        ("Бензин", "Бензин"),
        ("Дизель", "Дизель"),
        ("Гибрид", "Гибрид"),
        ("Прочий", "Прочий"),
    ]

    # Основные данные
    owner = models.CharField(max_length=50, verbose_name="Владелец", null=True, blank=True)
    brand = models.CharField(max_length=50, verbose_name="Марка", null=True, blank=True)
    model = models.CharField(max_length=50, verbose_name="Модель", null=True, blank=True)
    year = models.IntegerField(verbose_name="Год выпуска", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name="Телефон", region="KG", default="+996000000000")
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    avatar = ResizedImageField(
        size=[300, 300],       # размеры картинки (ширина, высота)
        crop=['middle', 'center'],  # как обрезать, если не пропорционально
        upload_to='avatars/',  # куда сохранять файлы (media/avatars/)
        null=True,
        blank=True
    )

    # Двигатель
    engine = models.CharField(max_length=15, choices=TYPE_ENGINE_CHOICES, default="Бензин", verbose_name="Тип двигателя")
    engine_capacity = models.DecimalField(verbose_name="Объем двигателя (л)", max_digits=3, decimal_places=1, null=True, blank=True)

    # Госномер — теперь необязательный и уникальность проверяется вручную
    number_plate = models.CharField(max_length=20, null=True, blank=True, unique=False)

    # Даты очистки двигателя
    engine_check_1 = models.DateField(verbose_name="Очистка двигателя — 1 раз", null=True, blank=True)
    engine_check_2 = models.DateField(verbose_name="Очистка двигателя — 2 раз", null=True, blank=True)
    engine_check_3 = models.DateField(verbose_name="Очистка двигателя — 3 раз", null=True, blank=True)

    # Системные даты
    join_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # Методы
    def avatar_preview(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" width="50" height="50" style="border-radius:5px"/>')
        return "Нет аватара"

    avatar_preview.short_description = "Аватар"

    def __str__(self):
        return f"{self.brand} {self.model} - {self.number_plate or 'без номера'}"

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"


# ======================== Отзывы клиентов ========================
class ClientReview(models.Model):
    name = models.CharField("Имя клиента", max_length=100)
    email = models.EmailField("Почта клиента")
    review = models.TextField("Отзыв клиента")
    rating = models.PositiveSmallIntegerField("Оценка (звезды)", default=5)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Отзыв клиента"
        verbose_name_plural = "Отзывы клиентов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
