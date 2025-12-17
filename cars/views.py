from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from cars.models import Cars, Group, ClientReview
from datetime import datetime
from urllib.parse import quote


# ----------------------------------------------------------------------------
def main(request):
    return render(request, "index.html")


# ----------------------------------------------------------------------------
def car_detail(request, id):
    car = get_object_or_404(Cars, id=id)
    return render(request, "car_detail.html", {"car": car})


# ----------------------------------------------------------------------------
def car_create(request):
    groups = Group.objects.all()

    if request.method == "POST":
        owner = request.POST.get("owner")
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        year = request.POST.get("year")
        engine_capacity = request.POST.get("engine_capacity")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        group_id = request.POST.get("group")
        avatar_file = request.FILES.get("avatar")
        description = request.POST.get("description")
        number_plate = request.POST.get("number_plate")  # необязательный

        # Сохраняем аватар
        avatar_path = None
        if avatar_file:
            fs = FileSystemStorage(location="media/Авто_фото")
            filename = fs.save(avatar_file.name, avatar_file)
            avatar_path = f"Авто_фото/{filename}"

        # Проверяем уникальность госномера
        if number_plate and Cars.objects.filter(number_plate=number_plate).exists():
            number_plate = None  # если такой уже есть — просто игнорируем

        # Создаём запись
        car = Cars.objects.create(
            owner=owner,
            brand=brand,
            model=model,
            year=year,
            engine_capacity=engine_capacity,
            phone_number=phone_number,
            email=email,
            group_id=group_id,
            avatar=avatar_path,
            description=description,
            number_plate=number_plate or None,
            is_active=True,
        )

        # Сообщение мастеру
        master_whatsapp = "996553029494"  # номер мастера без '+'
        text = f"Новый клиент!\nВладелец: {owner}\nМарка: {brand}\nМодель: {model}\nГод: {year}\nОбъем двигателя: {engine_capacity}\nТелефон: {phone_number}"
        wa_url = f"https://wa.me/{master_whatsapp}?text={quote(text)}"

        # Редирект на главную с WhatsApp-ссылкой
        response = redirect("main")
        response["Location"] += f"?whatsapp_url={quote(wa_url)}"
        return response

    return render(request, "car_create.html", {"groups": groups})


# ----------------------------------------------------------------------------
def car_update(request, id):
    car = get_object_or_404(Cars, id=id)
    groups = Group.objects.all()
    success = False

    if request.method == "POST":
        car.owner = request.POST.get("owner")
        car.brand = request.POST.get("brand")
        car.model = request.POST.get("model")
        car.year = request.POST.get("year")
        car.description = request.POST.get("description")
        car.phone_number = request.POST.get("phone_number")
        car.email = request.POST.get("email")
        car.is_active = bool(request.POST.get("is_active"))
        car.engine = request.POST.get("engine")
        car.engine_capacity = request.POST.get("engine_capacity")
        car.number_plate = request.POST.get("number_plate") or None

        def parse_date(date_str):
            if date_str:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            return None

        car.engine_check_1 = parse_date(request.POST.get("engine_check_1"))
        car.engine_check_2 = parse_date(request.POST.get("engine_check_2"))
        car.engine_check_3 = parse_date(request.POST.get("engine_check_3"))

        group_id = request.POST.get("group")
        car.group = get_object_or_404(Group, id=group_id)

        if "avatar" in request.FILES:
            avatar_file = request.FILES["avatar"]
            fs = FileSystemStorage(location="media/Авто_фото")
            filename = fs.save(avatar_file.name, avatar_file)
            car.avatar = f"Авто_фото/{filename}"

        car.save()
        success = True

    return render(request, "car_update.html", {"car": car, "groups": groups, "success": success})


# ----------------------------------------------------------------------------
def car_delete(request, id):
    car = get_object_or_404(Cars, id=id)
    car.delete()
    return redirect("main")


# ----------------------------------------------------------------------------
def about(request):
    return render(request, "about.html")


# ----------------------------------------------------------------------------
def clients(request):
    cars = Cars.objects.filter(is_active=True).order_by("-id")[:4]
    return render(request, "clients.html", {"cars": cars})


# ----------------------------------------------------------------------------
def clients_review(request):
    success = None

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        review_text = request.POST.get("review")
        rating = request.POST.get("rating")

        if name and email and review_text and rating:
            ClientReview.objects.create(
                name=name,
                email=email,
                review=review_text,
                rating=int(rating),
                is_active=True,
            )
            success = True
        else:
            success = False

    reviews = ClientReview.objects.filter(is_active=True).order_by("-created_at")[:4]
    return render(request, "clients_review.html", {"success": success, "reviews": reviews})
