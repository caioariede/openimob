from contact_form.forms import ContactForm as BaseContactForm


class ContactForm(BaseContactForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = 'Nome'
        self.fields['email'].label = 'Email'
        self.fields['body'].label = 'Mensagem'
        self.fields['body'].help_text =\
            'Deixe sua mensagem e nós retornaremos o quanto antes.'
