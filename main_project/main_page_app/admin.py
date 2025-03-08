from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Courses)
admin.site.register(SpecialOffers)
admin.site.register(Testimonial)
admin.site.register(Announcement)
admin.site.register(BlogPost)
