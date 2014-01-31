rt.commands
===========

deployment commands for RT (mainly fabric scripts)

Your fabfile
------------

To use rt.commands import it in your fabfile and
set some environment variables.

For example, you can start from this template::

    # this is necessary to make the fabric commands available
    from fabric.api import env
    from rt.commands import *
    from rt.commands.project import *
    from rt.commands.buildout_components import *

    # This is the main python version
    env.python_version = '2.7'

    # This is the buildout script to use
    env.buildout_cfg = 'buildout.cfg'

    # And some hosts
    env.staging_user = 'plone'
    env.staging_host = 'staging.example.com'
    env.staging_dir = '/opt/www.demo.example.com'
    env.production_user = 'plone'
    env.production_host = 'example.com'
    env.production_dir = '/opt/www.example.com'


rt.commands
-----------

production:
    Pushes into the env.hosts the production server

staging:
    Pushes into the env.hosts the production server

rt.commands.buildout_components
-------------------------------

sync_var:
    Requires *staging* or *production* before.
    Sync component's buildout var folder
    It accepts the component parameter (default=plone)
    You can pass .. to get the var at the buildout root

sync_var:
    Requires *staging* or *production* before.
    Sync component's buildout var folder
    It accepts the component parameter (default=plone)
    You can pass .. to get the var at the buildout root
