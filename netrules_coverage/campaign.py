import yaml
from loader import find_and_load_plugin



def load_configuration():
    with open("parameters.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':

    for plugin, parameters in load_configuration().items():
        print(plugin)
        print(parameters)
        obj = find_and_load_plugin(plugin)()
        getattr(obj, 'run')(**parameters)
        obj.generate_pcap("%s.pcap" % plugin)
