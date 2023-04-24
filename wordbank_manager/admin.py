from django.contrib import admin
from .models import StandardPrompt, PromptCategory, UserPrompt

@admin.register(StandardPrompt)
class StandardPromptAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'hashtags')

@admin.register(PromptCategory)
class PromptCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

@admin.register(UserPrompt)
class UserPromptAdmin(admin.ModelAdmin):
    list_display = ('text', 'hashtags')
    filter_horizontal = ('category',)