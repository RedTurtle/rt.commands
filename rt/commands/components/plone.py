# -*- coding: utf-8 -*-
import os
from fabric import api
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


def _base_path(component=''):
    ''' Return the base path for this host
    '''
    return os.path.join(
        api.env.paths[api.env.host_string],
        component
    )


def _buildout_path():
    ''' Return the base path for this host
    '''
    return os.path.join(_base_path(), '../../bin/buildout')


def _develop_path():
    ''' Return the base path for this host
    '''
    return os.path.join(_base_path(), 'bin/develop')


def _supervisorctl_path():
    ''' Return the base path for the supervisorctl executabel
    '''
    return os.path.join(_base_path(), '../../bin/supervisorctl')


def pull_buildout(component=''):
    ''' Update the buildout
    '''
    with api.cd(_base_path(component)):
        api.run('git fetch')
        api.run('git diff origin/master')
        api.run('git pull')


def buildout(component=''):
    if component and not component.startswith('components'):
        component = 'components/%s' % component

    with api.cd(_base_path(component)):
        api.run('{buildout} -Nt 2'.format(
            buildout=_buildout_path(),
        ))


def develop(params='rb'):
    with api.cd(_base_path()):
        api.run('{develop} {params}'.format(
            develop=_develop_path(),
            params=params,
        ))


def supervisorctl(params='status'):
    with api.cd(_base_path()):
        api.run('{supervisorctl} {params}'.format(
            supervisorctl=_supervisorctl_path(),
            params=params,
        ))


@needs_host
def _sync_path(relative_path='', exclude=''):
    ''' Syncs a remote path to a local folder

    The path is relative:
     - locally to the current working directory
     - remotely to the production_dir found in env
    '''
    normalize(api.env.host_string)
    local_path = os.path.normpath(os.path.join(os.getcwd(), relative_path))
    remote_path = os.path.normpath(
        os.path.join(
            _base_path(), relative_path
        )
    )
    cmd = "rsync -Pthrz {host}:{remote_path}/ {local_path}/".format(
        host=api.env.host_string,
        local_path=local_path,
        remote_path=remote_path,
    )
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
