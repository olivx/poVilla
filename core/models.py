from django.db import models
from django.contrib.auth.models import User


class Timestamp(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Mailbag(Timestamp):
    alias = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Malote'
        verbose_name_plural = 'Malotes'


class Local(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'

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

    def __str__(self):
        return f'{self.name} {self.grade}'

class Request(models.Model):

    name = models.CharField(max_length=200)
    grade = models.CharField(max_length=10)

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

    po = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)

    request = models.OneToOneField(Request, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    diciplina = models.OneToOneField('Disciplina', on_delete=models.SET_NULL, null=True, blank=True)
    local = models.OneToOneField('Local', on_delete=models.SET_NULL, null=True, blank=True)
    mailbag = models.ForeignKey('Mailbag', on_delete=models.CASCADE, related_name='mailbags', null=True, blank=True)

    seg_choices = models.IntegerField(choices=SEG_CHOICES, null=True, blank=True)
    date_period = models.DateField()
    date_to_finish = models.DateField()
    subject = models.TextField(null=True, blank=True)
    revision = models.IntegerField(choices=REVISION_CHOICES, default=NOT_REVISION)
    comment_seg = models.TextField(null=True, blank=True)
    xerox_choices = models.CharField(max_length=20, null=True, blank=True)
    copy_number = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    copy_original = models.IntegerField(null=True, blank=True)
    quant_grampos = models.IntegerField(default=0, null=True, blank=True)
    pre_impress_comment = models.TextField(null=True, blank=True)
    copy_choices = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-create_at',)

    def __str__(self):
        return f'{self.po}'








