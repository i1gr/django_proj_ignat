from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from service.models import Services

# Create your views here.
# def service(request):
# 	return render(request, 'service/service.html', {'title': f'Service {1}', 'nav_active': 'None'})

def order(request):
	return render(request, 'service/order.html', {'title': f'Service {1}', 'nav_active': 'None'})


def plug(request, service_id):
	return HttpResponse(f'It is plug, #{service_id}')


def service(request, service_slug):
	service_data = get_object_or_404(Services, slug=service_slug)

	context = {
		'title': f'{service_data.name}',
		'nav_active': 'None',
		'service_data': service_data
	}
	return render(request, 'service/service.html', context=context)