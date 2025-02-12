import sys
from src.logger import logging
from src.exception import CustomException
from src.components.helper import Helper
from src.utils import load_object

# Create a class for the Book Recommendation System
class BookRecommendationSystem:
    """
    A book recommendation system that filters data, creates pivot tables, 
    computes similarity scores, and provides top book recommendations.
    """
    
    def __init__(self):
        """
        Initializes the recommendation system by loading necessary data and computing similarity scores.
        """
        logging.info("Book Recommendation System Initialization Started")
        
        try:
            logging.info("Creating an instance of the Helper class")
            self.helper_obj = Helper()
            
            logging.info("Filtering data and saving as a pickle file")
            self.helper_obj.filter_data()
            
            logging.info("Loading the filtered dataset")
            self.books_dataset = load_object(file_path=self.helper_obj.helper_config.final_filtered_data_path)
            
            logging.info("Creating a pivot table and saving as a pickle file")
            self.helper_obj.pivot_table_data(filtered_data=self.books_dataset)
            
            logging.info("Loading the pivot table index (Book Titles)")
            self.books_titles = load_object(file_path=self.helper_obj.helper_config.users_books_pivot_table_path).index
            
            logging.info("Computing similarity scores and saving as a pickle file")
            self.helper_obj.similarity_score(pivot_table=self.books_titles)
            
            logging.info("Loading the similarity matrix")
            self.similarity_matrix = load_object(file_path=self.helper_obj.helper_config.similarity_scores_path)
            
            logging.info("Book Recommendation System Initialization Completed Successfully")
        
        except Exception as e:
            logging.error("Error occurred during initialization")
            raise CustomException(e, sys)
    
    def get_top_recommendations(self, book_title, top_n=5):
        """
        Retrieves the top N book recommendations based on cosine similarity.

        Parameters:
        book_title (str): The title of the book for which recommendations are needed.
        top_n (int): The number of recommendations to return.

        Returns:
        list: A list of dictionaries containing the recommended books' Title, Author, and Image URL.
        """
        try:
            logging.info(f"Fetching top {top_n} recommendations for: {book_title}")
            
            if book_title not in self.books_titles:
                logging.warning("Book not found in the dataset")
                return [{"message": "Book not found in dataset"}]

            logging.info("Extracting the index of the entered book title")
            book_idx = self.books_titles.get_loc(book_title)
            
            logging.info("Computing similarity scores")
            similarity_scores = list(enumerate(self.similarity_matrix[book_idx]))
            
            logging.info("Sorting the similarity scores in descending order")
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

            top_recommendations = []
            logging.info("Extracting the top recommended books")
            
            for i, _ in similarity_scores[1:top_n + 1]:
                book_info = self.books_dataset[self.books_dataset['Book-Title'] == self.books_titles[i]].iloc[0]
                
                top_recommendations.append({
                    "Title": book_info["Book-Title"],
                    "Author": book_info["Book-Author"],
                    "Image URL": book_info["Image-URL-M"]
                })

            logging.info("Successfully retrieved top recommendations")
            return top_recommendations
        
        except Exception as e:
            logging.error("Error occurred while generating recommendations")
            raise CustomException(e, sys)
