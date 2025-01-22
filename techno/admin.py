from .models import Attributes, Visitor, Profile, Currency
from .models import FilterSettings
from .models import Category, Brand, Product, Powerr, BlockType, SplitSystem
from django.contrib import admin
from django.urls import path



@admin.action(description="Перевести в черновик")
def mark_as_draft(modeladmin, request, queryset):
    queryset.update(draft=True)

@admin.action(description="Убрать из черновика")
def unmark_as_draft(modeladmin, request, queryset):
    queryset.update(draft=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'brand', 'category', 'series', 'type', 'price', 'currency', 'availability', 'Powerr', 'BlockType', 'SplitSystem', 'invertor', 'relevance',
                    'mark', 'date_of_establishment', 'number_of_views', 'draft', 'url', 'id', 'image', 'noise', 'refrigerant', 'compressor_type', 'split_type']
    list_filter = ['brand', 'series', 'category', 'availability', 'number_of_views', 'invertor', 'draft']
    prepopulated_fields = {'url': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'brand', 'category', 'series', 'type', 'price', 'currency', 'availability', 'Powerr', 'BlockType', 'SplitSystem', 'invertor', 'relevance',
                       'mark', 'date_of_establishment', 'number_of_views', 'draft',
                       'url', 'image', 'noise', 'refrigerant', 'compressor_type', 'split_type')
        }),
    )
    actions = [mark_as_draft, unmark_as_draft]
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-filters/', self.clear_filters, name='clear-filters'),
        ]
        return custom_urls + urls

    def clear_filters(self, request):
        # Здесь мы очищаем фильтры, например, удаляя все настройки фильтров
        FilterSettings.objects.all().delete()
        self.message_user(request, "Все фильтры были удалены.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




class PowerAdmin(admin.ModelAdmin):
    list_display = ('NamePower',)



class BlockTypeAdmin(admin.ModelAdmin):
    list_display = ('BlockType',)


class SplitSystemAdmin(admin.ModelAdmin):
    list_display = ('SplitSystem',)  # Имя поля из модели SplitSystem







@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_filter = ['draft']
    prepopulated_fields = {'url': ('name',)}
    actions = [mark_as_draft, unmark_as_draft]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image', 'url', 'id', 'draft', 'sort_order']
    list_filter = ['category', 'draft']
    prepopulated_fields = {'url': ('name',)}
    actions = [mark_as_draft, unmark_as_draft]







@admin.register(Attributes)
class AttributesAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'product']
    list_filter = ['product']
    

admin.site.register(Visitor)

admin.site.register(Profile)

admin.site.register(Currency)

admin.site.register(SplitSystem, SplitSystemAdmin)

admin.site.register(BlockType, BlockTypeAdmin)

admin.site.register(Powerr, PowerAdmin)

admin.site.register(FilterSettings)