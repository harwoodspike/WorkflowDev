def sidebar(request):
    return {'no_sidebar': True}


def app_list(request):
    import requests
    if 'api' not in request.path:
        app_req = requests.get('http://localhost:8000/api/app_list/')
        apps = app_req.json()

        return {
            'my_apps_title': 'My Apps',
            'my_apps': apps.get('myapps', []),
            'app_categories': apps.get('app_categories', [])}
    return {}
