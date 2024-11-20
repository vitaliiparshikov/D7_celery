from django import forms
from .models import Subscriber, Category

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()