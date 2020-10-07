from django.db import models
from django.conf import settings
import os
import uuid
from django.utils.deconstruct import deconstructible


"""
    FUNCTIONS
"""
@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("images/item")

"""
    Custom Fields
"""
class CustomEmailField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CustomEmailField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()



""" 
    MODELS
"""
from . import managers
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Keranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jumlah_item = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

class User(AbstractUser):
    """User model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    # first_name = None
    # last_name = None

    # email = CustomEmailField(_('email'), unique=True, max_length=64)
    # sementara email jadi char, untuk mempermudah register/login
    email = models.CharField(_('email'), unique=True, max_length=64)
    first_name = models.CharField(_('nama depan'), max_length=64)
    last_name = models.CharField(_('nama belakang'), max_length=64)
    password = models.CharField(_('password'), max_length=64)

    keranjang = models.ForeignKey(
        Keranjang,
        default=None,
        on_delete=models.CASCADE,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()
 
    def __str__(self):
        if self.first_name == '':
            return self.email
        return self.first_name+' '+self.last_name


# class Profile(models.Model):
#     # Relations
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE,
#         related_name="profile")
#     alamat = models.CharField(max_length=32)
#     # Attributes - Optional
#     # Object Manager
#     objects = managers.ProfileManager()
 
#     # Custom Properties
#     @property
#     def username(self):
#         return self.user.username
 
#     # Methods
 
#     # Meta and String
#     class Meta:
#         verbose_name_plural = "profile"
#         ordering = ("user",)
 
#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile_for_new_user(sender, created, instance, **kwargs):
#     if created:
#         profile = Profile(user=instance)
#         profile.save()

class JenisItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis = models.CharField(max_length=32)

    def __str__(self):
        return self.jenis
    class Meta:
        verbose_name_plural = 'jenis item'

class Kategori(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=32)
    def __str__(self):
        return self.nama_kategori
    class Meta:
        verbose_name_plural = 'kategori'

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_file = models.CharField(max_length=64)
    # img = models.ImageField(upload_to=PathAndRename('images/item'))
    img = models.ImageField(upload_to=path_and_rename)
    # path = models.CharField(max_length=64)
    # tipe = models.CharField(max_length=64)
    # size = models.IntegerField()
    # height = models.IntegerField()
    # width = models.IntegerField()

    def __str__(self):
        return self.nama_file
    class Meta:
        verbose_name_plural = 'gambar'


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis_item = models.ForeignKey(
        JenisItem,
        on_delete=models.CASCADE
    )
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE
    )
    nama_item = models.CharField(max_length=32)
    harga = models.IntegerField()
    deskripsi = models.TextField()
    jumlah_tersedia = models.IntegerField()
    foto = models.ImageField()
    # foto = models.ImageField(upload_to=path_and_rename('images/item'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_item
    
    class Meta:
        verbose_name_plural = 'Item'

class IsiKeranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keranjang = models.ForeignKey(
        Keranjang,
        on_delete=models.CASCADE,
    )
    item=models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MetodePembayaran(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_metode = models.CharField(max_length=32)
    deskripsi = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural='metode pembayaran'

class Alamat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Transaksi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        # Profile,
        on_delete=models.CASCADE
    )
    metode_pembayaran = models.ForeignKey(
        MetodePembayaran,
        on_delete=models.CASCADE
    )
    nama = models.CharField(max_length=64)
    telepon = models.CharField(max_length=64)
    alamat = models.CharField(max_length=64)
    subtotal = models.IntegerField()
    status_pembayaran = models.IntegerField()
    jumlah_item = models.IntegerField(default=0)

    kodepos = models.CharField(max_length=6, null=True)
    id_kota = models.IntegerField(null=True)
    id_provinsi = models.IntegerField(null=True)
    nama_kota = models.CharField(max_length=32, null=True)
    nama_provinsi = models.CharField(max_length=32, null=True)
    service = models.CharField(max_length=32, null=True)

    ongkos_kirim = models.IntegerField(null=True)
    total = models.IntegerField()
    # catatan
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='transaksi'

class DetailTransaksi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaksi = models.ForeignKey(
        Transaksi,
        # Profile,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
