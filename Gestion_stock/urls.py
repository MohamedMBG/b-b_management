from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from client_portal import views as client_views
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include('API.urls')),
    path('', include('admin_panel.urls')),

    re_path(r'^admindash/$', TemplateView.as_view(template_name='frontoffice/master_page.html')),
    path("admindash/statistiques/", TemplateView.as_view(template_name="frontoffice/page/statistiques.html"), name="admin_statistiques"),
    re_path(r'^admindash/produits$', TemplateView.as_view(template_name='frontoffice/page/produit.html'), name='admin_produits'),
    path("admindash/clients/", TemplateView.as_view(template_name="frontoffice/page/client.html"), name="admin_clients"),
    path("admindash/fournisseurs/", TemplateView.as_view(template_name="frontoffice/page/fournisseur.html"), name="admin_fournisseurs"),
    path("admindash/achats/", TemplateView.as_view(template_name="frontoffice/page/achat.html"), name="admin_achats"),
    # Client Portal URLs
    re_path('client/signup/', client_views.signup, name='client_signup'),
    re_path('client/signin/', client_views.signin, name='client_signin'),
    re_path('client/signout/',client_views.signout, name='client_signout'),
    re_path('client/dashboard/', client_views.dashboard, name='client_dashboard'),
]
