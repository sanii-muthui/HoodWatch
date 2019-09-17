from django.contrib import admin
from .models import Profile,Neighbourhood,Business,Review,Post,Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Neighbourhood)
admin.site.register(Business)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Comment)
