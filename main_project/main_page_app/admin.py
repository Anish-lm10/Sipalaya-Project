from django.contrib import admin
from .models import *


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username"]
    search_fields = ["username", "email"]


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Courses)
admin.site.register(SpecialOffers)
admin.site.register(Testimonial)
admin.site.register(Announcement)
admin.site.register(BlogPost)
admin.site.register(Payment)
