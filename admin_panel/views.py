# admin_panel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # Renamed login to auth_login
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt # Use carefully, consider CSRF protection for production
from django.core.paginator import Paginator
import json

from .forms import ProduitForm, FournisseurForm, ClientForm # Assuming ClientForm exists or will be created
from API.models import Produit, Fournisseur, Client # Assuming Client model is the correct one

# --- Authentication Views --- (Keep existing login/logout)

def login(request): # Keep original simple login render
    return render(request, "login.html")

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        # Use the custom Client model for authentication if it's the intended user model
        # If using Django's default User, adjust authentication accordingly.
        user = authenticate(request, username=username, password=password)
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
    template_name = 'login.html'

    def get(self, request, **kwargs):
        auth_logout(request) # Use the renamed auth_logout
        return render(request, self.template_name)

def admin_logout_view(request):
    auth_logout(request)
    return redirect('/')

# --- Product Views --- (New/Modified)

@require_GET
def list_produits(request):
    """Returns a JSON list of products for AJAX requests."""
    produits_list = Produit.objects.select_related('fournisseur').all()
    # Implement filtering/searching based on request.GET parameters if needed
    # Example: category = request.GET.get('category')
    # if category:
    #     produits_list = produits_list.filter(category=category) # Assuming category field exists

    data = [{
        'id': p.id,
        'reference': p.reference,
        'designation': p.designation,
        'prixU': str(p.prixU), # Convert Decimal to string for JSON
        'quantite': p.quantite,
        'alert_quantite': p.alert_quantite,
        'fournisseur_id': p.fournisseur.id,
        'fournisseur_libelle': p.fournisseur.libelle,
        'is_below_alert': p.is_below_alert_level()
        # Add category if it exists on the model
    } for p in produits_list]
    return JsonResponse({'produits': data})

@csrf_exempt # Consider proper CSRF handling for production
@require_POST
def add_produit(request):
    """Adds a new product via AJAX POST request."""
    try:
        data = json.loads(request.body)
        form = ProduitForm(data)
        if form.is_valid():
            produit = form.save()
            # Return the created product data for frontend update
            return JsonResponse({
                'success': True,
                'produit': {
                    'id': produit.id,
                    'reference': produit.reference,
                    'designation': produit.designation,
                    'prixU': str(produit.prixU),
                    'quantite': produit.quantite,
                    'alert_quantite': produit.alert_quantite,
                    'fournisseur_id': produit.fournisseur.id,
                    'fournisseur_libelle': produit.fournisseur.libelle,
                    'is_below_alert': produit.is_below_alert_level()
                }
            }, status=201)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt # Consider proper CSRF handling for production
def update_produit(request, pk):
    """Updates an existing product via AJAX PUT/POST request."""
    if request.method not in ['POST', 'PUT']:
        return HttpResponseNotAllowed(['POST', 'PUT'])

    produit = get_object_or_404(Produit, pk=pk)
    try:
        data = json.loads(request.body)
        form = ProduitForm(data, instance=produit)
        if form.is_valid():
            produit = form.save()
            return JsonResponse({
                'success': True,
                'produit': {
                    'id': produit.id,
                    'reference': produit.reference,
                    'designation': produit.designation,
                    'prixU': str(produit.prixU),
                    'quantite': produit.quantite,
                    'alert_quantite': produit.alert_quantite,
                    'fournisseur_id': produit.fournisseur.id,
                    'fournisseur_libelle': produit.fournisseur.libelle,
                    'is_below_alert': produit.is_below_alert_level()
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt # Consider proper CSRF handling for production
@require_POST # Or DELETE if preferred, adjust frontend accordingly
def delete_produit(request, pk):
    """Deletes a product via AJAX POST/DELETE request."""
    produit = get_object_or_404(Produit, pk=pk)
    try:
        produit.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Fournisseur Views --- (Placeholder - Implement similarly to Produit)

@require_GET
def list_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    data = [{'id': f.id, 'libelle': f.libelle, 'email': f.email, 'telephone': f.telephone, 'adresse': f.adresse} for f in fournisseurs]
    return JsonResponse({'fournisseurs': data})

@csrf_exempt
@require_POST
def add_fournisseur(request):
    try:
        data = json.loads(request.body)
        form = FournisseurForm(data)
        if form.is_valid():
            fournisseur = form.save()
            return JsonResponse({'success': True, 'fournisseur': {'id': fournisseur.id, 'libelle': fournisseur.libelle, 'email': fournisseur.email, 'telephone': fournisseur.telephone, 'adresse': fournisseur.adresse}}, status=201)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt
def update_fournisseur(request, pk):
    if request.method not in ['POST', 'PUT']:
        return HttpResponseNotAllowed(['POST', 'PUT'])
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    try:
        data = json.loads(request.body)
        form = FournisseurForm(data, instance=fournisseur)
        if form.is_valid():
            fournisseur = form.save()
            return JsonResponse({'success': True, 'fournisseur': {'id': fournisseur.id, 'libelle': fournisseur.libelle, 'email': fournisseur.email, 'telephone': fournisseur.telephone, 'adresse': fournisseur.adresse}})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt
@require_POST
def delete_fournisseur(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    try:
        fournisseur.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Client Views --- (Placeholder - Implement similarly to Produit/Fournisseur)
# Note: Uses the custom 'Client' model from API.models

@require_GET
def list_clients(request):
    # Use the custom Client model
    clients = Client.objects.filter(is_staff=False, is_superuser=False) # Exclude admin/staff users if needed
    data = [{'id': c.id, 'nom': c.nom, 'prenom': c.prenom, 'email': c.email, 'telephone': c.telephone, 'adresse': c.adresse} for c in clients]
    return JsonResponse({'clients': data})

@csrf_exempt
@require_POST
def add_client(request):
    try:
        data = json.loads(request.body)
        # Use a specific form for client creation if needed (e.g., ClientCreationForm)
        form = ClientForm(data)
        if form.is_valid():
            # Manually handle password setting if ClientForm doesn't
            client = form.save(commit=False)
            password = data.get('password') # Ensure password is sent from frontend
            if password:
                client.set_password(password)
            client.save()
            # Don't return password hash
            return JsonResponse({'success': True, 'client': {'id': client.id, 'nom': client.nom, 'prenom': client.prenom, 'email': client.email, 'telephone': client.telephone, 'adresse': client.adresse}}, status=201)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt
def update_client(request, pk):
    if request.method not in ['POST', 'PUT']:
        return HttpResponseNotAllowed(['POST', 'PUT'])
    client = get_object_or_404(Client, pk=pk)
    try:
        data = json.loads(request.body)
        # Exclude password from direct update via form unless specifically handled
        form = ClientForm(data, instance=client)
        if form.is_valid():
            client = form.save()
            # Handle password change separately if needed
            # password = data.get('password')
            # if password:
            #     client.set_password(password)
            #     client.save()
            return JsonResponse({'success': True, 'client': {'id': client.id, 'nom': client.nom, 'prenom': client.prenom, 'email': client.email, 'telephone': client.telephone, 'adresse': client.adresse}})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@csrf_exempt
@require_POST
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    try:
        client.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# --- Dashboard/Page Views --- (Keep existing TemplateViews for initial page load)
# The actual data loading will happen via AJAX calls to the list_* views above.

# Example (if needed, but URLs already point to TemplateView):
# def admin_dashboard(request):
#     return render(request, 'frontoffice/master_page.html')

# def admin_produits_page(request):
#     return render(request, 'frontoffice/page/produit.html')

# def admin_clients_page(request):
#     return render(request, 'frontoffice/page/client.html')

# def admin_fournisseurs_page(request):
#     return render(request, 'frontoffice/page/fournisseur.html')

# def admin_achats_page(request):
#     return render(request, 'frontoffice/page/achat.html')

# def admin_statistiques_page(request):
#     return render(request, 'frontoffice/page/statistiques.html')


