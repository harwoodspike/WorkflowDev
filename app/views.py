# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
import json

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import LegalAgreementForm
from app.models import WorkflowWizard
from app.utils import get_form


# Create your views here.
def redirectToVue(request, *args, **kwargs):
    return render(request, 'vue.html')


def dynamic_files(request, ftype):
    if ftype == 'js':
        content_type = 'text/javascript'

    elif ftype == 'css':
        content_type = 'text/css'

    return render(request, 'dynamic.' + ftype, {}, content_type=content_type)


def workflow(request, wiz_id, step=1):
    context = {'setup_wiz_page': True, 'no_sidebar': False}
    setup_wizards = WorkflowWizard.objects.filter(id=wiz_id)
    setup_wiz = setup_wizards.last()

    # Redirect to dashboard if no setup wizards
    if setup_wiz is None:
        return HttpResponseRedirect(reverse('dashboard'))

    else:
        context['page_title'] = setup_wiz.name
        context['workflow_wiz'] = setup_wiz
        context['step_num'] = step = int(step)
        context['steps'] = wiz_steps = setup_wiz.steps.filter(active=True)
        context['step_count'] = wiz_steps.count()
        context['nav_show_steps'] = nav_show_steps = 5
        context['nav_start'] = 0
        context['editable_step'] = True

        if (step % nav_show_steps) != 0:
            context['nav_start'] = math.floor(step / nav_show_steps)

        elif math.floor(step / nav_show_steps) > 0:
            context['nav_start'] = math.floor(step / nav_show_steps) - 1

        odl = None

        if context['step_count'] >= step:
            context['current_step'] = current_step = wiz_steps[step - 1]
            context['next_url'] = None

        elif step > context['step_count']:
            current_step = None
            return HttpResponseRedirect(reverse('dashboard'))

        if current_step.agreement is not None:
            # load_data = '%s:%s' % (str(setup_wiz.object_type), content_object.id)
            load_data = ''
            context['form'] = LegalAgreementForm(agreements=[(current_step.agreement, load_data)])

            if context['form'] is not None:
                if request.method == 'POST':
                    context['form'] = LegalAgreementForm(
                        agreements=[(current_step.agreement, load_data)],
                        data=request.POST
                    )
                    if context['form'].is_valid():
                        msg = 'Agreement signed successfully'
                        request.session['flash_alerts'].append({'msg': msg, 'type': 'success'})
                    return HttpResponseRedirect(request.POST.get('next_url', reverse('dashboard')))

        elif current_step.form is not None:
            form_context = {}
            context['form'] = get_form(current_step.form)

            if context.get('form') is not None:
                if request.method == 'POST':
                    # if hasattr(context['form'], 'get_instance'):
                    #     form_context['instance'] = context['form'].get_instance(odl)
                    form_context.update({'data': request.POST, 'files': request.FILES})
                    context['form'] = context['form'](**form_context)

                    if not context.get('editable_step', False):
                        return HttpResponseRedirect(
                            request.POST.get('next_url', reverse('dashboard')))

                    elif context['form'].is_valid():
                        form_save_context = {'request': request}
                        if request.FILES is not None and len(request.FILES) > 0:
                            form_save_context['odl'] = odl

                        return context['form'].save(**form_save_context)
                else:
                    initial_kwargs = {'request': request}

                    if hasattr(context['form'], 'get_initial'):
                        initial = context['form'].get_initial(**initial_kwargs)

                    else:
                        initial = {}

                    if 'instance' in initial:
                        form_context['instance'] = initial.pop('instance')

                    if 'odl' not in initial:
                        initial['odl'] = odl

                    form_context['initial'] = initial
                    context['form'] = context['form'](**form_context)
    return render(request, 'workflow.html', context)
