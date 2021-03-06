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
            local('test -f buildout.cfg || ln -s ./profiles/%(profile)s buildout.cfg' % opts)  # noqa
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


def _isuptodate(folder_path='.'):
    ''' Check if folder_path is up to date
    '''
    with lcd(folder_path):
        if os.path.exists('%s/.git' % folder_path):
            local('git --no-pager status')
            local('git --no-pager diff origin/master')
        if os.path.exists('%s/.svn' % folder_path):
            local('svn status')
            local('svn diff -rHEAD')
