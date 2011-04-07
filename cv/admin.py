# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from cv.models import *

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

def export_cv(modeladmin, request, queryset):
    pass

# This adds the UserProfile to the User admin page
admin.site.register(User, UserProfileAdmin)
admin.site.register(DistributionOfEffort)
admin.site.register(Summary)
admin.site.register(Accred)
admin.site.register(Honor)
admin.site.register(PositionHeld)
admin.site.register(PositionPriorTable)
admin.site.register(PositionElsewhereTable)
admin.site.register(GrantTable)
admin.site.register(InvestigatorTable)
admin.site.register(CourseTable)
admin.site.register(GradTable)
