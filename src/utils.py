import os
import sys
import pandas as pd
import numpy as np
import pickle

from src.logger import logging
from src.exception import CustomException

def save_object(file_path,object):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(object,file_obj)

    except Exception as e:
        logging.info("Error while saving the object")
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        logging.info("Error while loading the object")
        raise CustomException(e,sys)