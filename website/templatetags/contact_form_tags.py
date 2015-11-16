from django.template import Library

from ..forms import ContactForm


register = Library()


@register.assignment_tag(takes_context=True)
def get_contact_form(context):
    return ContactForm(request=context.get('request'))
