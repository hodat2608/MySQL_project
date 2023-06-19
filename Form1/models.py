from django.db import models


class Nhan_vien(models.Model):
    Hoten = models.CharField(max_length=20,default="")
    Msnv =  models.IntegerField(max_length=5,default="")
    Phongban = models.CharField(max_length=20,default="")
    def __str__(self):
        return self.Hoten
   
class Thong_tin_nhan_vien(models.Model):
    key = models.ForeignKey(Nhan_vien, on_delete=models.CASCADE)
    Ngay_kiem_tra = models.DateField(max_length=20, default="")
    Doi_tuong_danh_gia = models.CharField(max_length=20,default="")
    Lan_danh_gia = models.CharField(max_length=20,default="")
    Thoi_gian_TC = models.IntegerField(max_length=100,default="")
    Ma_hoc_trinh = models.TextField(max_length=10,default="")
    Diem = models.IntegerField(max_length=100,default="")
    Phan_dinh = models.CharField(max_length=20,default="") 
    def __str__(self):
        return self.Ma_hoc_trinh
