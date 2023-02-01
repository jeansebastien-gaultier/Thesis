import re
import os
from preprocessing import checkForBalises
import random

def checkEspaceMemoire(fname):
    '''Vérifie que l'on dispose de l'espace mémoire suffisant en RAM pour pouvoir charger le fichier fname.
    '''
    filepath = os.path.abspath(fname)
    filesize = os.path.getsize(filepath)
    available_memory = psutil.virtual_memory().free
    
    if filesize > available_memory:
        raise Exception("La taille du fichier est supérieure à l'espace disponible en mémoire RAM")
    return 1

def split_string(string, separator):
    '''Effectue un split en gérant le cas où le séparateur est une chaine vide
    '''
    if separator==None:
        raise ValueError("Le séparateur ne peut pas être NULL.")
    elif separator == '':
        return [string]
    else:
        return string.split(separator)

def getSingleRapport(fname, delimiteurSup, delimiteurInf, pattern=None, id=None):
    '''Fonction à privilégier lorsqu'on souhaite extraire des rapports et que l'on dispose d'un seul rapport par fichier.

    INPUTS 
        fname : nom ou  chemin du fichier <String>
        delimiteurSup : balise ou chaîne de caractères permettant de délimiter le début d'un enregistrement <String>
        delimiteurInf : balise ou chaîne de caractères permettant de délimiter la fin d'un enregistrement <String>
        pattern : pattern regex de la balise XML où se trouve l'id de l'enregistrement <String>
        id : si l'id est explicite (ex. nom du fichier) on peut se passer du pattern. Fonctionne seulement dans le cas d'un seul rapport par document. <int>

    OUTPUTS 
        dictionnaire contenant l'id en clé et le contenu de l'EHR en valeur.

    '''
    result = {}
    filepath = os.path.abspath(fname)
    ehr=''
    header=''
    
    try:
        checkEspaceMemoire(filepath)
    except Exception:
        print("Désolé, votre espace mémoire ne vous permet pas de charger le fichier...")
        return None
    
    with open(filepath) as f:
        content = f.read().strip()
        # L'utilisateur doit fournir un délimiteur inférieur non-null et différent de ''.
        # Dans le cas où la chaine donnée entrée n'existe pas dans le rapport, la variable paragraphs contiendra le paragraphe initial 
        if delimiteurInf!=None:
            paragraphs = split_string(content, delimiteurInf)
        else:
            raise ValueError("Le délimiteur inférieur ne peut pas être NULL.")
        
        # La chaîne d'intérêt (EHR), se trouve forcément à la case 0 du tableau paragraphs
        if paragraphs[0]!= None and paragraphs[0] != '' and not paragraphs[0].isspace():
            if delimiteurSup != None and delimiteurSup != '':
                header = paragraphs[0].split(delimiteurSup)[0]
                ehr = paragraphs[0].split(delimiteurSup)[1]
            else:
                ehr = paragraphs[0]
        else:
            return None
        
        # Une fois que l'ehr a été récupéré, on extrait l'id s'il n'a pas été fourni par l'utilisateur
        if ehr != None and ehr != '' and not ehr.isspace():
            if id != None:
                result[id] = ehr
            else:
                if pattern != None:
                    # On récupère l'id du compte rendu contenu dans la balise XML (<RECORD> par exemple)
                    rec_id = re.findall(pattern , header)
                    if rec_id != []:
                        # La chaîne sp[1] représente le corps du compte rendu
                        #result[int(rec_id[0])] = sp[1].replace('\n', ' ')
                        result[rec_id[0]] = ehr
                # Si l'ID n'est pas fourni, il faut que pattern soit != None
                else:
                    raise ValueError("Le pattern ne peut pas être NULL lorsque l'ID n'est pas spécifié.")
        return result

def getRapports(fname, delimiteurSup, delimiteurInf, pattern=None, id=None):
    '''Fonction qui se charge d'extraire PLUSIEURS rapports contenus dans un MÊME fichier.
    
    INPUTS 
        fname : nom ou  chemin du fichier <String>
        delimiteurSup : balise ou chaîne de caractères permettant de délimiter le début d'un enregistrement <String>
        delimiteurInf : balise ou chaîne de caractères permettant de délimiter la fin d'un enregistrement <String>
        pattern : pattern regex de la balise XML où se trouve l'id de l'enregistrement <String>
        id : dans le cas où l'id du fichier est connu mais pas celui des ehr dans le fichier <String>

    OUTPUTS 
        dictionnaire contenant les id en clés et les contenus des EHR en valeurs.
    '''
    result = {}
    filepath = os.path.abspath(fname)
    sp = []
    ap = None
    
    try:
        checkEspaceMemoire(filepath)
    except Exception:
        print("Désolé, le fichier n'a pas été trouvé ou votre espace mémoire ne vous permet pas de le charger...")
        return 0

    with open(filepath) as f:
        content = f.read().strip()
        # L'utilisateur doit fournir un délimiteur inférieur non-null et différent de ''.
        # Dans le cas où la chaine donnée entrée n'existe pas dans le rapport, la variable paragraphs contiendra le paragraphe initial 
        if delimiteurInf!=None:
            paragraphs = split_string(content, delimiteurInf)
        else:
            raise ValueError("Le délimiteur inférieur ne peut pas être NULL.")

        # Effectuer une deuxième séparation par le début avec la chaîne delimiteurSup
        for paragraph in paragraphs:
            # On vérifie que le paragraphe n'est pas vide 
            if paragraph!= None and paragraph != '' and not paragraph.isspace():
                if delimiteurSup != None and delimiteurSup != '':
                    sp = paragraph.split(delimiteurSup)
                else:
                    if delimiteurInf=='':
                        raise ValueError("Il faut au moins un délimiteur valide.")
                    ap = paragraph 

                if pattern != None:
                    if sp != []:
                        # On récupère l'id du compte rendu contenu dans la balise XML ou le texte (<RECORD> par exemple)
                        rec_id = re.findall(pattern , sp[0])
                        if rec_id != []:
                            # La chaîne sp[1] représente le corps du compte rendu
                            result[rec_id[0]] = sp[1]
                    elif ap != None:
                        rec_id = re.findall(pattern , ap)
                        if rec_id != []:
                            # La chaîne sp[1] représente le corps du compte rendu
                            result[rec_id[0]] = ap
                else:
                    # Si aucun pattern pour l'extraction d'id n'a été spécifiée
                    a_id = str(random.randint(8000,30000))
                    # On vérifie d'abord si l'on dispose d'un id pour le fichier entier
                    if id!=None and checkForBalises(paragraph) == False:
                        if sp!=[]:
                            if len(sp)==2:
                                result[id+'_'+a_id] = sp[1]
                            else:
                                result[id+'_'+a_id] = sp[0]
                        elif ap!=None:
                            result[id+'_'+a_id] = ap
                        
                    else:
                        if checkForBalises(paragraph) == False:
                            print(f"Warning : Aucun id n'a pu être identifié pour ce compte rendu. l'ID aléatoire {a_id} lui a été assigné.")
                            if sp!=[]:
                                result[a_id] = sp[1]
                            elif ap!=None:
                                result[a_id] = ap
            sp=[]
            ap=None
    return result

def getRapportsAnnee(annee, dossiers, delimSup, delimInf, typeRapport="Single", extension="txt", pattern=None, takeName=False):
    '''Renvoie les rapports médicaux d'une année sous forme d'un dictionnaire {ID: Rapport} 

    INPUTS :
        annee : année des rapports à extraire. (int)
        typeRapport : chaine de caractères pouvant prendre 2 valeurs. "Single" si on a un rapport par fichier, "Multiple" si possibilité d'avoir plusieurs rapports par fichier. 
        dossiers : liste de chemins (dossiers) contenant les rapports individuels si type="Single". Liste de chemins vers des fichier si type="Multiple".
        extension : spécifie les extensions à prendre en compte (.txt, .xml, ou None si pas d'extensions pour les fichiers de cette année-là.)
        delimSup : délimiteur supérieur pour extraire le corps des rapports.
        delimInf :  délimiteur inférieur pour extraire le corps des rapports.
        pattern : (optionnel) il s'agit du pattern pour extraire l'id du rapport s'il se trouve dans le document. Généralement utilisé lorsque type="Multiple".
        takeName : (optionnel) si les comptes rendus sont nombreux dans un même fichier mais qu'il n'y a pas d'id pour chacun, mettre à True pour considérer l'id du fichier.

    OUTPUTS :
        dictionnaire {ID: Rapport} pour l'année spécifiée.
    '''
    final_dict = {}
    rapports = {}
    warning = None

    if typeRapport=="Single":
        for doss in dossiers:
            with os.scandir(doss) as entries:
                for entry in entries:
                    if entry.is_file():
                        if extension!=None:
                            splitted = str(entry.name).split('.')
                            # On s'assure de ne traiter que les fichier dans le format spécifié
                            if len(splitted)==2 and ((extension=="xml" and splitted[1]=="xml") or (extension=="txt" and splitted[1]=="txt")): 
                                try:
                                    rapports[str(annee)+'_'+splitted[0]] = (getSingleRapport(doss+'/'+str(entry.name), delimiteurSup=delimSup, delimiteurInf=delimInf, pattern=None, id=splitted[0]))[splitted[0]]
                                except Exception as err:
                                    print(err.args)
                                    return
                            else:
                                warning = f"Warning : Des fichiers autres que {extension} ont été trouvés mais ont été ignorés pour l'année {annee}."
                        else:
                            try:
                                rapports[str(annee)+'_'+str(entry.name)] = (getSingleRapport(doss+'/'+str(entry.name), delimiteurSup=delimSup, delimiteurInf=delimInf, pattern=None, id=str(entry.name)))[str(entry.name)]   
                            except Exception as err:
                                print(err.args)
                                return
            # On concatène l'ancien contenu du dictionnaire final et les NOUVEAUX rapports (le complémentaire de l'intersection entre l'ensemble rapports et l'ensemble final_dict)
            #final_dict = {**rapports, **final_dict}
            final_dict = {**dict(set(rapports.items()).difference(set(final_dict.items()))), **final_dict}
            rapports={}             
    elif typeRapport=="Multiple":
        for doss in dossiers:
            if takeName==False:
                try:
                    rapports = getRapports(doss, delimSup, delimInf, pattern)
                except Exception as err:
                    print(err.args)
            else:
                with os.scandir(doss) as entries:
                    for entry in entries:
                        if entry.is_file():
                            if extension!=None:
                                splitted = str(entry.name).split('.')
                                if len(splitted)==2 and ((extension=="xml" and splitted[1]=="xml") or (extension=="txt" and splitted[1]=="txt")):
                                    ident = splitted[0]
                                    try:
                                        rapports = {**getRapports(doss+'/'+str(entry.name), delimSup, delimInf, pattern, id=ident), **rapports}
                                    except Exception as err:
                                        print(err.args)
                                else:
                                    warning = f"Warning : Des fichiers autres que {extension} ont été trouvés mais ont été ignorés pour l'année {annee}."
                            else:
                                ident = entry.name
                                try:
                                    rapports = {**getRapports(doss+'/'+str(entry.name), delimSup, delimInf, pattern, id=ident), **rapports}
                                except Exception as err:
                                    print(err.args)
            rapports = {str(annee)+"_"+str(key): value for key, value in rapports.items()}
            #final_dict = {**rapports, **final_dict}
            final_dict = {**dict(set(rapports.items()).difference(set(final_dict.items()))), **final_dict}
            rapports = {}
    else:
        raise ValueError("La valeur de 'typeRapport' doit être {'Single' ou 'Multiple'}.") 
    if warning!=None: print(warning)
    return final_dict

    
