from django.contrib import admin

from refdata.models import Banner, AltMenu, SocialLink

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'status',]
    list_editable = ['status']


class AltMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order']
    list_editable = ['order']
    fields = ('title', 'url', 'order')


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']


admin.site.register(Banner, BannerAdmin)
admin.site.register(AltMenu, AltMenuAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
