#We import decimal data type in order to avoid issue of rounding off with regard to price.

from decimal import Decimal
from django.conf import settings
from shop.models import Product
#a cart class that will help us manage our shopping cart.
class Cart(object):
	def __init__(self, request):
		#We store the current session using self.session = request.session and this help in making sure that the cart is available for other method in our Cart class.
		self.session = request.session
		#to get the cart using get method in the current session.
		cart = self.session.get(settings.CART_SESSION_ID)
		#If there is not cart in the session, we set an empty cart on line 11 by settings an empty dictionary in the session
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, quantity = 1, update_quantity = False):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity' : 0, 'price' : str(product.price)}

		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()
#We create save method which tracks changes in the cart and marks sessions as modified using self.session.modified = True
	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True
		#We create a method to remove a single product from the cart and save the cart in the session.
	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()
				#We define an __iter__ (self) method which help us iterate through the items in contained in our cart and get the related product instances.
	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in = product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	#We define a len method to return the total number of items store in our cart.
	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True

