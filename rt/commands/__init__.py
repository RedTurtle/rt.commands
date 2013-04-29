from fabric.api import env


def _err(msg):
    raise AttributeError(msg)


def staging():
    """Set host to staging"""
    env.hosts = [env.get('staging_host')] or _err('staging_host need to be set')
    env.component_buildout_cfg = 'staging.cfg'


def production():
    """Set host to production"""
    env.hosts = [env.get('production_host')] or _err('production_host need to be set')
    env.component_buildout_cfg = 'production.cfg'
