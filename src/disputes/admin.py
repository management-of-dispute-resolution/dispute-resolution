from django.contrib import admin

from .models import Comment, CommentDispute, Dispute

admin.site.register(Dispute)
admin.site.register(Comment)
admin.site.register(CommentDispute)
