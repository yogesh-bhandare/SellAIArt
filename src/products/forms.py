from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment

input_css_class = "w-full text-gray-900 p-2 m-2"

class ProductFrom(forms.ModelForm):
    class Meta:
        model= Product
        fields= ['image', 'name','handle','price', 'description', 'prompt', 'category', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
            'prompt': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
            

class ProductUpdateFrom(forms.ModelForm):
    class Meta:
        model= Product
        fields= ['image', 'name','handle','price', 'description', 'prompt', 'category', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
            'prompt': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class

class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ["file", 'name', 'is_free', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class


ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForm,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form = ProductAttachmentForm,
    formset = ProductAttachmentModelFormSet,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)

