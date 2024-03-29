from django.contrib import admin
from .models import CustomUser, Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)



class VideoAdmin(ImportExportModelAdmin):
    pass
class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

admin.site.register(Video, VideoAdmin)



