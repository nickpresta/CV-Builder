# -*- coding: utf-8 -*-
import zipfile
from cStringIO import StringIO

from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from cv.models import *
from cv.viewables.actions import export_download

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    actions = ['export_cv']

    def export_cv(self, request, queryset):
        if len(queryset) == 1:
            # Only 1 user
            return export_download(request, True, queryset[0])

        response = HttpResponse(mimetype='application/zip')
        response['Content-Disposition'] = 'filename=cv_export.zip'
        buf = StringIO()
        zip_file = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
        for user in queryset:
            pdf = export_download(request, True, user, True)
            zip_file.writestr("%s_cv.pdf" % user.get_full_name(), pdf.getvalue())
            pdf.close()
        zip_file.close()
        buf.flush()
        return_zip = buf.getvalue()
        buf.close()
        response.write(return_zip)
        return response

    export_cv.short_description = "Export Faculty CV"

# This adds the UserProfile to the User admin page
admin.site.register(User, UserProfileAdmin)
admin.site.register(DistributionOfEffort)
admin.site.register(Summary)
admin.site.register(Accred)
admin.site.register(Honor)
admin.site.register(PositionHeld)
admin.site.register(PositionPrior)
admin.site.register(PositionElsewhere)
admin.site.register(Grant)
admin.site.register(Investigator)
admin.site.register(Course)
admin.site.register(GradTable)
