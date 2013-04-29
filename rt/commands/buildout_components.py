from fabric.api import lcd, local
from fabric.utils import warn


COMPONENTS = {'plone': 'https://github.com/RedTurtle/deployments.buildout.plone/archive/master.tar.gz'}


def component(component):
    """clone component to ./components directory"""
    with lcd('components'):
        url = COMPONENTS.get(component)
        if not url:
            warn('Unknown component [%s]' % component)
            return
        local('wget %s -O %s.tar.gz' % (url, component))
        local('mkdir %s -p' % component)
        local('tar -xvf %(name)s.tar.gz --strip 1 -C %(name)s' % {'name':component})
        local('rm *.tar.gz')
