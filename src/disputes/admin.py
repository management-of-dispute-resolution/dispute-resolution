from django.contrib import admin

from .models import Comment, Dispute, FileDispute


class DisputeAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Dispute model.

    Displays Russian statuses in the admin panel.
    Overrides the formfield_for_choice_field method
    to customize the choices for the status field.
    """

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Customize the choices for the status field to display Russian statuses.

        Args:
            db_field: The field for which to customize choices.
            request: The current request.
            **kwargs: Additional keyword arguments.

        Returns:
            The modified field with customized choices.
        """
        if db_field.name == "status":
            kwargs['choices'] = [
                ('started', 'Решается'),
                ('closed', 'Решено'),
                ('not_started', 'Не рассмотрено')
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(Dispute, DisputeAdmin)
admin.site.register(Comment)
admin.site.register(FileDispute)
