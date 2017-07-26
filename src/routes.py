import os
from views import Home

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_routes(app):
    # app.router.add_get('/', index, name='home')
    app.router.add_route('*', '/', Home, name='home')
    # app.router.add_static('/static/',
    #                       path=str(project_root + '/static'),
    #                       name='static')