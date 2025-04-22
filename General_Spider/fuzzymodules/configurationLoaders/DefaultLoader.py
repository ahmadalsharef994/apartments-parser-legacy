import json
from pprint import pprint
class DefaultLoader:
    def __init__(self, moduleConfigurationFile, settings):
        if DefaultLoader.configurationFiles is None:
            DefaultLoader.configurationFiles = dict()
        self.moduleConfigurationFile = moduleConfigurationFile
        self.settings = settings
        pass
    def getConfiguration():
        if DefaultLoader.configurationFiles[self.moduleConfigurationFile] is not None:
            return DefaultLoader.configurationFiles[attribute]
        else:
            with open('configurations/'+moduleConfigurationFile) as data_file:
                data = json.load(data_file)
                DefaultLoader.configurationFiles[self.moduleConfigurationFile] = data
                return data