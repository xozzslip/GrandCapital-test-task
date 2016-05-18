from django.shortcuts import render
from .models import Menu, MenuItem

def get_menu(request, *arg):
	return render(request, 'menu/main.html')


