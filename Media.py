class Media:
    'Common base class for all media'

    counter = 0

    def __init__(self, tconst, type, pryTittle, oriTitle, isAdult, startYear, endYear, runtime, genres):
        self.tconst = tconst
        self.type = type
        self.priTitle = pryTittle
        self.oriTitle = oriTitle
        self.isAdult = isAdult
        self.startYear = startYear
        self.endYear = endYear
        self.runtime = runtime
        self.genres= genres
        Media.counter += 1

    def toString(self):
        return 'type '+self.type + '\npriTitle  '+self.priTitle + '\npriTitle ' + self.priTitle + '\nisAdult ' +self.isAdult + '\nstartYear ' +self.startYear + '\nendYear ' +self.endYear + '\nruntime '+self.runtime +'\ngenres '+ self.genres

    def toCsvRow(self):
        return str(str([self.tconst, self.type, self.priTitle, self.oriTitle, self.isAdult, self.startYear, self.endYear, self.runtime, self.genres]) + '\n')


