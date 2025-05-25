from django import forms

from API.models import *


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ('reference', 'designation', 'prixU', 'quantite', 'fournisseur')
        widgets = {
            'reference': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ), 'designation': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ), 'prixU': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ), 'quantite': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ), 'fournisseur': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }
class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ('libelle', 'telephone', 'email', 'adresse')



class ClientForm(forms.ModelForm):
    # Add a password field for creation, but make it not required for updates
    # Use PasswordInput widget to hide input
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password.")

    class Meta:
        model = Client
        # Include fields relevant for admin creation/update
        # Exclude password from direct model fields to handle hashing separately
        fields = ("nom", "prenom", "email", "telephone", "adresse", "is_active", "is_staff")
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Override save method if password hashing needs to be handled here
    # However, the view currently handles password setting, which is fine.

