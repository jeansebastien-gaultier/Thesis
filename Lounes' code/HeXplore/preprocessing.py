import re
import string
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#################################################
# Fonctions d'analyse syntaxique du texte       #
#################################################
def checkForBalises(rep):
    '''Renvoie TRUE si rep contient des balises.

    INPUTS :
        chaine : chaine de caractères à analyser.
    
    OUTPUTS :
        Booléen
    '''
    return True if re.search("<.+?>", rep) else False

def removeSpacePunct(rep):
    '''Supprime les espacements et les caractères de ponctuation du rapport

    INPUTS :
        rep : chaine de caractères représentant le rapport à nettoyer. <Chaine>

    OUTPUTS :
        String
    '''
    # On remplace tous les caractères de ponctuation par des espaces
    rep_clean = re.sub(f'[{re.escape(string.punctuation)}]', ' ', rep)

    return ''.join((rep_clean.lower()).split())

def removeMultipleSpaces(rep, replace=''):
    '''Supprime les espaces multiples de la chaine rep et les remplace par le caractère replace

    INPUTS :
        rep : chaine de caractères représentant le rapport à nettoyer. <Chaine>
        replace : chaine par laquelle remplacer les espaces. Par défaut : tout regrouper. <Chaine>

    OUTPUTS :
        String
    '''
    return replace.join((rep.lower()).split())

#################################################
# Fonctions liées à la suppression des doublons #     
#################################################

def reportsIdentical(rep1, rep2):
    '''Renvoie True si deux rapports sont égaux au sens absolu ; indépendamment des espaces, de la ponctuation et de la casse. 

    INPUTS :
        rep1, rep2 : deux chaines de caractères représentant les rapports à comparer.

    OUTPUTS :
        Booléen
    '''
    # On compare les chaînes de caractères sans tenir compte des espaces et de la casse
    return True if removeSpacePunct(rep1) == removeSpacePunct(rep2) else False

def getIdenticalReports(dictRaps):
    '''Renvoie les couples d'id des rapports identiques.

    INPUTS :
        dictRaps : dictionnaire {ID: Texte}
    
    OUTPUTS :
        Liste des couples d'id de rapports identiques. Ex : (2, 5).
    '''
    identical = []
    for couple in list(combinations(list(dictRaps.keys()), 2)):
        if reportsIdentical(dictRaps[couple[0]], dictRaps[couple[1]]):
            identical.append(couple)
    return identical

def removeDuplicateReports(repDf, colId, colReport, returnCleaned=False):
    '''Renvoie le dataframe de rapports en supprimant les doublons (au sens de la fonction removeSpacePunct)

    INPUTS :
        repDf : dataframe de rapports. <pandas.DataFrame>
        colId : colonne contenant les id. <String>
        colReport : colonne contenant le texte des rapports. <String>
        returnCleaned : mettre à true si vous souhaitez que le dataframe sans ponctuation et espacement soit renvoyé. <Booléen>
    
    OUPUTS :
        dictionnaire
    '''
    cloneDf = repDf.copy()

    for k in range(len(list(cloneDf[colReport]))):
        cloneDf[colReport][k] = removeSpacePunct(cloneDf[colReport][k])
    cloneDf.drop_duplicates(subset=[colReport], inplace = True)

    if returnCleaned==True:
        return cloneDf
    else:
        return repDf[repDf[colId].isin(list(cloneDf[colId]))]

def getTauxSimilarite(rep1, rep2):
    '''Calcule la similarité cosinus entre deux rapports représentés selon tfidf.

    INPUTS
        rep1, rep2 : chaînes de caractères représentant les rapports.

    OUTPUTS
        taux de similarité (numpy.float64)
    '''
    vectorizer = TfidfVectorizer()
    tfidf_vectors = vectorizer.fit_transform([rep1, rep2])
    similarity = cosine_similarity(tfidf_vectors[0:1], tfidf_vectors)
    return similarity[0][1]

################################################
# Fonctions pour la création d'un corpus       #
################################################
'''
def createVocabFromReports(raps , stopwords = [], racinisation = False):
    Crée un vocabulaire (liste de tokens) à partir de la Pandas Serie de rapports fournie en entrée.

    INPUTS :
        listRaps : liste de rapports médicaux (colonne de dataframe). pandas.Series
        stopwords : liste de stop words. List<String>
        racinisation : True si les mots doivent être racinisés. Booléen.

    OUTPUTS :
        Liste de tokens. List<String>
    
    vocab = []

    if stopwords:
        vocab = [word for i in raps.split().values.tolist() for word in i if (word not in stopwords)]
    else:
        vocab = [word for i in raps.split().values.tolist() for word in i]
    
    if vocab != [] and racinisation:
        vocab = set([])

    return vocab
'''