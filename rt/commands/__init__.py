from fabric.api import cd
from fabric.api import env
from fabric.api import sudo
import buildout_components; buildout_components


def _err(msg):
    raise AttributeError(msg)


def staging():
    """Set host to staging"""
    env.hosts = [env.get('staging_host')] or _err('staging_host need to be set')


def production():
    """Set host to production"""
    env.hosts = [env.get('production_host')] or _err('production_host need to be set')


def prepare_buildout(project_name=None, python_version=None, buildout_cfg=None, buildout_repo=None):
    """Prepare zc.buildout environment so we can use
    ``bin/buildout -c production.cfg`` to build a production environment.
    """
    opts = dict(
        project_name=project_name or env.get('project_name'),
        buildout_repo=buildout_repo or env.get('buildout_repo'),
        python_version=python_version or env.get('python_version') or '2.6',
        buildout_cfg=buildout_cfg or env.get('buildout_cfg') or 'buildout.cfg',
    )

    with cd('/opt'):
        sudo('svn co %(buildout_repo)s %(project_name)s' % opts)
    with cd('/opt/%(project_name)s' % opts):
        sudo(
            'virtualenv -p /opt/python/python-%(python_version)s/bin/python --no-site-packages ./' % opts,
        )
        sudo('bin/python bootstrap.py -c %(buildout_cfg)s' % opts)


def run_buildout(project_name=None, buildout_cfg=None):
    """Run ``bin/buildout -c production.cfg`` in production folder
    on the production server.
    """
    opts = dict(
        project_name=project_name or env.get('project_name'),
        buildout_cfg=buildout_cfg or env.get('buildout_cfg') or 'buildout.cfg',
    )

    with cd('/opt/%(project_name)s' % opts):
        sudo('bin/buildout -c %(buildout_cfg)s' % opts)
