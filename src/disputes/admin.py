from django.contrib import admin

from .models import Comment, Dispute, FileDispute

admin.site.register(Dispute)
admin.site.register(Comment)
admin.site.register(FileDispute)
