from importlib import import_module
class DefaultFuzzyComparisonModule:
    def __init__(self,configurationLoader, moduleConfigurationFile, settings, item):
        self.settings = settings
        self.configurationLoader = configurationLoader
        self.moduleConfigurationFile = moduleConfigurationFile
        pass

    def getNewItem(self):
        module_to_import = import_module('configurationLoaders.'+self.configurationLoader)
        instance = getattr(module_to_import, self.configurationLoader)(self.moduleConfigurationFile, self.settings)
        configuration_data = instance.getConfiguration()
        fuzzyResults = getFuzzyResutls(settings['attribute'], configuration_data)

    def getFuzzyResutls(self, word, data_json):
        results = dict()
            for masterEntry in data_json:
                compareAgainsMasterEntry = SM(None, word.lower(), masterEntry.lower()).ratio()
                resultsDetailsEntry = dict()
                for detailEntry in data_json[masterEntry]:
                    resultsDetailsEntry[detailEntry] = SM(None, word.lower(), detailEntry.lower()).ratio()
                results[masterEntry] = dict(masterEntry = compareAgainsMasterEntry, detailsEntry = resultsDetailsEntry)
        bestComparisin = -1
            bestResult = ""
            for masterEntry in results:
                entry = results[masterEntry]
                if entry['masterEntry']>bestComparisin:
                    bestComparisin = entry['masterEntry']
                    bestResult = masterEntry
                entryDetails = entry['detailsEntry']
                for entryDetail in entryDetails:
                    if entryDetails[entryDetail] > bestComparisin:
                        bestComparisin = entryDetails[entryDetail]
                        bestResult = masterEntry
        return dict(bestResult = bestResult, bestComparisin = bestComparisin)