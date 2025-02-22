import sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object

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
            self.final_filtered_data = load_object('artifacts/final_filtered_data.pkl')
            #self.book_pivot = load_object('artifacts/book_pivot.pkl')
            #self.knn_model = load_object('artifacts/knn_model.pkl')
            #self.svd_model = load_object('artifacts/svd_model.pkl')
            self.user_item_matrix = load_object('artifacts/user_item_matrix.pkl')
            self.user_similarity_matrix = load_object('artifacts/user_similarity_matrix.pkl')

            '''
            # Precompute nearest neighbors
            self.knn_neighbors = {}
            for idx in range(len(self.book_pivot)):
                distances, indices = self.knn_model.kneighbors([self.book_pivot.iloc[idx].values], n_neighbors=6)
                self.knn_neighbors[self.book_pivot.index[idx]] = self.book_pivot.iloc[indices.flatten()[1:]].index.tolist()
            '''
            logging.info("Book Recommendation System Initialized Successfully")

        except Exception as e:
            logging.error("Error occurred during initialization")
            raise CustomException(e, sys)
    
    def get_top_recommendations(self, user_id, top_n=5):
        """
        Retrieves the top N book recommendations based on SVD and KNN similarity.
        """
        try:
            logging.info(f"Fetching top {top_n} recommendations for: {user_id}")
            
            # ----------------
            # Hybrid Method
            # ----------------
            '''
            # Step 1: Get SVD-based Recommendations
            all_books = set(self.final_filtered_data['ISBN'].unique())
            user_rated_books = set(self.final_filtered_data[self.final_filtered_data['User-ID'] == user_id]['ISBN'].values)
            books_to_predict = list(all_books - user_rated_books)

            # Batch prediction for efficiency
            predictions = self.svd_model.test([(user_id, book, 0) for book in books_to_predict])
            predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
            svd_books = [pred.iid for pred in predictions]

            # Step 2: Get KNN-based Recommendations (precomputed)
            final_recommendations = set(svd_books)
            for book in svd_books:
                final_recommendations.update(self.knn_neighbors.get(book, []))

            top_recommendations = list(final_recommendations)[:top_n]
            '''
            
            # -------------------------
            # Cosine Similarity Method
            # -------------------------
            
            similar_users_cs  = self.user_similarity_matrix[user_id].sort_values(ascending=False)[1:6].index
            books_rated_by_user = set(self.user_item_matrix.columns[self.user_item_matrix.loc[user_id] > 0])
            
            recommended_books = {}

            for sim_user in similar_users_cs:
                sim_user_books = self.user_item_matrix.loc[sim_user]
                for book, rating in sim_user_books.items():
                    if book not in books_rated_by_user and rating > 0:
                        recommended_books[book] = recommended_books.get(book, 0) + rating
            recommended_books = sorted(recommended_books.items(), key=lambda x: x[1], reverse=True)[:5]
            
            result = []
            for book_data in recommended_books:
                book_info = self.final_filtered_data[self.final_filtered_data['Book-Title'] == book_data[0]].iloc[0]
                result.append({
                    "Title": book_info["Book-Title"],
                    "Author": book_info["Book-Author"],
                    "Image URL": book_info["Image-URL-M"]
                })
            
            return result
        
        except Exception as e:
            logging.error("Error occurred while generating recommendations")
            raise CustomException(e, sys)
