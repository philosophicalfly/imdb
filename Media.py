class Media:
    'Common base class for all media'

    counter = 0

    def __init__(self, type, pryTittle, oriTitle, isAdult, startYear, endYear, runtime, genres):
        self.type = type
        self.priTitle = pryTittle
        self.oriTitle = oriTitle
        self.isAdult = isAdult
        self.startYear = startYear
        self.startYear = endYear
        self.runtime = runtime
        self.genres= genres
        Media.counter += 1

    def toString(self):
        return 'type '+self.type + '\npriTitle  '+self.priTitle + '\npriTitle ' + self.priTitle + '\nisAdult ' +self.isAdult + '\nstartYear ' +self.startYear + '\nendYear ' +self.endYear + '\nruntime '+self.runtime +'\ngenres '+ self.genres


