from django.contrib import admin
from .models import Customer,Seller,Login_Details
from .models import CustomUser, SellerEditProfile, Society, IFSCCode,CattleType,Breed,Cattle,Insurance,Vaccination,ContactMessage,CustomerEditProfile,Veterinarian,VetEditProfile,DeliveryBoy,Delivery


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Login_Details)
admin.site.register(SellerEditProfile)
admin.site.register(CustomerEditProfile)
admin.site.register(Society)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(IFSCCode)
admin.site.register(CattleType)
admin.site.register(Breed)
admin.site.register(Cattle)
admin.site.register(Vaccination)
admin.site.register(Insurance)
admin.site.register(ContactMessage)
admin.site.register(Veterinarian)
admin.site.register(VetEditProfile)
admin.site.register(DeliveryBoy)
admin.site.register(Delivery)
