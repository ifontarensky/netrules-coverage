
import inspect
import importlib

from plugins.PluginAPI import PluginAPI


def find_and_load_plugin(plugin_type):

    try:
        module = importlib.import_module('plugins.{0}'.format( plugin_type))
        for x in dir(module):
            obj = getattr(module, x)

            if inspect.isclass(obj) and issubclass(obj, PluginAPI) and obj is not PluginAPI:
                return obj

    except ImportError as error:
        print(error)
        return None


def load_plugins():
    plugins = []
    plugins.append(find_and_load_plugin('tcp_port_range_scanner'))
    return plugins