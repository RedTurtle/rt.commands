rt.commands
===========

deployment commands for RT (mainly fabric scripts)

Your fabfile
------------

To use rt.commands import it in your fabfile and
set some environment variables.

For example, you can start from this template:: python

    # this is necessary to make the fabric commands available
    from rt.commands import _set_target
    from rt.commands.components.plone import buildout  # noqa
    from rt.commands.components.plone import develop  # noqa
    from rt.commands.components.plone import pull_buildout  # noqa
    from rt.commands.components.plone import supervisorctl  # noqa
    from rt.commands.components.plone import sync_blobstorage  # noqa
    from rt.commands.components.plone import sync_filestorage  # noqa


    def staging():
        ''' Prepare host
        '''
        _set_target(
            user='redturtle',
            host='127.0.0.1',
            path='/opt/www.redturtle.it/components/plone/'
        )

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

rt.commands.components.plone
----------------------------

Special functions to sync plone.
Given this fabfile::

    # -*- coding: utf-8 -*-
    from fabric.api import env
    from rt.commands import production, staging
    from rt.commands.components.plone import sync_blobstorage
    from rt.commands.components.plone import sync_filestorage

    env.staging_user = 'redturtle'
    env.staging_host = 'somehost.redturtle.it'
    env.staging_dir = '/opt/somedir'

You can invoke::

    fab staging sync_blobstorage
    fab staging sync_filestorage

In order to have those folders synced
