from django.contrib import admin
from .models import Profile
from .models import Post,Transaction,Wallet



admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Transaction)
admin.site.register(Wallet)

# admin.py