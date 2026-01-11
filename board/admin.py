from django.contrib import admin
from .models import Category, Advertisement, Response, Newsletter
from .services.newsletter import send_newsletter

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Response)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'is_sent')
    actions = ['send_newsletter_action']

    def send_newsletter_action(self, request, queryset):
        for newsletter in queryset:
            if not newsletter.is_sent:
                send_newsletter(newsletter)

    send_newsletter_action.short_description = 'Отправить рассылку'
