from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect
from .models import Nhan_vien, Thong_tin_nhan_vien
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import render
from .forms import Add_nhanvien_Form, Evaluate
import csv

class List_nhan_vien(generic.ListView):
    template_name = 'DisplayWeb/Danh_sach_nhan_vien.html'
    context_object_name = 'Nhanviens'
    def get_queryset(self):
        return Nhan_vien.objects.all() 

class list_thongtinnhanvien(generic.DetailView):
    model = Nhan_vien
    template_name = 'DisplayWeb/Thong_tin_nhan_vien.html'    

def add_nhan_vien(request):
    if request.method == "POST": 
        form = Add_nhanvien_Form(request.POST)
        if form.is_valid():
            ho_ten = form.cleaned_data['Hoten']
            msnv = form.cleaned_data['Msnv']
            phong_ban = form.cleaned_data['Phongban']
            if Nhan_vien.objects.filter(Hoten=ho_ten).exists():
                return render(request, 'DisplayWeb/Danh_sach_nhan_vien.html',{ 'error1': "Nhân viên đã tồn tại!",})
            add_nv = Nhan_vien.objects.create(Hoten=ho_ten,Msnv=msnv,Phongban=phong_ban)
            add_nv.save()
            return redirect('Form1:List_nhan_vien')
    else:
        form = Add_nhanvien_Form()
    return redirect('Form1:List_nhan_vien')

def Evaluation(request,id_nhanvien):
    staff = Nhan_vien.objects.get(pk=id_nhanvien)
    if request.method == 'POST':
        form = Evaluate(request.POST)
        if form.is_valid():
            Ngay_kiem_tra = form.cleaned_data['Ngay_kiem_tra']
            doituongdanhgia = form.cleaned_data['Doi_tuong_danh_gia']
            landanhgia = form.cleaned_data['Lan_danh_gia']   
            thoigiantc = form.cleaned_data['Thoi_gian_TC']   
            mahoctrinh = form.cleaned_data['Ma_hoc_trinh']  
            diem = form.cleaned_data['Diem']  
            phandinh = form.cleaned_data['Phan_dinh']
            evalated = Thong_tin_nhan_vien(key_id = id_nhanvien,Ngay_kiem_tra=Ngay_kiem_tra,
            Doi_tuong_danh_gia=doituongdanhgia,Lan_danh_gia=landanhgia,
            Thoi_gian_TC=thoigiantc,Ma_hoc_trinh=mahoctrinh,
            Diem=diem,Phan_dinh=phandinh)
            evalated.save()
            return redirect(reverse('Form1:List_thong_tin', args=(staff.id,)))
    else: 
        form = Evaluate()
    return render(request,'DisplayWeb/EvaluateForm.html', {'form': form,'staff': staff}) 

def Evaluated_form(request,id_nhanvien):
    infor_form = get_object_or_404(Thong_tin_nhan_vien,pk=id_nhanvien)
    staff_id = infor_form.key_id
    staff_infor_form = get_object_or_404(Nhan_vien,pk=staff_id)
    return render(request, 'DisplayWeb/detail_infor_form.html', {'infor_form': infor_form, 'staff_infor_form':staff_infor_form})

def Delete_staff(request,id_nhanvien):
    del_staff = get_object_or_404(Nhan_vien,pk=id_nhanvien)
    del_staff.delete()
    return HttpResponseRedirect(reverse('Form1:List_nhan_vien'))

def Delete_infor(request,id_nhanvien):
    del_infor = get_object_or_404(Thong_tin_nhan_vien, pk=id_nhanvien)
    del_infor.delete()
    return HttpResponseRedirect(reverse('Form1:List_thong_tin', args=(del_infor.key_id,)))

def search_staff(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        show_form = True
        if query:
            Nhanviens = Nhan_vien.objects.filter(Msnv__icontains=query)
            if not Nhanviens: 
                return render(request, 'DisplayWeb/Danh_sach_nhan_vien.html', {
                        'error2': "Không tìm thấy mã nhân viên! ",
                    }) 
        else:
            Nhanviens = Nhan_vien.objects.filter
        context = {'Nhanviens': Nhanviens , 'show_form': show_form}
        return render(request, 'DisplayWeb/Danh_sach_nhan_vien.html', context)
    
def import_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
        csv_reader = csv.reader(decoded_file)
        next(csv_reader) 
        duplicate_datas = []
        for row in csv_reader:
            hoten = row[0]
            msnv = int(row[1])  
            phongban = row[2]
            if Nhan_vien.objects.filter(Hoten=hoten).exists():
                duplicate_datas.append(hoten)
            else :
                add_nhan_vien = Nhan_vien.objects.create(Hoten=hoten,Msnv=msnv,Phongban=phongban)
                add_nhan_vien.save()
        if duplicate_datas: 
            return render(request, 'DisplayWeb/Danh_sach_nhan_vien.html',{'duplicate_datas': duplicate_datas , 'error3': "Nhân viên !",})       
        return redirect('Form1:List_nhan_vien')
    return redirect('Form1:List_nhan_vien')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Form1:List_nhan_vien')
    else:
        form = UserCreationForm()
    return render(request, 'DisplayWeb/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            request.session['username'] = user.username
            return redirect('Form1:List_nhan_vien')
    else:
        form = AuthenticationForm()
    return render(request, 'DisplayWeb/login.html', {'form': form})
def user_logout(request):
    del request.session['username']
    auth_logout(request)
    return redirect('Form1:List_nhan_vien')




    
