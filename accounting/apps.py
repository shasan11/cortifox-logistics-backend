from django.apps import AppConfig


class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting'
    verbose_name="General Accounting"
    def ready(self):
        import accounting.signals   