from django.contrib import admin
from .models import Vendor

from django import forms
from .models import Vendor
from image_uploader_widget.widgets import ImageUploaderWidget

admin.site.register(Vendor)