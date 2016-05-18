from django.db import models
from django.core.exceptions import ValidationError

class Menu(models.Model):
	name = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.name

class MenuItem(models.Model):
	"""Пункт любого уровня в иерархической сруктуре меню"""
	title = models.CharField(max_length=200)
	parent = models.ForeignKey('self', null=True, blank=True, help_text="If left blank then creates root node")
	menu = models.ForeignKey(Menu, null=True, blank=True, related_name="all_items", help_text="Required if parent is null, else leave blank: will be the same as parent")
	url = models.CharField(max_length=200, blank=True, null=True, help_text="Will be 'parent.URL/title' if left blank")
	lvl = models.IntegerField(default=0, editable=False)
	def save(self):
		if self.parent:
			self.menu = self.parent.menu
			if not self.url:
				self.url = "%s/%s" % (self.parent.url, self.title)
			self.lvl = self.parent.lvl + 1
		else:
			if not self.url:
				self.url = "/%s" % (self.title)
			self.lvl = 0
		if not self.parent and not self.menu:
			raise ValidationError("Field Parent or Menu must be filled out")
		super().save()
	def __str__(self):
		return "Title: %s | URL: %s | Menu name: %s" % (self.title, self.url, self.menu)


