import streamlit as st
import pandas as pd
import numpy as np
import difflib
import string



dico1 = pd.read_csv("dico_uno.csv")
dico2 = pd.read_csv("dico_duo.csv")
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
    
    #Résultat final
    func_html = open("résultat.html","w") 

    #Liste résultats parfaits
    if new_string in dico['Listes'].unique():
        string_unique = string_.lower()
        liste_parf = list(dico[dico.Listes == new_string].Mot.values)
        liste_parf.remove(str(string__unique).lower())
        for i in range(len(liste_parf)):
            liste_parf[i] = liste_parf[i].capitalize()
        if len(liste_parf) > 0:    
       
            func_html.write(f"Voici une liste des anagrammes parfaits de {string_.capitalize()} : {', '.join(liste_parf)}")
      
    
   
    else:
        
        nombre_bonnes_réponses_90 = 0
        written_message = 0
        for index, row in enumerate(dico['Listes']):        
            check_90 = difflib.SequenceMatcher(None,new_string,row).ratio()*100 >= ress_level           
        
                
            if check_90 is True and difflib.SequenceMatcher(None, new_string, row).ratio()*100 < 100:
                nombre_bonnes_réponses_90 +=1 
                if written_message == 0:
                    func_html.write(f'Je ne trouve aucun anagramme parfait pour "{string_}".')
                    func_html.write(f'\nVoici les mots qui y ressemblent à au moins {ress_level}% !\n')
                    written_message +=1
                func_html.write(f"- {dico['Mot'][index].capitalize()} (Ressemblance = {int(round(difflib.SequenceMatcher(None, new_string, row).ratio()*100,0))}%)\n")
            
            
            else:
                pass
            
        if nombre_bonnes_réponses_90 == 0:
            func_html.write(f"Désolé, je ne trouve aucun anagramme pour ce mot !")
            func_html.write(f'\nVous pouvez essayer de réduire le pourcentage de ressemblance.')
            
        else:
            func_html.write('\nEt voilà !')
            

    func_html.close()
    HTMLFile = open("résultat.html","r")
    result_final = HTMLFile.read()
    return result_final
    
    

def main():
    
    string_text = st.text_input("Ecrivez ici le ou les mots dont vous souhaitez découvrir les anagrammes !")
    percent = st.number_input("Pourcentage de ressemblance")
    st.warning("Note : l'algorithme testera automatiquement la ressemblance parfaite, donc inutile d'inscrire '100' en guise de pourcentage de ressemblance. La plupart des mots trouveront des anagrammes imparfaits entre 85 et 91% de ressemblance.")
    if string_text and percent:

        st.write(ressemblance(string_text, percent))

if __name__ == "__main__":
    main()

