from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Category, Products

#product_list use to display a list of products
# category_slug=None use if products are filtered using a given category by our users.

def product_list(request, category_slug = None):
	category = None
	categories = Category.objects.all()
	products = Products.objects.filter(available = True)
	if category_slug:
		category = get_object_or_404(Category, slug = category_slug)
		products = Products.objects.filter(category = category)

	context = {
	'category' : category,
	'categories' : categories,
	'products' : products
	}
	return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
	product = get_object_or_404(Products, id = id, slug = slug, available= True)
	context = {
	'product' : product
	}
	return render(request, 'shop/product/details.html', context)


