from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from ..models import Mailbag, Local
from ..forms import MailbagModelForm
from faker import Faker
from django.contrib import messages
from core.utils import paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q


def mailbag_list(request): 
    search = request.GET.get('search')
    if search is not None:
        list_objects = Mailbag.objects.filter(
            Q(alias__icontains=search) |
            Q(local__name__icontains=search)
        )
    else:
        list_objects = Mailbag.objects.all()

    context = {
        'list_objects': list_objects
    }
    return render(request, 'mailbag/mailbag-list.html', context)


# @login_required
# @client_user_denied
def mailbag_create(request):
    tempate_name = 'mailbag/mailbag-create.html'
    message = 'Malote criado com sucesso'

    fake_alias = Faker('pt_BR').name()
    if request.method == 'POST':
        mailbag_form = MailbagModelForm(request.POST)
        if mailbag_form.is_valid():
            local = get_object_or_404(Local, pk=request.POST.get('local'))
            object = mailbag_form.save(commit=False)
            object.user =request.user
            object.local =local
            object.save() 
            messages.success(request, message)
            return redirect('core:po-add', mailbag_pk=object.id)
    else: 
        mailbag_form = MailbagModelForm(instance=Mailbag(alias=fake_alias))
      

    context = {
        'mailbag_form': mailbag_form,
    }
    return render(request, tempate_name, context)


def mailbag_details(request, pk):
    tempate_name = 'mailbag/mailbag-detail.html'
    message = 'Malote criado com sucesso'
    
    mailbag = get_object_or_404(Mailbag, pk=pk)
    
    mailbag_form = MailbagModelForm(request.POST or None, instance=mailbag)
    if request.method == 'POST':
        if mailbag_form.is_valid():
            mailbag_form.save()
            messages.success(request, message)
            return redirect('core:mailbag-list')
        else:
            messages.error(request, f'formulario não é valido {mailbag_form.errors.items}')

    
    context = {
        'mailbag_form': mailbag_form,
    }
    return render(request, tempate_name, context)


def mailbag_delete(request, pk):
    data = {}
    template = 'mailbag/modal-delete.html'
    template_success = 'mailbag/mailbag-table.html'

    mailbag = get_object_or_404(Mailbag, pk=pk)
    if request.method == 'POST':
        data['is_form_valid'] = True
        message = f'Malote: {mailbag} \nDeletado com sucesso definitivamente.\n\n'  
        messages.error(request, message)

        data['message'] = render_to_string('messages.html', {}, request=request)
        Mailbag.objects.filter(pk=pk).delete()
        list_objects = Mailbag.objects.filter()

        data['html_table'] = render_to_string(
            template_success, {
                'list_objects':  list_objects
            }, request=request
        )


    else:
        form_mailbag = MailbagModelForm(instance=mailbag)
        data['disable_all'] = True
        data['html_form'] = render_to_string(
            template, {
                'form_mailbag': form_mailbag
            },request=request
        )

    return JsonResponse(data)