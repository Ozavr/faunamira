from django.contrib import admin
from pages.animal.models import KindAnimal, KindAnimalAttr, AnimalAttr


class KindAnimalAttrInline(admin.TabularInline):
    model = KindAnimalAttr
    fields = ('attr',)


class KindAnimalAdmin(admin.ModelAdmin):
    inlines = [KindAnimalAttrInline,]
    fields = ('kind',)
    list_display = ['kind',]
    search_fields = ['kind']


admin.site.register(KindAnimal, KindAnimalAdmin)
admin.site.register(AnimalAttr)

