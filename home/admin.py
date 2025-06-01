from django.contrib import admin
from home.models import Contact
from home.models import ImageUpload
from home.models import ChatMessage
# Register your models here.

admin.site.register(Contact)
admin.site.register(ImageUpload)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "user_message", "bot_response", "timestamp", "needs_admin")
    list_filter = ("needs_admin",)
    actions = ["mark_as_resolved"]

    def mark_as_resolved(self, request, queryset):
        queryset.update(needs_admin=False)
        self.message_user(request, "Selected messages marked as resolved.")

    mark_as_resolved.short_description = "Mark selected messages as resolved"
    