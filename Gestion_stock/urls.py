from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('API/', include('API.urls')),
    path('', include('frontoffice.urls')),

    re_path(r'^admindash/$', TemplateView.as_view(template_name='frontoffice/master_page.html')),
    re_path(r'^admindash/statistiques$', TemplateView.as_view(template_name='frontoffice/page/statistiques.html')),
    re_path(r'^admindash/produits$', TemplateView.as_view(template_name='frontoffice/page/produit.html')),
    re_path(r'^admindash/clients$', TemplateView.as_view(template_name='frontoffice/page/client.html')),
    re_path(r'^admindash/fournisseurs$', TemplateView.as_view(template_name='frontoffice/page/fournisseur.html')),
    re_path(r'^admindash/achats$', TemplateView.as_view(template_name='frontoffice/page/achat.html')),
]
