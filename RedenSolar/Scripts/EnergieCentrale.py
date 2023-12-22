# %%
import pandas as pd
import os 

df=pd.read_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\df_final_restat.csv')


# %%


# Specify the folder path
folder_path = r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\TABLE DONNEES CENTRALE\ENERGIE CENTRALE\ENERGIE CENTRALE'
df_final=pd.DataFrame(columns=['Date','Energie (kWh)','Centrale'])


# %%

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        # Process or read the file here
        print(f'Reading file: {filename}')
        df=pd.read_csv(os.path.join(folder_path,filename),delimiter=',')
        df=df.drop(index=0)
        df=df.drop(df.columns[[1]],axis=1)
        df=df.rename(columns={'Courbe de charge (kWh)':'Energie (kWh)'})
        df['Date'] = pd.to_datetime(df['Date'])
        df_final=pd.concat([df_final,df],axis=0)
        


# %% [markdown]
# 

# %%
df_final.to_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\TABLE DONNEES CENTRALE\ENERGIE CENTRALE\ENERGIE CENTRALE.csv')




