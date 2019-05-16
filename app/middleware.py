from django.utils.deprecation import MiddlewareMixin


class Middleware(MiddlewareMixin):
    def process_request(self, request):
        request.modalAlerts = []
        if 'modalAlerts' in request.session.keys():
            request.modalAlerts.extend(request.session.get('modalAlerts', []))
        request.session['modalAlerts'] = []

        request.modalAlertSize = 'small'
        if 'modalAlertSize' in request.session.keys():
            request.modalAlertSize = request.session.get('modalAlertSize')

        request.flash_alerts = []
        if 'flash_alerts' in request.session.keys():
            request.flash_alerts.extend(request.session.get('flash_alerts', []))
        request.session['flash_alerts'] = []

        # to add modal alert >> request.modalAlerts.append({
        #     'title': 'some title',
        #     'msg': "Some user message.",
        #     'type': "success"})
        # types >> ['success', 'error', 'info', 'empty']

        return None

    def process_response(self, request, response):
        if getattr(request, 'session', None) is not None:
            if 'modalAlerts' in request.session.keys() and len(request.session['modalAlerts']) < 1:
                del request.session['modalAlerts']

            if 'flash_alerts' in request.session.keys() and len(request.session['flash_alerts']) < 1:
                del request.session['flash_alerts']

            if 'next' in request.session.keys() and request.session['next'] == '/':
                del request.session['next']

        return response
