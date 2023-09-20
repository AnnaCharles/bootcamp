
import csv
import gzip
import ural
from collections import Counter
import argparse
from collections import defaultdict
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Lis le fichier CSV et renvoie les URL doublons.')
parser.add_argument('filename',   help='nom du fichier CSV')


args = parser.parse_args()

count=0
depth = 0
url_dep = []
doublons=[]
dico=Counter()
lines=Counter()
c=Counter()
nbre_par_profondeur = Counter()

multimap = defaultdict(list)

with gzip.open(str(args.filename), 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader.fieldnames)
    for row in tqdm(reader,total=12643957):
        count+=1
        text=row['url']
        domaine = ural.get_domain_name(text)
        c[domaine]+=1

        d = int(row['depth'])
        if d > depth :
            depth=d
        multimap[text].append(row['id'])

        # dico[text]+=1
        # if dico[text]>1 :
        #     doublons.append(row)
        #     doublons.append(lines[text])
        # lines[text]=row 

        if domaine == 'rfi.fr' :
            nbre_par_profondeur[row['depth']]+=1

    print('Le nombre d url de ladepeche.fr par profondeur est : \n')
    for key, value in nbre_par_profondeur.items() :
        print("Pour la profondeur : "+ str(key) +" il y a "+ str(value) +" url ")
        
    print ( "La profondeur maximale est : "+str(depth))
    print("Les 10 noms de domaine qui apparaissent le plus sont : \n")

    val = c.most_common(10)
    i=0
    while i<10:
        print(val[i][0] +" : "+str(val[i][1])+"\n")
        i+=1

    print(dico.most_common(10))

    #recuperer les doublons 
    #for (key,value) in multimap.items :
    #   if len(value) >1 :
    #      doublons.append(value)

    # j=0
    # while j<len(doublons) :
    #     print("Les url de ces lignes sont égaux \n" )
    #     print (doublons[j])
    #     print("\n")
    #     print(doublons[j+1])
    #     print("\n\n")
    #     j+=2

    with open('doublons.csv', 'w', newline='') as csvfile:
        #fieldnames = reader.fieldnames
        fieldnames = ['id', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in multimap.items() :
            if len(value) >1 :
                for row_id in value : 
                    writer.writerow({'id':str(row_id), 'url':key})
            
