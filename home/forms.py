from django import forms
from .models import *


class productForm(forms.ModelForm):

	class Meta:
		model = products
		fields = ['name','price','discription','img','img2','img3','img4','catagory']

class disable_productForm(forms.ModelForm):

	class Meta:
		model = products
		fields = ['disable']

class contactForm(forms.ModelForm):

	class Meta:
		model = contact_message
		fields = ['name','email','subject','message']