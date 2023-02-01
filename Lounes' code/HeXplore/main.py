from data_extraction import getRapportsAnnee
from preprocessing import getTauxSimilarite
import json
import pandas as pd

# On importe le fichier qui contient les fichiers à lire
with open('documents.json', 'r') as f:
    directories = json.loads(f.read())

allRapports = {}
rapports_annee = None

for annee in list(directories.keys()):
    print(f"Année : {str(annee)}")
    dossiers = [directories[annee]["metadata"]["baseDossier"]+"/"+doss for doss in directories[annee]["dossiers"]]
    delimSup = directories[annee]["metadata"]["delimSup"] if directories[annee]["metadata"]["delimSup"] != "None" else None
    delimInf = directories[annee]["metadata"]["delimInf"]
    typeRap = directories[annee]["metadata"]["type"]
    ext = directories[annee]["metadata"]["extension"] if directories[annee]["metadata"]["extension"] != "None" else None
    pattern = directories[annee]["metadata"]["pattern"] if directories[annee]["metadata"]["pattern"] != "None" else None
    takeName = True if directories[annee]["metadata"]["takeName"] == "True" else False
    rapports_annee = getRapportsAnnee(annee, dossiers, delimSup, delimInf, typeRap, ext, pattern, takeName)
    allRapports = {**rapports_annee, **allRapports}
    print(f"Nombre de rapports : {str(len(rapports_annee))}")
    print("#################################")
    rapports_annee = None

print(f"Nombre de rapports total : {str(len(allRapports))}")
print("*********************************")

df_rapports = pd.DataFrame.from_dict(allRapports, orient="index")
print(df_rapports.head())
#print("*********************************")

