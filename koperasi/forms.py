from django import forms
from django.contrib.auth.models import User
from .models import AkunPerkiraan, Koperasi


class AkunForm(forms.ModelForm):
    attrs = {'class': 'w3-input w3-border'}
    KATEGORI = (('1', 'Aktiva'), ('2', 'Hutang'), ('3', 'Modal'), ('4', 'Pendapatan'), ('5', 'HPP'), ('6', 'Biaya'))
    SALDO_NORMAL = (('D', 'Debet'), ('K', 'Kredit'))
    attr = attrs
    attr['required'] = True
    attr['autofocus'] = 'True'
    nama = forms.CharField(widget=forms.TextInput(attr))
    kode_akun = forms.CharField(widget=forms.TextInput(attrs))
    saldo_normal = forms.CharField(widget=forms.Select(attrs, choices=SALDO_NORMAL))
    kategori = forms.CharField(widget=forms.Select(attrs, choices=KATEGORI))

    class Meta:
        model = AkunPerkiraan
        fields = ['nama', 'kode_akun', 'saldo_normal', 'kategori']


class KoperasiForm(forms.ModelForm):
    attrs = {'class': 'w3-input w3-border'}
    nama = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'autofocus': True, 'class': 'w3-input w3-border', }))
    badan_hukum = forms.CharField(widget=forms.TextInput(attrs))
    telp = forms.CharField(widget=forms.TextInput(attrs))
    alamat = forms.CharField(widget=forms.TextInput(attrs))
    fax = forms.CharField(widget=forms.TextInput(attrs))
    tgl = forms.DateTimeField(widget=forms.DateTimeInput(attrs))

    class Meta:
        model = Koperasi
        fields = ['nama', 'badan_hukum', 'telp', 'alamat', 'fax', 'tgl']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
