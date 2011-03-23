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
admin.site.register(FacultyTable)
admin.site.register(DoeTable)
admin.site.register(SummaryTable)
admin.site.register(AccredTable)
admin.site.register(HonorTable)
admin.site.register(PositionTable)
admin.site.register(GrantTable)
admin.site.register(InvestTable)
admin.site.register(CourseTable)
admin.site.register(GradTable)
