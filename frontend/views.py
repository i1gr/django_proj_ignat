from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect


# Create your views here.
def profile(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if user.is_staff:
        return redirect('admin_profile')

    context = {
        'title': 'Profile',
        'nav_active': 'account',
    }
    return render(request, 'frontend/index.html', context=context)


def admin_profile(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not user.is_staff:
        return redirect('profile')

    context = {
        'title': 'Profile',
        'nav_active': 'account',
    }
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

    if not user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        raise PermissionDenied

    context = {
        'title': 'Kanban Board',
        'nav_active': 'None',
        'block_content': 'full_screen',
    }
    return render(request, 'frontend/index.html', context=context)
