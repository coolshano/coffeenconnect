from django.forms.widgets import ClearableFileInput

class CleanFileInput(ClearableFileInput):
    template_name = "widgets/clean_file_input.html"
