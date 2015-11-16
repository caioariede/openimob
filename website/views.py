from contact_form.views import ContactFormView as BaseContactFormView

from .forms import ContactForm


class ContactFormView(BaseContactFormView):
    form_class = ContactForm
