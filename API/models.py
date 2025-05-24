

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

import json

from django.utils.formats import localize
# Create your models here.

class Administrateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    def __str__(self):
        return '{} {} {}'.format(self.nom, self.prenom, self.login)




"""
class Fournisseur(models.Model):
    libelle = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)

    def __str__(self):
        return '{} by {}'.format(self.libele, self.email)
"""

#####################
#    Fournisseurs  #
#####################
class Fournisseur(models.Model):
    libelle = models.CharField(max_length=50)
    telephone = models.CharField("Téléphone", max_length=20)
    email = models.EmailField("E-Mail", blank=True)
    adresse = models.CharField(max_length=200)

    class Meta:
        ordering = ["libelle",]

    def __str__(self):
        # return json.dumps(self.__dict__)
         return '{} {} {} {}'.format(self.libelle, self.telephone, self.email, self.adresse)


#####################
#    Produits       #
#####################
class Produit(models.Model):
    reference = models.CharField(unique=True,max_length=50)
    designation = models.CharField(max_length=50)
    prixU = models.DecimalField(max_digits=8, decimal_places=2)
    quantite = models.IntegerField()
    alert_quantite = models.PositiveIntegerField(
        "Alert Quantite",
        help_text="Seuil pour la notification de stock faible.")
    fournisseur = models.ForeignKey(Fournisseur,on_delete=models.CASCADE)
    # fournisseur = models.OneToOneField(Fournisseur,on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {} {}'.format(self.reference, self.designation, self.quantite, self.fournisseur)

    # Add this new method to check alert status
    def is_below_alert_level(self):
        """Checks if the current quantity is at or below the alert level."""
        return self.quantite <= self.alert_quantite


##this is the client
class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        client = self.model(email=email, **extra_fields)
        client.set_password(password)
        client.save()
        return client

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Client(AbstractBaseUser, PermissionsMixin):
    # Add related_name to resolve clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="api_client_groups",  # Unique related_name
        related_query_name="api_client",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        help_text=("Specific permissions for this user."),
        related_name="api_client_user_permissions",  # Unique related_name
        related_query_name="api_client",
    )

    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    produits = models.ManyToManyField(Produit, through='Achat', blank=True)

    # Required fields for custom user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = ClientManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom


# Create your models here.
class Superviseur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)

    class Meta:
        db_table = 'api_superviseur'  # To match your naming convention

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# class achat
class Achat(models.Model):
    date_Achat = models.DateField(default=timezone.now)
    quantite = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_Achat} - {self.quantite} units"

    class Meta:
        ordering = ['-date_Achat']