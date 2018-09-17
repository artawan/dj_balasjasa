from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import datetime


class Koperasi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, verbose_name="nama koperasi")
    badan_hukum = models.CharField(max_length=200, verbose_name="nomor badan hukum")
    telp = models.CharField(max_length=20)
    alamat = models.CharField(max_length=250)
    fax = models.CharField(max_length=50)
    tgl = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.pk) + " " + self.nama + " " + self.badan_hukum


class Membership(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    tgl_daftar = models.DateField()
    tgl_berakhir = models.DateField()
    masa_aktif = models.IntegerField()
    status = models.BooleanField()

    def __str__(self):
        return " Koperasi: " + self.koperasi.nama + " Tgl daftar: " + str(self.tgl_daftar) + " Tgl berakhir:" + str(self.tgl_berakhir)

# TODO: ManyToMany - Koperasi memiliki banyak AkunPerkiraan


class Login(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)


class AkunPerkiraan(models.Model):
    KATEGORI = (('1', 'Aktiva'), ('2', 'Hutang'), ('3', 'Modal'), ('4', 'Pendapatan'), ('5', 'HPP'), ('6', 'Biaya'))
    SALDO_NORMAL = (('D', 'Debet'), ('K', 'Kredit'))
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    kode_akun = models.CharField(max_length=50)
    saldo_normal = models.CharField(max_length=10, choices=SALDO_NORMAL)
    kategori = models.CharField(max_length=1, choices=KATEGORI)

    def __str__(self):
        return self.kategori + "." + self.kode_akun + " - " + self.nama + " - " + self.koperasi

    def get_absolute_url(self):
        return reverse('koperasi:detail-akun', kwargs={'pk': self.pk})


class Anggota(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    JK = (('L', 'Laki-laki'), ('P', 'Perempuan'))
    no_identitas = models.CharField(max_length=50)
    nama = models.CharField(max_length=250)
    jk = models.CharField(max_length=1, choices=JK)
    tempat_lahir = models.CharField(max_length=100, verbose_name='tempat lahir')
    tgl_lahir = models.DateField(verbose_name='tanggal lahir')
    alamat = models.CharField(max_length=300)
    pekerjaan = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    pic = models.FileField(verbose_name='foto')
    scan_identitas = models.FileField()


class TransaksiSimpan(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    tgl = models.DateTimeField(verbose_name='tanggal')
    jumlah = models.IntegerField()
    keterangan = models.CharField(max_length=200)
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)


class TransaksiPinjam(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    tgl = models.DateTimeField(verbose_name='tanggal')
    jumlah = models.IntegerField()
    keterangan = models.CharField(max_length=200)
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)


class Transaksi(models.Model):
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE)
    tgl = models.DateTimeField(verbose_name='tanggal')
    dari_akun = models.CharField(max_length=100)
    untuk_akun = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    user = models.CharField(max_length=100)
