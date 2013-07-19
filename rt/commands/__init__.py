from fabric.api import env


def _err(msg):
    raise AttributeError(msg)


def _set_target(target_type):
    """Set host to staging"""
    env.hosts = [env.get('%s_host' % target_type)
                 or _err('%s need to be set' % '%s_host' % target_type)]
    env.user = env.get('%s_user' % target_type) or 'plone'
    env.code_dir = (env.get('%s_dir' % target_type)
                    or _err('%s_dir need to be set' % target_type))


def staging():
    """Set host to staging"""
    _set_target('staging')


def production():
    """Set host to production"""
    _set_target('production')
