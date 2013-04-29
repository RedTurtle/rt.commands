from fabric.api import cd
from fabric.api import env
from fabric.api import sudo
from rt.commands import _err
from rt.commands.buildout_components import _prepare_cmp_buildout, _run_cmp_buildout


def staging():
    """Set host to staging"""
    env.hosts = [env.get('staging_host')] or _err('staging_host need to be set')
    env.component_buildout_cfg = 'staging.cfg'


def production():
    """Set host to production"""
    env.hosts = [env.get('production_host')] or _err('production_host need to be set')
    env.component_buildout_cfg = 'production.cfg'


def prepare_buildout(buildout_cfg=None, buildout_repo=None):
    """Prepare zc.buildout environment so we can use
    ``bin/buildout -c production.cfg`` to build a production environment.
    """
    if hasattr(env, 'component'):
        _prepare_cmp_buildout(env.component, buildout_cfg=buildout_cfg)
        return

    opts = dict(
        project_name=env.get('project_name') or _err('project_name missing'),
        buildout_repo=buildout_repo or env.get('buildout_repo'),
        python_version=env.get('python_version') or '2.6',
        buildout_cfg=buildout_cfg or env.get('buildout_cfg') or 'buildout.cfg',
    )

    with cd('/opt'):
        sudo('svn co %(buildout_repo)s %(project_name)s' % opts)
    with cd('/opt/%(project_name)s' % opts):
        sudo(
            'virtualenv -p /opt/python/python-%(python_version)s/bin/python --no-site-packages ./' % opts,
        )
        sudo('bin/python bootstrap.py -c %(buildout_cfg)s' % opts)


def run_buildout(buildout_cfg=None):
    """Run ``bin/buildout -c production.cfg`` in production folder
    on the production server.
    """
    if hasattr(env, 'component'):
        _run_cmp_buildout(env.component)
        return

    opts = dict(
        project_name=env.get('project_name') or _err('project_name missing'),
        buildout_cfg=buildout_cfg or env.get('buildout_cfg') or 'buildout.cfg',
    )

    with cd('/opt/%(project_name)s' % opts):
        sudo('bin/buildout -c %(buildout_cfg)s' % opts)


def install_init():
    """Install debian-based init script"""
    
    opts = dict(
        project_name=env.get('project_name') or _err('project_name missing'),
    )
    sudo('cp /opt/%(project_name)s/etc/initscript /etc/init.d/%(project_name)s' % opts)
    sudo('update-rc.d %(project_name)s defaults' % opts)


def deploy():
    """1. Prepare buildout, 2. Run buildout, 3. Install init"""
    prepare_buildout()
    run_buildout()
    install_init()

