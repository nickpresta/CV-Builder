from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from cv.models import *

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

# This adds the UserProfile to the User admin page
admin.site.register(User, UserProfileAdmin)
admin.site.register(DistributionOfEffort)
admin.site.register(Summary)

