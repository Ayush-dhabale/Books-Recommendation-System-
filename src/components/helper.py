import os
import sys
import pandas as pd
import numpy as np
import pickle

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split


@dataclass  # Decorator
class HelperConfig:
    """
    HelperConfig is a special class using @dataclass, which automatically creates methods like __init__ and __repr__.
    It stores the paths for important dataset files:
    
    1. `final_filtered_data_path`: Path to the final filtered dataset.
    2. `users_books_pivot_table_path`: Path to the pivot table of users and books.
    3. `similarity_scores_path`: Path to the precomputed similarity scores.
    """
    
    final_filtered_data_path = os.path.join('artifacts', 'final_filtered_data.pkl')
    users_item_matrix_path = os.path.join('artifacts', 'users_books_pt.pkl')
    similarity_scores_path = os.path.join('artifacts', 'similarity_scores.pkl')
    knn_model_path = os.path.join('artifacts', 'knn_model.pkl')
    svd_model_path = os.path.join('artifacts', 'svd_model.pkl')
    book_pivot_path = os.path.join('artifacts', 'book_pivot.pkl')
    
# Create a helper class
class Helper:
    
    def __init__(self):
        """
        Initializes the Helper class by setting up configurations and loading the cleaned dataset.
        """
        logging.info("Helper Configuration Starts")
        self.helper_config = HelperConfig()
        logging.info("Helper Configuration completed")

        logging.info("Loading the cleaned data")
        try:
            self.data = pd.read_csv('artifacts/cleaned_data.csv', encoding='ISO-8859-1')
            logging.info("Cleaned data loaded successfully")
        except Exception as e:
            logging.error("Error occurred while loading the cleaned data")
            raise CustomException(e, sys)

    def filter_data(self):
        """
        Filters the dataset by:
        1. Selecting users who have rated at least 200 books.
        2. Selecting books that have received at least 50 ratings.
        
        The filtered dataset is then saved as a pickle file.
        """
        logging.info("Filtering the data")
        
        try:
            # Users with 200+ ratings
            logging.info("Extracting users with 200+ ratings")
            users_with_200_ratings_data = self.data.loc[
                self.data.groupby('User-ID')['Book-Rating'].transform('count') >= 200
            ]

            logging.info("Extracting books with 50+ ratings from the filtered user data")
            # Books with 50+ ratings in this user dataset
            final_filtered_data = users_with_200_ratings_data.loc[
                users_with_200_ratings_data.groupby('Book-Title')['Book-Rating'].transform('count') >= 50
            ]

            logging.info(f"Final filtered data shape: {final_filtered_data.shape}")
            
            # Saving filtered data as a pickle file
            logging.info("Saving the filtered data as a pickle file")
            save_object(file_path=self.helper_config.final_filtered_data_path, object=final_filtered_data)
            logging.info("Filtered data saved successfully")

        except Exception as e:
            logging.error("Error occurred while filtering the data")
            raise CustomException(e, sys)

    def pivot_table_data(self, filtered_data):
        """
        Creates a pivot table with:
        - Index: 'Book-Title'
        - Columns: 'User-ID'
        - Values: 'Book-Rating'
        
        Missing values are filled with 0. The result is then saved as a pickle file.
        """
        logging.info("Creating a pivot table")

        try:
            # Creating pivot table
            user_item_matrix = filtered_data.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')

            logging.info(f"Pivot table shape before filling NaNs: {user_item_matrix.shape}")

            # Filling missing values with 0
            logging.info("Filling missing values with 0")
            user_item_matrix.fillna(value=0, inplace=True)

            logging.info(f"Pivot table shape after filling NaNs: {user_item_matrix.shape}")

            # Saving the pivot table
            logging.info("Saving the pivot table data as a pickle file")
            save_object(file_path=self.helper_config.users_item_matrix_path, object=user_item_matrix)
            logging.info("Pivot table saved successfully")

        except Exception as e:
            logging.error("Error occurred while creating the pivot table")
            raise CustomException(e, sys)

    def similarity_score(self, pivot_table):
        """
        Computes cosine similarity between book rows in the pivot table.
        
        Parameters:
        pivot_table (pd.DataFrame): The user-book interaction matrix.
        
        Returns:
        np.ndarray: A square matrix containing cosine similarity scores.
        """
        logging.info("Calculating similarity scores")

        try:
            # Computing cosine similarity
            similarity_score = cosine_similarity(pivot_table)

            logging.info(f"Similarity matrix shape: {similarity_score.shape}")

            # Saving similarity scores as a pickle file
            logging.info("Saving the similarity scores as a pickle file")
            save_object(file_path=self.helper_config.similarity_scores_path, object=similarity_score)
            logging.info("Similarity scores saved successfully")

            return similarity_score

        except Exception as e:
            logging.error("Error occurred while calculating similarity score")
            raise CustomException(e, sys)

    def knn_model(self,final_filtered_data):
        logging.info("Training and saving the knn model")
        
        try:
            logging.info("Creating a book_pivot")
            book_pivot = final_filtered_data.pivot_table(index='ISBN', columns='User-ID', values='Book-Rating').fillna(0)
            
            #Saving the book_pivot a pickel file
            logging.info("Saving the book pivot file")
            save_object(file_path= self.helper_config.book_pivot_path, object= book_pivot)
            logging.info("Saved the book_pivot as pickle file")
            
            logging.info("Initializing the knn model")
            knn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=5, n_jobs=-1)
            
            logging.info("Training the knn model")
            knn_model.fit(book_pivot.values)
            
            #Saving the knn model as pickle file
            logging.info("Saving the knn model")
            save_object(file_path= self.helper_config.knn_model_path,object= knn_model)
            logging.info("KNN model saved successfully")
            
        except Exception as e:
            logging.info("Error occured while training and saving the knn model")
            raise CustomException(e,sys)
        
    def svd_model(self,final_filtered_data):
        logging.info("Training and saving the svd model")
        
        try:
            #Convert data to Surprise format
            logging.info("Converting the data into the format what svd accepts")
            reader = Reader(rating_scale=(0, 10))
            data = Dataset.load_from_df(final_filtered_data[["User-ID", "Book-Title", "Book-Rating"]], reader)
            
            # Train-test split
            logging.info("Train test split of the data")
            trainset, testset = train_test_split(data, test_size=0.2)
            
            #Best parameters
            logging.info("Definging the best parameters")
            best_params = {'n_factors': 100, 
               'n_epochs': 10, 
               'lr_all': 0.005, 
               'reg_all': 0.2}
            
            #Training the model
            logging.info("Trainig the best svd model")
            best_model = SVD(**best_params)
            best_model.fit(trainset)
            
            #Saving the knn model as pickle file
            logging.info("Saving the svd model")
            save_object(file_path= self.helper_config.svd_model_path,object= best_model)
            logging.info("svd model saved successfully")
            
        except Exception as e:
            logging.info("Error occured while training and saving the svd model")
            raise CustomException(e,sys)