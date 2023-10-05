from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.validators import MinValueValidator

def words_validator(comment):
    if len(comment) < 4:
        raise ValidationError("Comment must be at least 4 words long")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(validators=[words_validator])

class userform(forms.Form):
    username = forms.CharField(max_length=50)

class Calculateform(forms.Form):
    row = forms.IntegerField(
        min_value=1,  # 设置最小值为1
        initial=1,   # 设置默认值为1（可选）
    )
    line = forms.IntegerField(
        min_value=1,  # 设置最小值为1
        initial=1,   # 设置默认值为1（可选）
    )
    def clean_row(self):
        row = self.cleaned_data['row']
        if row < 1:
            raise forms.ValidationError("行数必须大于等于1")
        return row
    
    def clean_my_list(self):
        line = self.cleaned_data['my_list']
        if line < 1:
            raise forms.ValidationError(" 列数必须大于等于1")
        return line