import pickle
import os
import sys
from src.logger import logging
from src.exception import CustomException

# Create a class for book recommendation system
class BookRecommendationSystem:
    def __init__(self, similarity_matrix_file, pivot_table_file, dataset_file):
        try:
            logging.info("The recommendation starts")
            logging.info("Loading the pickle files")
            self.similarity_matrix = self.load_pickle(similarity_matrix_file)
            self.book_titles = self.load_pickle(pivot_table_file).index
            self.book_dataset = self.load_pickle(dataset_file)
            logging.info("Loaded the pickle files")
        except Exception as e:
            logging.error(f"Error occurred during initialization: {str(e)}")
            raise CustomException("Error occurred while initializing the BookRecommendationSystem")

    def load_pickle(self, file_path):
        """Loads a pickled file."""
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            logging.error(f"Error occurred during loading pickle file {file_path}: {str(e)}")
            raise CustomException(f"Error occurred while loading the pickle file: {file_path}")
    
    def get_top_recommendations(self, book_title, top_n=5):
        """
        Retrieves the top N book recommendations based on cosine similarity, along with Title, Author, and Image URL.
        """
        try:
            logging.info("Recommendation Starts")
            if book_title not in self.book_titles:
                logging.info("Error occurred during book_title searching")
                return [{"message": "Book not found in dataset"}]

            logging.info("Extracting the index of the entered book title")
            book_idx = self.book_titles.get_loc(book_title)
            similarity_scores = list(enumerate(self.similarity_matrix[book_idx]))
            logging.info("Sorting the similarity scores")
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

            top_recommendations = []
            logging.info("Extracting the top recommendations")
            for i, _ in similarity_scores[1:top_n+1]:
                book_info = self.book_dataset[self.book_dataset['Book-Title'] == self.book_titles[i]].iloc[0]
                top_recommendations.append({
                    "Title": book_info["Book-Title"],
                    "Author": book_info["Book-Author"],
                    "Image URL": book_info["Image-URL-M"]
                })
            
            return top_recommendations
        
        except Exception as e:
            logging.error(f"Error occurred during recommendation generation: {str(e)}")
            raise CustomException("Error occurred while generating recommendations")
