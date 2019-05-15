try:
    from urlparse import urlparse  # Python 2
except ImportError:
    from urllib.parse import urlparse

import requests

from django import template
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.six import string_types
from django.utils.text import slugify

register = template.Library()


@register.filter
def has_app(user, app):
    try:
        if user.company.billing is not None:
            if isinstance(app, string_types):
                return user.company.billing.internal_app.filter(name=app).exists()
            elif isinstance(app, dict):
                return user.company.billing.internal_app.filter(name=app.get('name')).exists()
            else:
                return user.company.billing.internal_app.filter(id=app.id).exists()
        else:
            return False
    except Exception:
        return False


@register.filter
def has_app_link(user, link):
    try:
        if user.company.billing is not None:
            if isinstance(link, string_types):
                return user.company.billing.internal_app.filter(link=link).exists()
            elif isinstance(link, dict):
                return user.company.billing.internal_app.filter(link=link.get('link')).exists()
            else:
                return user.company.billing.internal_app.filter(id=link.id).exists()
        else:
            return False
    except Exception:
        return False


@register.filter
def has_live_apps(request):
    return request.user.company.app_access.filter(is_public=True, companyapp__visible=True).exists()


@register.filter
def has_dev_apps(request):
    return request.user.company.app_access.filter(is_public=False, companyapp__visible=True).exists()


@register.filter
def get_app_html(app, request):
    add_modal = False
    html = []

    html.append('<div class="medium-12 large-8 columns tile-margin end">')
    html.append('<div class="dashboard-tile">')

    html.append('<div class="row collapse coming-soon-row">')
    if app.coming_soon:
        html.append('<img src="/static/images/platinum.svg" alt="Coming Soon" class="coming-soon">')
    else:
        html.append('&nbsp;')
    html.append('</div>')

    if not request.user.company.app_access.filter(id=app.id, companyapp__visible=True).exists():
        return ''

    if not app.appdomain_set.filter(id=request.domain.id).exists():
        return ''

    app_target = ' target="_blank"' if app.new_tab else ''
    app.name = force_str(app.name)
    app.desc = force_str(app.desc)

    needs_signature = False
    if app.agreement is not None and app.agreement.sign:
        signature = request.user.company.signature_set.filter(legal=app.agreement).last()
        if signature is None or (signature is not None and not signature.verify()):
            needs_signature = True

    if not app.link or not app.is_public:
        html.append('<a href="#" class="app-link app-modal" data-app="{}"></a>'.format(slugify(app.name)))
        add_modal = True

    elif needs_signature and not request.user.has_permission("Manage App"):
        html.append(
            '<a href="{}" class="app-link subscribe-modal" data-legal="{}"></a>'.format(
                app.link,
                reverse('view_agreement', kwargs={'agreement_id': app.agreement.id}),
                app_target
            )
        )
    else:
        html.append('<a href="{}" class="app-link" {}></a>'.format(app.link, app_target))

    html.append('<h2>{}</h2>'.format(app.name))
    html.append('<div class="sub-title">{}</div>'.format(app.sub_title))

    if app.image:
        logosrc = app.image.url
        html.append('<img class="app-image" src="{}" alt="{}">'.format(logosrc, app.name))
    else:
        html.append('<span class="icon-cloud app-image"></span>')

    html.append('<div class="tile-text-bottom">{}</div></div></div>'.format(app.desc))

    if add_modal:
        html.append('<div id="{}-modal" class="reveal-modal small" data-reveal>'.format(slugify(app.name)))
        html.append('<a class="close-reveal-modal">&#215;</a><div>{}</div></div>'.format(app.alert_text))

    return '\n'.join(html)


@register.filter
def get_my_app_html(app, request):
    has_login = 'false'
    html = []

    html.append('<div class="medium-12 large-8 columns tile-margin end">')
    html.append('<div class="dashboard-tile">')

    if not request.user.company.app_access.filter(id=app.id, companyapp__visible=True).exists():
        return ''

    if not app.appdomain_set.filter(id=request.domain.id).exists():
        return ''

    app_target = ' target="_blank"' if app.new_tab else ''
    app.name = force_str(app.name)
    app.desc = force_str(app.desc)

    if not app.link and app.alert_text:
        html.append('<a href="#" class="app-link app-modal" data-app="{}"></a>'.format(slugify(app.name)))

    elif not app.is_public:
        html.append('<a href="#" class="app-link app-modal" data-app="{}"></a>'.format(slugify(app.name)))

    else:
        html.append('<a href="{}" class="app-link app_check" data-app="{}" data-has_login="{}"{}></a>'.format(
            app.link, app.name, has_login, app_target))

    html.append('<h2>{}</h2>'.format(app.name))
    html.append('<div class="sub-title">{}</div>'.format(app.sub_title))

    applogo = {}
    if app.image:
        applogo['src'] = app.image.url
        applogo['show'] = True

    if app.link and 'http' in app.link and not applogo.get('show', False):
        # Check clearbit api
        addr_parts = urlparse(app.link)
        address = 'https://logo.clearbit.com/{}/?size=500'.format(addr_parts.netloc)
        cb_image = requests.get(address)
        if cb_image.status_code == 200:
            applogo['src'] = address
            applogo['show'] = True

    if applogo.get('show', False):
        logosrc = applogo.get('src', '')
        html.append('<img class="app-image" src="{}" alt="{}">'.format(logosrc, app.name))
    else:
        html.append('<span class="icon-cloud app-image"></span>')

    html.append('<div class="tile-text-bottom">{}</div>'.format(app.desc))
    html.append(
        '<div class="editaction" data-id="{}" data-name="{}" data-link="{}" data-desc="{}" ' +
        'data-new_tab="{}" data-sub_title="{}"><span class="icon-gear">' +
        '</span></div></div></div>'.format(
            app.id, app.name, app.link, app.desc, app.new_tab, app.sub_title))

    return '\n'.join(html)


@register.filter
def get_active_apps_html(request):
    html = []
    apps_kwargs = {'is_public': True}
    if request.domain:
        apps_kwargs['appdomain'] = 'localhost'
    app_req = requests.get('/api/app_list/', params=apps_kwargs)
    live_apps = app_req.json()
    for app in live_apps:
        html.append(get_app_html(app, request))

    return '\n'.join(html)


@register.filter
def get_dev_apps_html(request):
    html = []
    apps_kwargs = {'is_public': False}
    if request.domain:
        apps_kwargs['appdomain'] = 'localhost'
    app_req = requests.get('/api/app_list/', params=apps_kwargs)
    dev_apps = app_req.json()
    for app in dev_apps:
        html.append(get_app_html(app, request))

    return ''.join(html)
