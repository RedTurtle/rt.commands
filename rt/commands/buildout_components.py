from fabric.api import local
from fabric.api import quiet
from fabric.api import env
from fabric.api import cd
from fabric.api import run
from fabric.network import needs_host, normalize
import os


@needs_host
def tail_log(component='', glob='*.log'):
    """Tail the log in the component folder
    """
    opts = env.copy()
    opts['glob'] = glob
    if component:
        opts['component'] = 'components/%s' % component
    else:
        opts['component'] = component

    cmd = ("tail -f %(code_dir)s/%(component)s/var/log/%(glob)s" % opts)
    run(cmd)

@needs_host
def sync_var(component='plone'):
    """Sync component's buildout var folder

    :params component: a string specify the component or ".." to sync the var
                       at the root of the buildout
    """
    user, host, port = normalize(env.host_string)
    opts = env.copy()
    with quiet():
        opts['local_buildout'] = local('pwd', capture=True) + '/var/'

    opts['component'] = os.path.normpath('components/%s/var/' % component)
    opts['short_options'] = '-Pthrvz'
    opts['exclude'] = ' '.join(["--exclude='%s'" % x
                                for x in ('log', '*.old', '.svn')])
    cmd = ("rsync %(exclude)s %(short_options)s "
           "%(user)s@%(host)s:%(code_dir)s/%(component)s %(local_buildout)s"
           ) % opts
    local(cmd)


def run_buildout(buildout_cfg='buildout.cfg', component='plone'):
    """Run remotely ``bin/buildout -c ${buildout_cfg}`` in component folder.
    """
    opts = env.copy()
    opts['buildout_cfg'] = buildout_cfg
    opts['component'] = 'components/%s/' % component

    with cd('%(code_dir)s/%(component)s' % opts):
        run('svn up')
        run('./bin/buildout -NUc %(buildout_cfg)s' % opts)
