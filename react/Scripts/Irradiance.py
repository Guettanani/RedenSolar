# %%
import pandas as pd
import os 

df=pd.read_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\df_final_restat.csv')


# %%


# Specify the folder path
folder_path = r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\IRRADIANCE\IRRADIANCE'
df_final=pd.DataFrame(columns=['Date','Irradiance'])


# %%

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        # Process or read the file here
        print(f'Reading file: {filename}')
        df=pd.read_excel(os.path.join(folder_path,filename))
        df=df.drop(df.index[0:7])
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]
        df=df.drop(index=0)
        dfSplit=pd.DataFrame(columns=['Avant','Apres'])
        dfSplit[['Avant','Apres']]=df['device'].str.split('- ',expand=True)
        df['Centrale']=dfSplit['Apres']
        df=df.drop(df.columns[[0,2]],axis=1)
        df['solar_energy']=df['solar_energy']*1000
        df=df.rename(columns={'date':'Date','solar_energy':'Irradiance'})
        df['Date'] = pd.to_datetime(df['Date'])
        df_final=pd.concat([df_final,df],axis=0)
        


# %% [markdown]
# 

# %%
df_final.to_csv(r'C:\Users\Florent\WebEnvironment\RedenSolar\DataStorage\IRRADIANCE\IRRADIANCE.csv')




