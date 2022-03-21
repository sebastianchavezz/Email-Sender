
import pandas as pd
from .sendEmail import EmailSender

class Datahandler:

    filename :str = '.\\app\\vibes.json'
    
    
    def __init__(self):
        self.dataframe =  pd.read_json(self.filename)
        self.dataframe.fillna('', inplace=True)
        self.update_df_indexes()


    def update_df_toevoegen(self,array_like:list)->None:
        temp = pd.DataFrame([array_like],columns=['PRODUCTEN','OPMERKING'])
        self.dataframe = pd.concat([self.dataframe,temp],axis=0)
        self.update_df_indexes()
    
    def update_df(self,col,producten,opmerking):
        """Handles the change if data for file"""
        self.dataframe.loc[col:col,'PRODUCTEN':'OPMERKING'] = producten, opmerking
        self.update_df_indexes()

    def update_df_remove(self,array:list):
        self.update_df_indexes()
        for i in sorted(array,reverse=True):
            self.dataframe = self.dataframe.drop(self.dataframe.index[i])
        self.update_df_indexes()

    def save_df(self):
        self.update_df_indexes()
        self.dataframe.to_json('.\\app\\vibes.json')
        
    
    def send_email(self,indexes):
        sender = EmailSender(self.dataframe.iloc[indexes])
        sender.send_mail()

    def update_df_indexes(self)->None:
        self.dataframe.reset_index(drop=True,inplace=True)