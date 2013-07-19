# -*- coding: utf-8 -*-
import os
from fabric.operations import local
from fabric.utils import warn
from fabric.contrib.console import confirm


def _get_projectname():
    '''
    Try to guess our projectname
    '''
    path = os.getcwd()
    if path.endswith('/plone'):
        path = os.path.split(path)[0]
    if path.endswith('/components'):
        path = os.path.split(path)[0]
    return os.path.split(path)[1]


def install_file(source, target, force=''):
    '''
    This will install the logrotate file for this component
    '''
    if not os.path.isfile(source):
        return warn('%s is missing' % source)
    opts = {'source': source,
            'target': target,
            'cpcommand': 'cp'
            }

    if force != 'true':
        opts['cpcommand'] += ' -i'
    try:
        local('%(cpcommand)s  %(source)s %(target)s' % opts)
    except SystemExit as e:
        if not confirm('Do you want to go on?'):
            raise e


def install_crontab(force=''):
    '''
    This will install the logrotate file for this component
    '''
    projectname = _get_projectname()
    source = 'etc/crontab'
    target = '/etc/cron.d/%s_plone' % projectname.replace('.', '_')
    install_file(source, target, force)


def install_logrotate(force=''):
    '''
    This will install the logrotate file for this component
    '''
    projectname = _get_projectname()
    source = 'etc/logrotate.conf'
    target = '/etc/logrotate.d/%s.plone' % projectname
    install_file(source, target, force)
