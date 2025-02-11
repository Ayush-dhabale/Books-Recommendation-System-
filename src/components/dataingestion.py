import os
import sys
import pandas as pd

from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException

#Initializze the Data Ingestion Configuration

@dataclass #decorator
class DataIngestionConfig:
    '''
        Is a Special class, which automatically creates the special methods like __init__ and __repr__ 
        Will use it to store three variables
        1. path to training dataset
        2.path to test dataset
        3. path to row dataset

    '''
    
    cleaned_data_path = os.path.join('artifacts', 'cleaned_data.csv')
    

##Create a class for Data Ingestion
class DataIngestion:
    def __init__(self):
        #Create a variable which will store the paths to raw,trian,test data
        logging.info("Data Ingestion Configuration Starts")
        self.ingestion_config = DataIngestionConfig()
        logging.info("Data Ingestion Configuration completed")
        
    def initiate_data_ingestion(self):
        logging.info("Data Ingetion process starts")
        
        try:
            data = pd.read_csv()
        
        except:
            raise CustomException()