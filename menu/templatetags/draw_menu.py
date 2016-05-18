from django import template
from menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
	current_item = get_current_item(context['request'])
	menu = Menu.objects.get(name=menu_name)
	START_LVL = 0
	menuitems = list(menu.all_items.filter(lvl=START_LVL))
	if current_item.menu == menu:
		menuitems = expand_menu_until(menuitems, current_item)
	return{"menuitems":menuitems, "menu":menu}
	
def expand_menu_until(zero_lvl_items, until_item):
	"""Функция для развертки пунктов меню. 
	На вход подется список пунктов меню нулевого уровня и пункт, до которого требуется развертка этого меню (until_item).
	Выходом является полностью развернутое меню вплоть до уровня, на котором находится until_item, включая его подпункты"""
	START_LVL = 0
	queue = zero_lvl_items
	expand_menuitems = []
	lvl = START_LVL
	while len(queue) > 0:
		item = queue.pop(0)
		lvl_dif = lvl - item.lvl
		if lvl_dif > 0:
			html_li = "out" #При герерации HTML вместо 'out' будет вставлен закрывающий тэг </ul>
		elif lvl_dif < 0:
			html_li = "in" #Будет вставлен открывающийся тэг <ul>
		expand_menuitems.extend([html_li for _ in range (abs(lvl_dif))]) 
		lvl = item.lvl
		expand_menuitems.append(item)
		if lvl < until_item.lvl or item == until_item:
			queue = list(item.menuitem_set.all()) + queue
	expand_menuitems.extend([html_li for _ in range (abs(lvl))])
	return expand_menuitems

def get_current_item(request):
	curren_url = request.path
	current_item = MenuItem.objects.get(url=curren_url)
	return current_item