from Web3Scraping import Web3Scraping
import shutil
import os

import time

# Debut du decompte du temps
start_time = time.time()

webscraping = Web3Scraping()
webscraping.saveHtmlFile()

# remove folders if they exists
shutil.rmtree(webscraping.pathBP, ignore_errors=True)
shutil.rmtree(webscraping.pathBS, ignore_errors=True)
shutil.rmtree(webscraping.pathJT, ignore_errors=True)
shutil.rmtree(webscraping.pathJT_langid, ignore_errors=True)
shutil.rmtree(webscraping.pathJT_Truelg, ignore_errors=True)

os.mkdir(webscraping.pathJT)
os.mkdir(webscraping.pathBS)
os.mkdir(webscraping.pathBP)
os.mkdir(webscraping.pathJT_langid)
os.mkdir(webscraping.pathJT_Truelg)

webscraping.justText()
webscraping.boilerPipe()
webscraping.beautifulSoup()

webscraping.lgTable["JT"] = webscraping.calculStat(webscraping.pathJT, "JustText")
webscraping.lgTable["BP"] = webscraping.calculStat(webscraping.pathBP, "BoilerPipe")
webscraping.lgTable["BS"] = webscraping.calculStat(webscraping.pathBS, "BeautifulSoup")

#print(webscraping.lgTable['JT'])
#print(webscraping.lgTable["BP"])
#print(webscraping.lgTable["BS"])

print("*********** Question 2************")

webscraping.JTWithlangid()
webscraping.JTWithTruelg()
webscraping.lgTable["JT_langid"] = webscraping.calculStat(webscraping.pathJT_langid, "JT_langid")
webscraping.lgTable["JT_Truelg"] = webscraping.calculStat(webscraping.pathJT_Truelg, "JT_Truelg")


#print(webscraping.lgTable["JT_langid"])
#print(webscraping.lgTable["JT_Truelg"])

print("************* Question 3 **********")


webscraping.evaluates["JT"] = webscraping.evaluationIntrinseque(webscraping.pathJT)
webscraping.evaluates["JT_langid"] = webscraping.evaluationIntrinseque(webscraping.pathJT_langid)
webscraping.evaluates["JT_Truelg"] = webscraping.evaluationIntrinseque(webscraping.pathJT_Truelg)

print(webscraping.evaluates)

print("____End____")

# Affichage du temps d execution
print("Temps d execution : %s secondes ---" % (time.time() - start_time))
