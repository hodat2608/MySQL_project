from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Nhan_vien, Thong_tin_nhan_vien


class Add_nhanvien_Form(forms.ModelForm):
    class Meta:
        model = Nhan_vien
        fields = ['Hoten', 'Msnv','Phongban']

class Evaluate(forms.ModelForm):
    class Meta:
        model = Thong_tin_nhan_vien
        fields = ['Ngay_kiem_tra','Doi_tuong_danh_gia','Lan_danh_gia','Thoi_gian_TC','Ma_hoc_trinh','Diem','Phan_dinh']



class EvaluationForm(forms.Form):
    CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]
    Doi_tuong_danh_gia = forms.MultipleChoiceField(
        choices=CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'horizontal-checkbox'}),
    )

    