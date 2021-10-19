from django.apps import AppConfig
from common.logger_format_and_file_setup import initialize_logger


class AuthManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_management'

    def ready(self):
        initialize_logger()
