"""uchaguzi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import pages.views as page_views
import results.views as results_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_views.home, name='home'),
    re_path(
        r'^position/(?P<pos_id>[A-Z]{2})/$', page_views.position,
        name='position'),
    re_path(
        r'^result/(?P<pos_id>[A-Z]{2})/$', page_views.result, name='result'),
    re_path(
        r'^candidate/(?P<pos_id>[A-Z]{2})/$',
        page_views.candidate, name='candidate'),
    path('party/', page_views.parties, name='parties'),
    # path('party/<int:id>', page_views.parties, name='party'),
    re_path(
        r'^party/(?P<pos_id>[A-Z]{2})/$', page_views.parties,
        name='party'),
    path('county/', page_views.counties, name='counties'),
    re_path(
        r'^county/(?P<county_id>[0-9]{3})/$', page_views.counties,
        name='county'),
    path('constituency/', page_views.constituencies, name='constituencies'),
    re_path(
        r'^constituency/(?P<const_id>[0-9]{3})/$', page_views.constituencies,
        name='constituency'),
    path('ward/', page_views.wards, name='wards'),
    re_path(
        r'^ward/(?P<ward_id>[0-9]{4})/$', page_views.wards,
        name='ward'),
    path('polls/', page_views.polls, name='polls'),
    path('ps/', page_views.ps, name='ps'),
    re_path(
        r'^ps/(?P<rid>[0-9]{1})/(?P<area_id>[0-9]{3})/$',
        page_views.ps, name='p_station'),
    re_path(
        r'^pc/(?P<rid>[0-9]{1})/(?P<ward_id>[0-9]{4})/$',
        page_views.pc, name='pc'),
    path('search/', page_views.search, name='search'),
    path('vote/', page_views.vote, name='vote'),
    path('contact/', page_views.contact, name='contact'),
    re_path(
        r'^top/(?P<pos_id>[A-Z]{2})/$', page_views.top, name='top'),
    re_path(
        r'^results/(?P<pos_id>[A-Z]{2})/(?P<year>[0-9]{4})/$',
        page_views.results, name='results'),
    path('map/', results_views.maps, name='maps'),
]

admin.site.site_header = 'Uchaguzi Administration'
admin.site.site_title = 'Uchaguzi administration'
admin.site.index_title = 'Uchaguzi admin'
