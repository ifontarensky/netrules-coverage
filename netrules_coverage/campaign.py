import yaml
from loader import find_and_load_plugin

from utils import ColorPrint as _


def load_configuration():
    with open("parameters.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def is_disable(parameters):
    if 'enable' in parameters and not parameters['enable']:
        _.print_plugin_disable(plugin, parameters)
        return True
    return False



if __name__ == '__main__':

    for plugin, parameters in load_configuration().items():
        if is_disable(parameters):
            _.print_plugin_disable(plugin, parameters)
            continue
        else:
            _.print_plugin(plugin, parameters)
            if 'enable' in parameters:
                del parameters['enable']

        obj = find_and_load_plugin(plugin)()
        getattr(obj, 'run')(**parameters)
        obj.generate_pcap("%s.pcap" % plugin)
