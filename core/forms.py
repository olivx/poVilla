from django import forms
from .models import Mailbag, PO, Request, Disciplina, Local
from django.core.exceptions import ValidationError
import datetime


class MailbagModelForm(forms.ModelForm): 

    class Meta: 
        model = Mailbag
        fields = ('alias', 'local', 'entrega')


    def clean_alias(self):
        alias = self.cleaned_data.get('alias')
        if not alias:
            return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M') 
        return alias

    def clean_local(self):
        local = self.cleaned_data.get('local')
        if not local:
            raise ValidationError('Campo não pode estar vazio.', code='local_empty')


class RequestModelForm(forms.ModelForm): 
    
    class Meta:
        model = Request
        fields = ('__all__')

class DisciplinaModelForm(forms.ModelForm): 
    
    class Meta:
        model = Disciplina
        fields = ('__all__')

class LocalModelForm(forms.ModelForm): 
    
    class Meta:
        model = Local
        fields = ('__all__')

class POModelForm(forms.ModelForm):
    NO_OPTION = 0
    COPY_PB = 1
    COPY_COLOR = 2
    AMPLIFY_A3 = 3
    PRE_IMPRESS = 4
    FRENTE_VERSO = 5
    GRAMPO = 6
    FUROS_4 = 7
    FUROS_2 = 8
    ENCADERNACAO = 9
    PLASTIFICACAO = 10

    copy_option = (
        (NO_OPTION , 'Não relacionado'),
        (COPY_PB , 'copias em PB'),
        (COPY_COLOR ,'copias coloridas'),
        (AMPLIFY_A3, 'ampliar para A3'),
        (PRE_IMPRESS, 'pre impresso'),
        (FRENTE_VERSO, 'frente e verso' ),
        (GRAMPO, 'Grampo'),
        (FUROS_4, '4 furios'),
        (FUROS_2, '2 furos'),
        (ENCADERNACAO, 'encadernação'),
        (PLASTIFICACAO, 'plastificação'),
    )
    copy_option = forms.MultipleChoiceField(
        label="OPÇÕES DE COPIAS", choices=copy_option, widget=forms.CheckboxSelectMultiple(), 
    )
    
    class Meta:
        model = PO
        exclude = ('mailbag', 'local')


    def clean_po(self):
        po = self.cleaned_data.get('po')
        if po is None: 
            raise ValidationError('Numero da PO não pode estar vazia.', code='po_empty')
        return po