from django.contrib.staticfiles.apps import StaticFilesConfig

class CustomStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = [
        'CVS', 
        '.*', 
        '*~'
    ]