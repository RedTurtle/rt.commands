from fabric.api import lcd, local
from fabric.api import cd
from fabric.api import sudo
from fabric.api import env
from fabric.utils import warn, abort
from fabric.contrib.files import exists
from rt.commands import _err


COMPONENTS = {'plone': 'https://github.com/RedTurtle/deployments.buildout.plone/archive/master.tar.gz'}


def pull_cmp(component):
    """pull component to ./components directory"""
    with lcd('components'):
        url = COMPONENTS.get(component)
        if not url:
            warn('Unknown component [%s]' % component)
            return
        local('wget %s -O %s.tar.gz' % (url, component))
        local('mkdir %s -p' % component)
        local('tar -xvf %(name)s.tar.gz --strip 1 -C %(name)s' % {'name':component})
        local('rm *.tar.gz')


def component(component):
    """Set's component env to join commands on"""
    env.component = component


def _prepare_cmp_buildout(component, buildout_cfg=None):
    opts = dict(
        component=component,
        project_name=env.get('project_name'),
        buildout_cfg=buildout_cfg or env.get('component_buildout_cfg') or _err('buildout_cfg missing'),
    )
    with cd('/opt/%(project_name)s/components/%(component)s' % opts):
        if not exists('buildout.cfg'): # no symlink
            if not exists('profiles/%(buildout_cfg)s' % opts): # no profile
                abort('No %(buildout_cfg)s found' % opts)
            sudo('ln -s profiles/%(buildout_cfg)s buildout.cfg' % opts)
        sudo('/opt/%(project_name)s/bin/python bootstrap.py' % opts)


def _run_cmp_buildout(component):
    opts = dict(
        component=component,
        project_name=env.get('project_name'),
    )
    with cd('/opt/%(project_name)s/components/%(component)s' % opts):
        sudo('bin/buildout')
