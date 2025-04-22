from importlib import import_module
class FuzzyComparisonPipeline(object):
    def process_item(self, item, spider):
        for module in FuzzyComparisonPipeline.fuzzyModules:
            name = module['name']
            configurationLoader = module['configurationLoader']
            moduleConfigurationFile = module['moduleConfigurationFile']
            settings = module['settings']
            module_to_import = import_module('fuzzymodules.'+name)
            #print(getattr(module_to_import, name))
            instance = getattr(module_to_import, name)(configurationLoader, moduleConfigurationFile, settings, item)
        #item = instanceOfModule.getNewItem()
            #instanceOfModule(configurationLoader, moduleConfigurationFile, settings)
        return item

    @staticmethod
    def setFuzzyModules(fuzzyModules):
        FuzzyComparisonPipeline.fuzzyModules = fuzzyModules# Define your item pipelines here