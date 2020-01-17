from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r


class Timestamp(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Mailbag(Timestamp):
    MANHA_FRIST_HOUR = 1
    MANHA_SECOND_HOUR = 2
    TARDE_FRIST_HOUR = 3
    TARDE_SECOND_HOUR = 4

    TIME_MAILBAG = (
        (MANHA_FRIST_HOUR, 'manhã 08:00'),
        (MANHA_SECOND_HOUR, 'tarde 11:00'),
        (TARDE_FRIST_HOUR, 'manhã 14:00'),
        (TARDE_SECOND_HOUR, 'manhã 16:00'),
    )

    alias = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.ForeignKey('Local',null=True, blank=True, on_delete=models.CASCADE)
    entrega = models.IntegerField(choices=TIME_MAILBAG, default=MANHA_FRIST_HOUR)


    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Malote'
        verbose_name_plural = 'Malotes'

    objects = models.Manager()

    
    def __str__(self):
        if not self.local:
            return f"{'-'.join(self.alias.split(' '))}-{'-'.join(self.get_entrega_display().split(' '))}"
        return f"{'-'.join(self.alias.split(' '))}-{'-'.join(self.local.name.split(' '))}-{'-'.join(self.get_entrega_display().split(' '))}"
    
    def get_absolute_url(self):
        return r('core:mailbag-details', pk=self.pk)


class Local(models.Model):
    name = models.CharField(max_length=200)

    objects = models.Manager()


    class Meta:
        verbose_name_plural = 'Locais'

    def __str__(self):
        return f'{self.name}'


class Servico(Timestamp): 

    nome = models.CharField(max_length=200)
    price= models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        ordering = ('-create_at',)
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.nome
    

class Disciplina(models.Model):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    GRADE_CHOICES = (
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
        (D, 'D'),
        (E, 'E'),
    )

    name = models.CharField(max_length=200)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.grade}'

class Request(models.Model):

    name = models.CharField("Requisitante",max_length=200)
    grade = models.CharField("Grade escolar",max_length=10)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.grade}'

class PO(Timestamp):
    ALUNOS = 1
    PROFESSOR = 2
    CARTA  = 3
    TYPE_CHOICES = (
        (ALUNOS, 'uso dos alunos'),
        (PROFESSOR, 'uso dos professores'),
        (CARTA, 'carta'),
    )

    SEG_DIGITAR = 1
    SEG_ESCANEAR = 2
    SEG_CHOICES = (
        (SEG_DIGITAR, 'DIGITAR'),
        (SEG_ESCANEAR, 'ESCANEAR'),
    )

    NOT_REVISION = 0
    REVISION_BEFORE = 1
    REVISION_VIST = 2
    REVISION_CHOICES = (
        (NOT_REVISION, 'sem revisão'),
        (REVISION_BEFORE, 'antes de ser cherocado'),
        (REVISION_VIST, 'visto da revisão'),
    )

    xerox_option = (
        (1, 'NÃO FAZER FRENTE E VERSO'),
        (2, 'COLAR NO CADERNO'),
        (3, 'CORTAR'),
    )

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

    po = models.CharField("Numero PO", max_length=20, null=True, blank=True)
    type = models.IntegerField("TIPO DO MATERIAL USADO",choices=TYPE_CHOICES)

    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    diciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True, blank=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)
    mailbag = models.ForeignKey(Mailbag, on_delete=models.CASCADE, related_name='mailbags', null=True, blank=True)

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    servico_qdt = models.IntegerField("Quantidade", default=0)


    seg_choices = models.IntegerField("INFO PARA O SEG",choices=SEG_CHOICES, null=True, blank=True)
    date_period = models.DateField()
    date_to_finish = models.DateField()
    subject = models.TextField("ASSUNTO",null=True, blank=True)
    revision = models.IntegerField("REVISÃO",choices=REVISION_CHOICES, default=NOT_REVISION)
    comment_seg = models.TextField("OBS PARA  SEG",null=True, blank=True)
    xerox_choices = models.CharField("NUM COPIAS ORIGINAIS",max_length=20, null=True, blank=True)
    copy_number = models.IntegerField("NUM DE COPIAS", null=True, blank=True)
    active = models.BooleanField(default=True)
    copy_original = models.IntegerField("NUM DE COPIAS ORIGINAIS", null=True, blank=True)
    quant_grampos = models.IntegerField(default=0, null=True, blank=True)
    pre_impress_comment = models.TextField(null=True, blank=True)
    copy_choices = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField("OBS PARA COPIADORA", null=True, blank=True)

    class Meta:
        ordering = ('-create_at',)

    objects = models.Manager()

    def __str__(self):
        return f'{self.po}'








