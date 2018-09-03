from django import forms
#we create a range that start from 1 to 26. We will use this as drop down for user to select number of items.
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,26)]

class CartAddProductForm(forms.Form):
	quantity = forms.TypedChoiceField(choices = PRODUCT_QUANTITY_CHOICES, coerce = int)
	update = forms.BooleanField(required = False, initial = False, widget = forms.HiddenInput)
