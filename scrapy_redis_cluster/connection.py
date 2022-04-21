import sys

import six

from redis.cluster import ClusterNode
from scrapy.utils.misc import load_object

from . import defaults


# Shortcut maps 'setting name' -> 'parmater name'.
SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url',
    'REDIS_HOST': 'host',
    'REDIS_PORT': 'port',
    'REDIS_DB': 'db',
    'REDIS_ENCODING': 'encoding',
}

if sys.version_info > (3,):
    SETTINGS_PARAMS_MAP['REDIS_DECODE_RESPONSES'] = 'decode_responses'


def get_redis_from_settings(settings):
    """Returns a redis client instance from given Scrapy settings object.

    This function uses ``get_client`` to instantiate the client and uses
    ``defaults.REDIS_PARAMS`` global as defaults values for the parameters. You
    can override them using the ``REDIS_PARAMS`` setting.

    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.

    Returns
    -------
    server
        Redis client instance.

    Other Parameters
    ----------------
    REDIS_URL : str, optional
        Server connection URL.
    REDIS_HOST : str, optional
        Server host.
    REDIS_PORT : str, optional
        Server port.
    REDIS_DB : int, optional
        Server database
    REDIS_ENCODING : str, optional
        Data encoding.
    REDIS_PARAMS : dict, optional
        Additional client parameters.

    Python 3 Only
    ----------------
    REDIS_DECODE_RESPONSES : bool, optional
        Sets the `decode_responses` kwarg in Redis cls ctor

    """
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


def get_redis_cluster_from_settings(settings):
    """
    Returns a redis cluster instance from given Scrapy settings object.

    :param settings:
    :return:
    """
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict("REDIS_PARAMS"))
    params.setdefault("cluster_nodes", settings.get("REDIS_STARTUP_NODES"))
    # XXX: Deprecate REDIS_* settings.
    return get_redis_cluster(**params)


# Backwards compatible alias.
def from_settings(settings):
    """
    Select the connection method of redis according to the configuration in settings

    :param settings:
    :return:
    """
    if "REDIS_STARTUP_NODES" in settings:
        return get_redis_cluster_from_settings(settings)
    return get_redis_from_settings(settings)


def get_redis(**kwargs):
    """Returns a redis client instance.

    Parameters
    ----------
    redis_cls : class, optional
        Defaults to ``redis.StrictRedis``.
    url : str, optional
        If given, ``redis_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.

    Returns
    -------
    server
        Redis client instance.

    """
    redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)

def get_redis_cluster(**kwargs):
    """
    Returns a redis cluster instance.

    :param kwargs:
    :return:
    """
    redis_cluster_cls = kwargs.get("redis_cluster_cls", defaults.REDIS_CLUSTER_CLS)
    cluster_nodes = kwargs.pop("cluster_nodes")
    cluster_nodes = [ClusterNode(i['host'], i['port']) for i in cluster_nodes]
    return redis_cluster_cls(startup_nodes=cluster_nodes, **kwargs)
