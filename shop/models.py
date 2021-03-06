from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 150 , db_index = True)
	#slug – which is a unique field, this help us in building canonical urls later
	slug = models.SlugField(max_length = 150, unique = True, db_index = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category' , args = [self.slug])

class Products(models.Model):
	category = models.ForeignKey(Category, related_name = 'products' , on_delete = models.CASCADE)
	name = models.CharField(max_length = 100, db_index = True)
	slug = models.SlugField(max_length = 100, db_index = True)
	description = models.TextField(blank  = True)
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	available = models.BooleanField(default = True)
	created_at = models.DateTimeField(auto_now_add = True)
	stock  = models.PositiveIntegerField()
	updated_at = models.DateTimeField(auto_now = True)
	image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'))

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail' , args = [self.id, self.slug])
