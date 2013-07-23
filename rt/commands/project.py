# -*- coding: utf-8 -*-
from fabric.api import cd
from fabric.api import env
from fabric.api import lcd
from fabric.api import local
from fabric.api import run
from fabric.context_managers import quiet
from fabric.contrib import console
from rt.commands.components import plone
import os


def supervisor(action='status'):
    """Run remotely ``bin/supervisorctl ${action}"""
    opts = env.copy()
    opts['action'] = action

    with cd('%(code_dir)s' % opts):
        run('./bin/supervisorctl %(action)s' % opts)


def component_buildout(components='*', profile='production.cfg'):
    """Deploy local production ${components} buildouts"""
    # if we get asterix - iterate on all commands
    with quiet():
        local_buildout = local('pwd', capture=True)
    if components == '*':
        with quiet():
            with lcd('components'):
                output = local('ls -d */', capture=True)
                components = [a.strip('/') for a in output.split()]
    else:
        components = [components]

    for component in components:
        opts = {'component_dir': '%s/components/%s' % (local_buildout,
                                                       component),
                'profile': profile}
        if not console.confirm("Do you want to launch "
                               "buildout in %(component_dir)s" % opts):
            continue

        with lcd('%(component_dir)s' % opts):
            # symlink profile
            if not os.path.exists('buildout.cfg'):
                local('ln -s ./profiles/%(profile)s buildout.cfg' % opts)
            # bootstrap
            local('../../bin/python bootstrap.py')
            # run buildout
            local('./bin/buildout -N')


def install_crontab(components='*'):
    '''
    Install crontab for components
    '''
    return plone.install_crontab()


def install_logrotate(components='*'):
    '''
    Install logrotate for components
    '''
    return plone.install_logrotate()
