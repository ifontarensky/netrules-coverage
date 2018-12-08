
import inspect
import importlib

from traffic.TrafficAPI import TrafficAPI


def find_and_load_plugin(plugin_type):

    try:
        module = importlib.import_module('traffic.{0}'.format( plugin_type))
        for x in dir(module):
            obj = getattr(module, x)

            if inspect.isclass(obj) and issubclass(obj, TrafficAPI) and obj is not TrafficAPI:
                return obj

    except ImportError as error:
        print(error)
        return None


def load_plugins():
    plugins = []
    plugins.append(find_and_load_plugin('tcp_port_range_scanner'))
    return plugins