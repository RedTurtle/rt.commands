# -*- coding: utf-8 -*-
import os
from fabric.api import env
from fabric.contrib.console import confirm
from fabric.network import needs_host, normalize
from fabric.operations import local
from fabric.utils import warn


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


@needs_host
def _sync_path(relative_path='', exclude=''):
    ''' Syncs a remote path to a local folder

    The path is relative:
     - locally to the current working directory
     - remotely to the production_dir found in env
    '''
    normalize(env.host_string)
    local_path = os.path.normpath(os.path.join(os.getcwd(), relative_path))
    remote_path = os.path.normpath(
        os.path.join(
            env['code_dir'], 'components/plone', relative_path
        )
    )
    cmd = "rsync -Pthrz %(user)s@%(host)s:%(remote_path)s/ %(local_path)s/" % {
        'user': env['user'],
        'host': env['host'],
        'local_path': local_path,
        'remote_path': remote_path,
    }
    if exclude:
        cmd = "%s --exclude=%s" % (cmd, exclude)
    local(cmd)


def sync_blobstorage(relative_path="var/blobstorage", exclude=""):
    """Sync Plone var/filestorage folder

    :params component: a string specify the component or ".." to sync the var
                       at the root of the buildout
    """
    return _sync_path(relative_path=relative_path, exclude=exclude)


def sync_filestorage(relative_path="var/filestorage", exclude="*.old"):
    """Sync Plone var/filestorage folder

    :params component: a string specify the component or ".." to sync the var
                       at the root of the buildout
    """
    return _sync_path(relative_path=relative_path, exclude=exclude)
