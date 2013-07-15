from fabric.api import env


def _err(msg):
    raise AttributeError(msg)


def staging():
    """Set host to staging"""
    env.hosts = [env.get('staging_host')] or _err('staging_host need to be set')
    env.user = env.get('staging_user') or 'plone'
    env.code_dir = env.get('staging_dir') or _err('staging_dir need to be set')


def production():
    """Set host to production"""
    env.hosts = [env.get('production_host')] or _err('production_host need to be set')
    env.user = env.get('production_user') or 'plone'
    env.code_dir = env.get('production_dir') or _err('production_dir need to be set')
