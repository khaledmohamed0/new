from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rate", "review"]

        widgets = {
            "rate": forms.HiddenInput(),
            "review": forms.Textarea(attrs={
                "class": "size-110 bor8 stext-102 cl2 p-lr-20 p-tb-10",
                "rows": 5,
            }),
        }