# %%
import pandas as pd
import os

#Lecture des différents fichiers
dfJadas=pd.read_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\Dossier dfs JADAS\df_final_jadas.csv')
dfRestat=pd.read_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\Dossier dfs restat\df_final_restat.csv')
dfJadas.insert(column='Installation',loc=1,value='JADAS')
dfRestat.insert(column='Installation',loc=1,value='LYCEE RESTAT')


# %%
df_final=pd.concat([dfJadas,dfRestat],axis=0)
df_final=df_final.loc[:,['Installation','Onduleur']]
df_final= df_final.drop_duplicates(subset=['Onduleur'])
df_final.to_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\TableDonneesOnduleurs.csv')

# %%
