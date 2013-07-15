from fabric.api import cd
from fabric.api import env
from fabric.api import run


def supervisor(action='status'):
    """Run ``bin/supervisorctl ${action}"""
    opts = env.copy()
    opts['action'] = action

    with cd('%(code_dir)s' % opts):
        run('./bin/supervisorctl %(action)s' % opts)
