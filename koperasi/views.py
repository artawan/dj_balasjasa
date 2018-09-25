from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
# from django.views import generic
from .models import AkunPerkiraan, Koperasi, Membership
from .forms import UserForm, AkunForm, KoperasiForm
import datetime
from django.forms import modelformset_factory


def index(request):
    return render(request, 'koperasi/index.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'koperasi/login.html')
    else:
        k = Koperasi.objects.filter(user=request.user)
        context = {
            'all_koperasi': k,
            'all_akun': AkunPerkiraan.objects.filter(koperasi=k),
        }
        return render(request, 'koperasi/dashboard.html', context)


def detail_akun(request, akun_id):
    if not request.user.is_authenticated:
        return render(request, 'koperasi/login.html')
    else:
        akun = get_object_or_404(AkunPerkiraan, pk=akun_id)
        context = {
            'akunperkiraan': akun,
        }
        return render(request, 'koperasi/detail.html', context)


def hapus_akun(request, akun_id):
    if not request.user.is_authenticated:
        return render(request, 'koperasi/login.html')
    else:
        akun = AkunPerkiraan.objects.get(pk=akun_id)
        akun.delete()
        k = Koperasi.objects.filter(user=request.user)
        context = {
            'all_koperasi': k,
            'all_akun': AkunPerkiraan.objects.filter(koperasi=k),
        }
        return render(request, 'koperasi/dashboard.html', context)


def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_koperasi = Koperasi.objects.filter(user=request.user)
                return render(request, 'koperasi/dashboard.html', {'all_koperasi': all_koperasi})
    else:
        context = {
            "form": form,
            'error_message': 'Form is not valid'
        }
        return render(request, 'koperasi/register.html', context)

    context = {
        "form": form,
    }
    return render(request, 'koperasi/register.html', context)


def create_koperasi(request):
    KoperasiFormSet = modelformset_factory(Koperasi, form=KoperasiForm, fields='__all__')
    if request.method == 'POST':
        data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0', 'form-0-tgl': datetime.date.today()}
        form = KoperasiFormSet(request.POST, data)
        if form.is_valid():
            koperasi = form.save(commit=False)
            koperasi.user = request.user
            koperasi.save()
            m = Membership(koperasi=koperasi, tgl_daftar="2018-01-12", tgl_berakhir="2019-11-12", masa_aktif="12", status=True)
            m.save()
            return render(request, 'koperasi/dashboard.html', {'koperasi': koperasi})
    else:
        data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0', 'form-0-tgl': datetime.date.today(), 'form-0-DELETE': 'on', }
        form = KoperasiFormSet(data, initial=[{'tgl': datetime.date.today()}])
    context = {'form': form}
    return render(request, 'koperasi/create_koperasi.html', context)


def login_user(request):
    # lakukan pengecekan apakah user sudah di autentikasi, jika sudah arahkan ke halaman dashboard, jika belum lakukan pengecekan user
    if request.user.is_authenticated:
        k = Koperasi.objects.filter(user=request.user)
        context = {
            'all_koperasi': k,
            'all_akun': AkunPerkiraan.objects.filter(koperasi=k.first()),
            'user': request.user
        }
        return render(request, 'koperasi/dashboard.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                k = Koperasi.objects.filter(user=request.user)
                context = {
                    'all_koperasi': k,
                    'all_akun': AkunPerkiraan.objects.filter(koperasi=k.first()),
                    'user': request.user
                }
                return render(request, 'koperasi/dashboard.html', context)
            else:
                return render(request, 'koperasi/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'koperasi/login.html', {'error_message': 'Invalid login'})
    return render(request, 'koperasi/login.html')


def logout_user(request):
    logout(request)  # logout auth user
    form = UserForm(request.POST or None)  # mengambil forms dari daftar form
    context = {
        "form": form,
    }
    return render(request, 'koperasi/login.html', context)


def AkunCreate(request):
    form = AkunForm(request.POST or None)
    if form.is_valid():
        akunperkiraan = form.save(commit=False)
        akunperkiraan.koperasi = Koperasi.objects.get(user=request.user)
        akunperkiraan.save()
        return render(request, 'koperasi/detail.html', {'akunperkiraan': akunperkiraan})
    context = {
        "form": form,
    }
    return render(request, 'koperasi/create_akun.html', context)
