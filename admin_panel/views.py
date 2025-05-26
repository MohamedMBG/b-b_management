from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json

from Gestion_stock import settings
from .forms import ProduitForm, FournisseurForm, ClientForm
from API.models import Produit, Fournisseur, Client

# --- Vue pour la connexion ---

def login(request):
    """Affiche la page de connexion."""
    return render(request, "login.html")

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        email = request.POST.get("email", False)
        password = request.POST.get('password', False)
        # Use the custom Client model for authentication if it's the intended user model
        # If using Django's default User, adjust authentication accordingly.
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            # Check if the user is staff or superuser to grant admin access
            if user.is_staff or user.is_superuser:
                auth_login(request, user) # Use the renamed auth_login
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Accès non autorisé pour ce type d\'utilisateur.')
                return render(request, self.template_name)
        else:
            messages.error(request, 'Mot de passe ou nom d\'utilisateur incorrect.')
            return render(request, self.template_name)

class LogoutView(TemplateView):
    """Déconnecte un utilisateur."""
    template_name = 'login.html'

    def get(self, request, **kwargs):
        auth_logout(request)
        return render(request, self.template_name)

# --- Utilitaire générique pour les vues CRUD ---
def handle_form_submission(request, form_class, instance=None, success_status=200):
    """
    Gère la validation et la sauvegarde d'un formulaire pour les opérations CRUD.
    :param request: La requête HTTP.
    :param form_class: La classe du formulaire à valider.
    :param instance: (Optionnel) Objet existant pour une modification.
    :param success_status: Statut HTTP en cas de succès.
    :return: JsonResponse.
    """
    try:
        data = json.loads(request.body)
        form = form_class(data, instance=instance)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'success': True, 'data': model_to_dict(obj)}, status=success_status)
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON invalide.")
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Vues pour Produits ---
@require_GET
def list_produits(request):
    """Retourne la liste des produits."""
    produits = Produit.objects.select_related('fournisseur').all()
    data = [
        {
            'id': produit.id,
            'reference': produit.reference,
            'designation': produit.designation,
            'prixU': str(produit.prixU),
            'quantite': produit.quantite,
            'alert_quantite': produit.alert_quantite,
            'fournisseur': produit.fournisseur.libelle,
        }
        for produit in produits
    ]
    return JsonResponse({'produits': data})

@csrf_exempt
@require_POST
def add_produit(request):
    """Ajoute un produit."""
    return handle_form_submission(request, ProduitForm, success_status=201)

@csrf_exempt
def update_produit(request, pk):
    """Met à jour un produit."""
    produit = get_object_or_404(Produit, pk=pk)
    return handle_form_submission(request, ProduitForm, instance=produit)

@csrf_exempt
@require_POST
def delete_produit(request, pk):
    """Supprime un produit."""
    produit = get_object_or_404(Produit, pk=pk)
    try:
        produit.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Vues pour Fournisseurs ---
@require_GET
def list_fournisseurs(request):
    """Retourne la liste des fournisseurs."""
    fournisseurs = Fournisseur.objects.all()
    data = [
        {
            'id': f.id,
            'libelle': f.libelle,
            'email': f.email,
            'telephone': f.telephone,
            'adresse': f.adresse,
        }
        for f in fournisseurs
    ]
    return JsonResponse({'fournisseurs': data})

@csrf_exempt
@require_POST
def add_fournisseur(request):
    """Ajoute un fournisseur."""
    return handle_form_submission(request, FournisseurForm, success_status=201)

@csrf_exempt
def update_fournisseur(request, pk):
    """Met à jour un fournisseur."""
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    return handle_form_submission(request, FournisseurForm, instance=fournisseur)

@csrf_exempt
@require_POST
def delete_fournisseur(request, pk):
    """Supprime un fournisseur."""
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    try:
        fournisseur.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Vues pour Clients ---
@require_GET
def list_clients(request):
    """Retourne la liste des clients."""
    clients = Client.objects.filter(is_staff=False, is_superuser=False)
    data = [
        {
            'id': client.id,
            'nom': client.nom,
            'prenom': client.prenom,
            'email': client.email,
            'telephone': client.telephone,
            'adresse': client.adresse,
        }
        for client in clients
    ]
    return JsonResponse({'clients': data})

@csrf_exempt
@require_POST
def add_client(request):
    """Ajoute un client."""
    return handle_form_submission(request, ClientForm, success_status=201)

@csrf_exempt
def update_client(request, pk):
    """Met à jour un client."""
    client = get_object_or_404(Client, pk=pk)
    return handle_form_submission(request, ClientForm, instance=client)

@csrf_exempt
@require_POST
def delete_client(request, pk):
    """Supprime un client."""
    client = get_object_or_404(Client, pk=pk)
    try:
        client.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)
# admin_panel/views.py

from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

def admin_logout_view(request):
    """
    Déconnecte l'administrateur et redirige vers la page principale.
    """
    auth_logout(request)
    return redirect('/')