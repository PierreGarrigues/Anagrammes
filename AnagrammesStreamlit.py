import streamlit as st
import pandas as pd
import numpy as np
import difflib
import string



dico1 = pd.read_csv(r"C:\Users\pierr\Downloads\dico1.csv")
dico2 = pd.read_csv(r"C:\Users\pierr\Downloads\dico2.csv")
dico = pd.concat([dico1, dico2], ignore_index=True, axis=0)


def ressemblance(string_, ress_level):
    
    #Travail sur la string_ initiale
    translator = str.maketrans('', '', string.punctuation)
    #Suppression des espaces
    new_string = string_.replace(" ","").replace('é','e').replace('è','e').replace('ê','e').replace('à','a').replace('â','a')
    #Lower
    new_string = new_string.lower()
    #string to list        
    new_string = new_string.translate(translator)
    new_string = sorted(list(new_string))
    new_string = ''.join(new_string)
    
    
   
    
    if new_string in dico['Listes'].unique():
        liste_parf = dico[dico.Listes == new_string].Mot.values
        #liste_parf.tolist().remove(string_)
        result = f"Voici une liste des anagrammes parfaits de {string_.capitalize()} : {', '.join(liste_parf)}"
        return result
      
    
   
    else:
        print(f'Je ne trouve aucun anagramme parfait pour "{string_}".\nCherchons les mots qui y ressemblent à au moins {ress_level}% !')
        nombre_bonnes_réponses_90 = 0
        for index, row in enumerate(dico['Listes']):        
            check_90 = difflib.SequenceMatcher(None,new_string,row).ratio()*100 >= ress_level           
        
                
            if check_90 is True:
                nombre_bonnes_réponses_90 +=1
                
                result = f"- {dico['Mot'][index].capitalize()} (Ressemblance = {int(round(difflib.SequenceMatcher(None, new_string, row).ratio()*100,0))}%)"
                return result
            
            
            else:
                pass
            
        if nombre_bonnes_réponses_90 == 0:
            result = f"Désolé, je ne trouve aucun anagramme pour ce mot !\nVous pouvez essayer de réduire le taux de matching minimal."
            return result
        else:
            print('Et voilà !')
            

    
    
    

def main():
    string_text = st.text_input("Ecrivez ici le ou les mots dont vous souhaitez découvrir les anagrammes !")
    percent = st.number_input("Pourcentage de ressemblance")
    if string_text and percent:

        st.write(ressemblance(string_text, percent))

if __name__ == "__main__":
    main()

