from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect


# Create your views here.
from service.services import get_notifications_count


def profile(request):
    user = request.user
    context = dict()

    context.update(get_notifications_count(user))

    if not user.is_authenticated:
        return redirect('login')

    if user.is_staff:
        return redirect('admin_profile')

    context.update({
        'title': 'Profile',
        'nav_active': 'account',
    })
    return render(request, 'frontend/index.html', context=context)


def admin_profile(request):
    user = request.user
    context = dict()

    context.update(get_notifications_count(user))

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_staff:
        return redirect('profile')

    context.update({
        'title': 'Profile',
        'nav_active': 'account',
    })
    return render(request, 'frontend/index.html', context=context)

# ??????????????????????
# def service(request):
#     context = {
#         'title': '!!!!!!!!!!!!!!!!!! service name',
#         'nav_active': 'none',
#     }
#     return render(request, 'frontend/index.html', context=context)


def kanban_board(request):
    user = request.user
    context = dict()

    context.update(get_notifications_count(user))

    if not user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        raise PermissionDenied

    context.update({
        'title': 'Kanban Board',
        'nav_active': 'orders',
        'block_content': 'full_screen',
    })
    return render(request, 'frontend/index.html', context=context)


def orders(request):
    user = request.user
    context = dict()

    if not user.is_authenticated:
        return redirect('login')
    if user.is_staff:
        return redirect(to='admin_orders')

    context.update(get_notifications_count(user))

    context.update({
        'title': 'Orders',
        'nav_active': 'orders',
        'block_content': 'full_screen',
    })
    return render(request, 'frontend/index.html', context=context)
