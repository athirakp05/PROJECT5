from django.contrib import admin
from .models import Customer,Seller
from .models import CustomUser, SellerEditProfile, Society, IFSCCode


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(SellerEditProfile)
admin.site.register(Society)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(IFSCCode)
