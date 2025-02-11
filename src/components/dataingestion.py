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
            
            logging.info("Readin the datasets")
            books_df = pd.read_csv('notebook/data/Books.csv', encoding='ISO-8859-1')
            ratings_df = pd.read_csv('notebook/data/Ratings.csv', encoding='ISO-8859-1')
            users_df = pd.read_csv('notebook/data/Users.csv', encoding='ISO-8859-1')
            
            return books_df,ratings_df,users_df
        
        except Exception as e:
            logging.info('Error occured during initiating the Data Ingetion process')
            raise CustomException(e,sys)
        
        
    def split_location(self):
        
        logging.info("Spliting the Location feature of the user dataset")
        
        try:
            logging.info("Reading the user dataset")
            _,__,user_df = self.initiate_data_ingestion()
            
            # Function to extract City, State, and Country
            def extract_location(location):
                
                logging.info("Spliting the location feature by ','")
                parts = [part.strip() for part in str(location).split(',')]
    
                logging.info("Defining the city, state and country variables")
                # Assign default empty values
                city, state, country = "", "", ""

                logging.info("Setting the values of city , state, country")
                # Extract based on available parts
                if len(parts) == 3:
                    city, state, country = parts
                elif len(parts) == 2:
                    city, state, country = parts[0], "", parts[1]
                elif len(parts) == 1:
                    city = parts[0]

                # Handling cases where 'n/a' appears in the state field
                if state.lower() == "n/a":
                    state = ""

                return pd.Series([city, state, country])
            
            logging.info("Calling the function to split the location feature")
            user_df[['City', 'State', 'Country']] = user_df['Location'].apply(extract_location)
            logging.info("Splited the location feature")
            
            #Now the location feature in the user dataset is no longer required , so just remove it
            
            user_df.drop('Location',axis= 1, inplace= True)
            logging.info("Droped the Location feature")
            
            return user_df
        
        except Exception as e:
            logging.info("Error occured during spliting the location dataset")
            raise CustomException(e,sys)
        
    def handle_nullvalues_booksdataset(self):
        
        logging.info("Handling the nan values of booksdataset")
        
        try:
            
            logging.info("Reading the book dataset")
            
            book_df , _, __ = self.initiate_data_ingestion()
            
            logging.info("Extracting the null features")
            null_features = [feature for feature in book_df.columns if book_df[feature].isnull().sum() >= 1]
            
            #Out of 2.7 lakh records only 2,3 values are missing in the features, so we will just replace them by empty string
            for feature in null_features:
                book_df[feature].fillna(value= "", inplace= True)
                
            return book_df
            
        except Exception as e:
            logging.info("Error occured while handling the nan values of the book dataset")
            raise CustomException(e,sys)
        
    def remove_imageUrls(self,books_df):
        logging.info("Removing the image urls of the books dataset")
        
        try:
            
            logging.info("Defining the columns to drop")
            #Columns to remove/drop
            columns_to_drop = ['Image-URL-S','Image-URL-L']
            
            logging.info("Dropping the image urls")
            books_df.drop(columns= columns_to_drop, inplace=True)
            
            return self.books_df
            
        except Exception as e:
            logging.info("Error ocurred during the removal of the image urls")
            raise CustomException(e,sys)
        
        
    def clean_year_of_publication(self,books_df):
        
        logging.info("Cleaning the year of publication feature of the books datasset")
        
        try:
            
            logging.info("Coverting the data type of the year of publication feature")
            # Convert string years to numeric
            books_df['Year-Of-Publication'] = pd.to_numeric(books_df['Year-Of-Publication'], errors='coerce') #enteries which are not numeric will we stored as Nan
            
            logging.info("Replacing the out-of-range values of years")
            # Replace out-of-range values
            books_df.loc[(books_df['Year-Of-Publication'] < 1800) | (books_df['Year-Of-Publication'] > 2025), 'Year-Of-Publication'] = None
            
            #will replace nan values of year of publication with median year
            logging.info("Defining a median year")
            median_year = books_df['Year-Of-Publication'].median()
            
            logging.info("Filling the nan values")
            books_df['Year-Of-Publication'].fillna(median_year, inplace=True)
            
            return books_df
        
        except Exception as e:
            
            logging.info("Error occured during cleanning the year of pulication feature")
            raise CustomException(e,sys)
      
                
    def megring_datasets(self,users_df,ratings_df,books_df):
         
        logging.inf("Merging the datasets")
        
        try:
            logging.info("Merging rating ad book datasets")
            # Merge Books and Ratings on ISBN
            merged_books_ratings = pd.merge(ratings_df, books_df, on='ISBN', how='inner')
            
            logging.info("Merging the resulting dataframe of books and ratings with user datasets")
            # Merge the resulting dataframe with Users on User-ID
            final_merged_df = pd.merge(merged_books_ratings, users_df, on='User-ID', how='inner')
            
            return final_merged_df
            
        except Exception as e:
            
            logging.info("Error occured while merging the datasets")
            raise CustomException(e,sys)
        
    def handling_age_nan_values(self,final_merged_df):
        
        logging.info("Handling the nan values of age feature")
        
        try:
            logging.info("Replacing the out of range values by nan")
            # Replace out-of-range values
            final_merged_df.loc[(final_merged_df['Age'] < 5) | (final_merged_df['Age'] > 100), 'Age'] = None
            
            # Compute median ages by book rating and publication year
            
            rating_medians = final_merged_df.groupby('Book-Rating')['Age'].median()
            year_medians = final_merged_df.groupby('Year-Of-Publication')['Age'].median()
            overall_median = final_merged_df['Age'].median()
    
            def impute_age(row):
                if pd.notna(row['Age']):
                    return row['Age']
                elif row['Book-Rating'] in rating_medians:
                    return rating_medians[row['Book-Rating']]
                elif row['Year-Of-Publication'] in year_medians:
                    return year_medians[row['Year-Of-Publication']]
                else:
                    return overall_median

            final_merged_df['Age'] = final_merged_df.apply(impute_age, axis=1)
            final_merged_df['Age'].fillna(overall_median, inplace=True)

            return final_merged_df
            
        except Exception as e:
            
            logging.info("Error occured while handlin the nan values of age feature")
            raise CustomException(e,sys)
        