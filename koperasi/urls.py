from django.conf.urls import url
from . import views


app_name = 'koperasi'


urlpatterns = [
    url(r'^$', views.index, name='main'),
    url(r'^akun/add/$', views.AkunCreate, name='akun-add'),
    url(r'^akun/(?P<akun_id>[0-9]+)/delete/$', views.hapus_akun, name='hapus-akun'),
    url(r'^akun/(?P<akun_id>[0-9]+)/$', views.detail_akun, name='detail-akun'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^buat-koperasi$', views.create_koperasi, name='buat-koperasi'),
]
