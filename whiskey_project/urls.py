from django.contrib import admin
from django.urls import path

from hielander_whiskey_app.views.login import login_page
from hielander_whiskey_app.views.dashboard import dashboard_page
from hielander_whiskey_app.views.masterclass_reservering import masterclass_reservering_page
from hielander_whiskey_app.views.masterclass_bevestiging import masterclass_bevestiging_page
from hielander_whiskey_app.views.botteling_reservering import botteling_reservering_page
from hielander_whiskey_app.views.botteling_bevestiging import botteling_bevestiging_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_page),
    path("dashboard/", dashboard_page, name='dashboard'),
    path("masterclass_reservering/", masterclass_reservering_page),
    path("masterclass_bevestiging/", masterclass_bevestiging_page,
         name="masterclass_bevestiging"),
    path("botteling_reservering/", botteling_reservering_page),
    path("botteling_bevestiging/", botteling_bevestiging_page, 
         name="botteling_bevestiging"),
]