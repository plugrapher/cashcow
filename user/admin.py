from django.contrib import admin
from .models import Profile
from .models import City
from .models import Data,Jobs,Post  



admin.site.register(Jobs)
admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Data)
admin.site.register(Post)
