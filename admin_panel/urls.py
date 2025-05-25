# admin_panel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"), # General logout
    path("admin_logout/", views.admin_logout_view, name="admin_logout"), # Specific admin logout URL used in template

    # API endpoints for AJAX calls
    path("api/produits/", views.list_produits, name="api_list_produits"),
    path("api/produits/add/", views.add_produit, name="api_add_produit"),
    path("api/produits/update/<int:pk>/", views.update_produit, name="api_update_produit"),
    path("api/produits/delete/<int:pk>/", views.delete_produit, name="api_delete_produit"),

    path("api/fournisseurs/", views.list_fournisseurs, name="api_list_fournisseurs"),
    path("api/fournisseurs/add/", views.add_fournisseur, name="api_add_fournisseur"),
    path("api/fournisseurs/update/<int:pk>/", views.update_fournisseur, name="api_update_fournisseur"),
    path("api/fournisseurs/delete/<int:pk>/", views.delete_fournisseur, name="api_delete_fournisseur"),

    path("api/clients/", views.list_clients, name="api_list_clients"),
    path("api/clients/add/", views.add_client, name="api_add_client"),
    path("api/clients/update/<int:pk>/", views.update_client, name="api_update_client"),
    path("api/clients/delete/<int:pk>/", views.delete_client, name="api_delete_client"),

    # Note: The main page URLs like /admindash/produits are still handled
    # by TemplateView in the main Gestion_stock/urls.py.
    # The data for these pages will be loaded via AJAX calls to the API endpoints above.
]

