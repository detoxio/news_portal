from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_header',
            'post_text',
            'author_name',
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get('post_text')
        if post_text is not None and len(post_text) < 20:
            raise ValidationError({
                "description": "Текст новости должен быть не менее 20 символов"
            })
        header = cleaned_data.get("post_header")
        if header == post_text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data