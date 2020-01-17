from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from ..models import Mailbag, Local, Request, Disciplina
from ..forms import MailbagModelForm, POModelForm, RequestModelForm, LocalModelForm, PO
from django.contrib import messages
from core.utils import paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q


def pod_list(request, mailbag_pk):
    template = 'po/list-po.html'
    mailbag = get_object_or_404(Mailbag, pk=mailbag_pk)

    search = request.GET.get('search')
    if search is not None:
        list_objects = PO.objects.filter(
            Q(po__icontains=search) |
            Q(servico__nome__icontains=search) | 
            Q(request__name__icontains=search) | 
            Q(request__grade__icontains=search) , 
            mailbag__pk=mailbag_pk

        )
    else:
        list_objects =PO.objects.filter(mailbag__pk=mailbag_pk)

    context = {
        'mailbag': mailbag,
        'list_objects': list_objects,
    }
    
    return render(request, template, context) 


def pod_add(request, mailbag_pk): 
    template = 'po/add-po.html'
    mailbag = get_object_or_404(Mailbag, pk=mailbag_pk)
    local_list =  Local.objects.all() 
    po_form =  POModelForm(request.POST or None)

    if request.method == 'POST':
        if po_form.is_valid():
            po = po_form.save(commit=False)
            po.user = request.user
            po.mailbag = mailbag
            # import ipdb; ipdb.set_trace()

            # print(po.local)
            po.local = Local.objects.filter(name=po.local).first()
            po.diciplina = Disciplina.objects.filter(pk=po.diciplina).first()
            po.request = Request.objects.filter(pk=po.request.pk).first()

            po.save()
            messages.success(request, f'PO {po.po} add com sucesso.')
            
            return redirect('core:po-add', mailbag_pk=mailbag_pk)
        else:
            messages.error(request, 'alguns campos fora enviado com erro, por favor verifique os capos abaixo')

    context = {
        'mailbag': mailbag,
        'po_form': po_form,
        'local_list': local_list,
    }
    
    return render(request, template, context) 


def pod_edit(request, pk, mailbag_pk): 
    template = 'po/add-po.html'
    po = get_object_or_404(PO, pk=pk)
    local_list =  Local.objects.all() 
    po_form =  POModelForm(request.POST or None, instance=po)

    if request.method == 'POST':
        if po_form.is_valid():
            po = po_form.save(commit=False)
            po.user = request.user
            po.local = Local.objects.filter(name=po.local).first()
            po.diciplina = Disciplina.objects.filter(pk=po.diciplina).first()
            po.request = Request.objects.filter(pk=po.request.pk).first()

            po.save()
            messages.success(request, f'PO {po.po} add com sucesso.')
            
            return redirect('core:po-list', mailbag_pk=po.mailbag.pk)
        else:
            messages.error(request, 'alguns campos fora enviado com erro, por favor verifique os capos abaixo')

    context = {
        'po_form': po_form,
        'local_list': local_list,
    }
    
    return render(request, template, context) 

def pod_delete(request, pk,): 
    template = 'po/add-list.html'
    po = get_object_or_404(PO, pk=pk)
    po_form =  POModelForm(request.POST or None, instance=po)

    if request.method == 'POST':
        if po_form.is_valid():
            PO.objects.filter(pk=pk).delete()
            messages.success(request, f'PO deletada {po.po} de ID {po.id}.')
            
            return redirect('core:po-list', mailbag_pk=po.mailbag.pk)
        else:
            messages.error(request, 'alguns campos fora enviado com erro, por favor verifique os capos abaixo')

    object_list  =  PO.objects.filter(pk=pk)
    context = {
        'po_form': po_form,
        "object_list":  object_list
    }
    return render(request, template, context) 


