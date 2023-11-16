from django.contrib import admin

from .models import Comment, Dispute, FileComment, FileDispute

class DisputeAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'description', 'status', 'count_comments_for_dispute']
    search_fields = ['creator']
    list_filter = ['created_at', 'creator', 'status']

    def count_comments_for_dispute(self, obj):
        return obj.comments.all().count()

    count_comments_for_dispute.short_description = 'Количество комментариев к спору'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'content','dispute']
    search_fields = ['sender']
    list_filter = ['created_at', 'sender', 'dispute']


admin.site.register(Dispute, DisputeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FileDispute)
admin.site.register(FileComment)

