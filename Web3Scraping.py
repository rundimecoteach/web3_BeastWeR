import os
import justext
import langid
import json

from math import *
from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
from cleaneval_tool import *




class Web3Scraping:

    def __init__(self):
        self.files = []
        self.paths = '/Users/yassineel-azami/Downloads/Corpus_detourage/'
        self.pathJT_langid = self.paths + 'JT_langid/'
        self.pathFrom = self.paths + "html/"
        self.pathJT = self.paths + 'JT/'
        self.pathBP = self.paths + 'BP/'
        self.pathClean = self.paths + 'clean/'
        self.pathBS = self.paths + 'BS/'
        self.pathJT_Truelg = self.paths + 'JT_TrueLg/'
        self.lgTable = dict()
        self.evaluates = dict()

    def saveHtmlFile(self):
        print("______Require files______")
        for r, d, f in os.walk(self.pathFrom):
            for file in f:
                self.files.append(file)

    def calculStat(self, path, name):
        print("______Stat calculation______")
        nblignes    = 0
        nbChars = 0
        varianceL   = 0
        varianceC   = 0

        nbBruit = 0
        nbSilence = 0

        nbCharfileArray   = []
        nbCharfCleanArray = []

        for f in self.files:
            file    = open(path + f, 'r', encoding='utf8', errors="ignore")
            fClean = open(self.pathClean + f, 'r', encoding='utf8', errors="ignore")

            nbLineFile  = 0
            nbCharFile  = 0

            for line in file:
                nbLineFile += 1
                nbCharFile += len(line)
            file.close()

            nbCharfileArray.append(nbCharFile)

            nbLineFClean  = 0
            nbCharFClean  = 0

            for line in fClean:
                nbLineFClean += 1
                nbCharFClean += len(line)
            fClean.close()

            nbCharfCleanArray.append(nbCharFClean)

            nblignes    += nbLineFile
            nbChars     += nbCharFile
            varianceL   += (nbLineFClean - nbLineFile) ** 2
            varianceC   += (nbCharFClean - nbCharFile) ** 2

        ecartTypeLine = sqrt(varianceL / len(self.files))
        ecartTypeChar = sqrt(varianceC / len(self.files))

        i=0
        for _ in nbCharfileArray:
            if nbCharfCleanArray[i] - nbCharfileArray[i] > ecartTypeChar:
                nbBruit += 1
            if nbCharfCleanArray[i] - nbCharfileArray[i] < nbChars / len(self.files):
                nbSilence += 1
            i+=1


        nblignes += nbLineFile
        nbChars  += nbCharFile

        print("==========================================================>")
        print(name)
        print("lignes")
        print('Nombre totals de ligne : {0}'.format(nblignes))
        print("Nombre de ligne moyenne par fichier : {0}".format(nblignes / len(self.files)))
        print("Ecart type : {0}".format(ecartTypeLine))
        print("===========>")
        print("caracteres")
        print('Nombre totals de ligne : {0}'.format(nbChars))
        print("Nombre de ligne moyenne par fichier : {0}".format(nbChars / len(self.files)))
        print("Ecart type : {0}".format(ecartTypeChar))
        print("===========>")
        print("Pourcentages des silences et bruits")
        print('Silence: {:10.4f} %'.format((nbSilence / len(self.files)) * 100))
        print("Bruit : {:10.4f} %".format((nbBruit / len(self.files)) * 100))
        print("==========================================================>")

        return {
            "nbLigne": nblignes,
            "nbCaractere": nbChars,
            "moyLigne": nblignes / len(self.files),
            "moyCaractere": nbChars / len(self.files),
            "ecartLigne": ecartTypeLine,
            "ecartCaractere": ecartTypeChar,
            "bruit": ((nbSilence / len(self.files)) * 100),
            "silence": ((nbBruit / len(self.files)) * 100),
        }

    def isFileEmpty(self, fpath):
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

    def justText(self):
        print("______Just Text Method______")
        for f in self.files:
            file = open(self.pathFrom + f, 'r', encoding='utf8', errors="ignore")
            s = file.read()
            fr = open(self.pathJT + f, "w+",encoding='utf8', errors="ignore")
            paragraphs = justext.justext(s, justext.get_stoplist("English"))
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    fr.write('<p>' + paragraph.text + '</p>')
            fr.close()

    def boilerPipe(self):
        print("______Boiler Pipe Method______")
        for f in self.files:
            file = open(self.pathFrom + f, 'r', encoding='utf8', errors="ignore")
            s = file.read()
            fr = open(self.pathBP + f, "w+", encoding='utf8', errors="ignore")
            paragraphs = Extractor(extractor='ArticleExtractor', html=s)
            try:
                if paragraphs is not None:
                    fr.write(paragraphs.getText())
            except OSError as err:
                print("OS error: {0}".format(err))
            fr.close()

    def beautifulSoup(self):
        print("______Beautiful Soup Method______")
        for f in self.files:
            fr = open(self.pathBS + f, "w+", encoding='utf8', errors="ignore")
            with open(self.pathFrom + f, encoding='utf8', errors="ignore") as fp:
                soup = BeautifulSoup(fp)
                paragraph = soup.p
                if paragraph is not None:
                    fr.write('<p>' + paragraph.text + '</p>')
            fr.close()

    # question 2
    def JTWithlangid(self):
        for f in self.files:

            if not self.isFileEmpty(self.pathJT + f):
                file = open(self.pathJT + f, 'r', encoding='utf8', errors="ignore")
                s = file.read()
            else:
                file = open(self.pathFrom + f, 'r', encoding='utf8', errors="ignore")
                s = file.read()

            lg = langid.classify(s)

            fr = open(self.pathJT_langid + f, "w+", encoding='utf8', errors="ignore")

            switcher = {
                "el": "Greek",
                "pl": "Polish",
                "ru": "Russian",
            }

            langue = switcher.get(lg[0], "English")

            fileHtml = open(self.pathFrom + f, 'r', encoding='utf8', errors="ignore")
            sHtml = fileHtml.read()

            paragraphs = justext.justext(sHtml, justext.get_stoplist(langue))
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    fr.write(paragraph.text)
            fr.close()

    def JTWithTruelg(self):
        with open(self.paths + 'doc_lg.json') as json_file:
            data = json.load(json_file)

        for f in self.files:
            fr       = open(self.pathJT_Truelg + f, "w+", encoding='utf8', errors="ignore")
            fileHtml = open(self.pathFrom + f, 'r', encoding='utf8', errors="ignore")
            sHtml    = fileHtml.read()

            langue = data[f]
            if langue == "Chinese":
                langue = "English"

            paragraphs = justext.justext(sHtml, justext.get_stoplist(langue))
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    fr.write(paragraph.text)
            fr.close()

    def evaluationIntrinseque(self, path):
        print("_____ Evaluation Intrinseque _______")
        results = {
            'el' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
            'pl' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
            'ru' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
            'en' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
            'zh' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
            'all' : {'fScore' : 0, 'precision' : 0, 'recall' : 0 },
        }


        for f in self.files:
            if not self.isFileEmpty(path+f):
                file = open(self.pathJT+f, 'r', encoding='utf8', errors="ignore")
                s = file.read()
            else:
                file = open(self.pathFrom+f, 'r', encoding='utf8', errors="ignore")
                s = file.read()

            lg = langid.classify(s)

            eval_ = evaluate_file(path+f, self.pathClean+f)

            results[lg[0]]['fScore'] += eval_['f-score']
            results[lg[0]]['precision'] += eval_['precision']
            results[lg[0]]['recall'] += eval_['recall']

            results['all']['fScore'] += eval_['f-score']
            results['all']['precision'] += eval_['precision']
            results['all']['recall'] += eval_['recall']

        for k in results:
            for i in results[k]:
                results[k][i] = results[k][i]/len(self.files)

        return results