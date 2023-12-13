from django.contrib import admin

from disputes.models import Comment, Dispute, FileComment, FileDispute


class DisputeAdmin(admin.ModelAdmin):
    """
    A class that displays the interface of the Dispute in the admin panel.

    Contains a list_display, search_fields, list_filter.
    """

    list_display = ['id', 'creator', 'description', 'status']
    search_fields = ['creator']
    list_filter = ['created_at', 'creator', 'status']


class CommentAdmin(admin.ModelAdmin):
    """
    A class that displays the interface of the Comment in the admin panel.

    Contains a list_display, search_fields, list_filter.
    """

    list_display = ['id', 'sender', 'content', 'dispute']
    search_fields = ['sender']
    list_filter = ['created_at', 'sender', 'dispute']


admin.site.register(Dispute, DisputeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FileDispute)
admin.site.register(FileComment)
