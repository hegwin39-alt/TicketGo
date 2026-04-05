from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event


def home(request):
    featured_events = Event.objects.all()[:3]
    return render(request, "home.html", {"featured_events": featured_events})


def event_list(request):
    category = (request.GET.get("category") or "").strip()
    query = (request.GET.get("q") or "").strip()

    filtered_events = Event.objects.all()

    if category:
        filtered_events = filtered_events.filter(category__iexact=category)

    if query:
        filtered_events = (
            filtered_events.filter(title__icontains=query)
            | filtered_events.filter(location__icontains=query)
        )

    categories = Event.objects.order_by().values_list("category", flat=True).distinct()

    context = {
        "events": filtered_events,
        "categories": sorted(categories),
        "selected_category": category,
        "query": query,
    }
    return render(request, "event_list.html", context)


def event_detail(request, event_id):
    event = Event.objects.filter(pk=event_id).first()
    return render(request, "event_detail.html", {"event": event})


@login_required
def checkout(request, event_id):
    event = Event.objects.filter(pk=event_id).first()
    if not event:
        return redirect("event_list")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        try:
            tickets_count = int(request.POST.get("tickets_count", 1))
        except (TypeError, ValueError):
            tickets_count = 1
        total_price = event.price * tickets_count

        context = {
            "event": event,
            "name": name,
            "email": email,
            "tickets_count": tickets_count,
            "total_price": total_price,
        }
        return render(request, "success.html", context)

    return render(request, "checkout.html", {"event": event})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Вы успешно вошли в аккаунт.')
        next_url = request.GET.get('next') or request.POST.get('next')
        return redirect(next_url or 'home')

    return render(request, 'login.html', { 'form': form })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт успешно создан. Добро пожаловать!')
        return redirect('home')

    return render(request, 'register.html', { 'form': form })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('home')