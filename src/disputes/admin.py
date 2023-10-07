from django.contrib import admin

from .models import Dispute, DisputeParticipants, Message, Attachment

admin.site.register(Dispute)
admin.site.register(DisputeParticipants)
admin.site.register(Message)
admin.site.register(Attachment)
