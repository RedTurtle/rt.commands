# coding=utf-8
from fabric import api


def _set_target(host='', user='', path=''):
    ''' Prepare host
    '''
    if user:
        host = '{user}@{host}'.format(
            user=user,
            host=host,
        )
    api.env.hosts.append(host)
    api.env.setdefault('paths', {}).update({host: path})
