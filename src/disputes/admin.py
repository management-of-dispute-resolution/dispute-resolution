from django.contrib import admin

from .models import Comment, Dispute

admin.site.register(Dispute)
admin.site.register(Comment)
