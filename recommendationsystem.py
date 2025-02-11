import streamlit as st
import pickle
import requests

class BookRecommendationSystem:
    def __init__(self, similarity_matrix_file, pivot_table_file, dataset_file):
        self.similarity_matrix = self.load_pickle(similarity_matrix_file)
        self.book_titles = self.load_pickle(pivot_table_file).index
        self.book_dataset = self.load_pickle(dataset_file)
        
    def load_pickle(self, file_path):
        """Loads a pickled file."""
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    
    def get_top_recommendations(self, book_title, top_n=5):
        """
        Retrieves the top N book recommendations based on cosine similarity, along with Title, Author, and Image URL.
        """
        if book_title not in self.book_titles:
            return [{"message": "Book not found in dataset"}]

        book_idx = self.book_titles.get_loc(book_title)
        similarity_scores = list(enumerate(self.similarity_matrix[book_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        top_recommendations = []
        for i, _ in similarity_scores[1:top_n+1]:
            book_info = self.book_dataset[self.book_dataset['Book-Title'] == self.book_titles[i]].iloc[0]
            top_recommendations.append({
                "Title": book_info["Book-Title"],
                "Author": book_info["Book-Author"],
                "Image URL": book_info["Image-URL-M"]
            })
        
        return top_recommendations


# Streamlit App
def run_app():
    # Custom CSS styling
    st.markdown("""
        <style>
            .main .block-container {
                max-width: 1200px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .title-text {
                font-size: 2.5rem;
                font-weight: 700;
                color: #2F4F4F;
                text-align: center;
                margin-bottom: 1.5rem;
            }
            .recommendation-card {
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
                background: white;
                margin: 10px;
            }
            .recommendation-card:hover {
                transform: translateY(-3px);
            }
            .book-title {
                font-size: 1.1rem;
                font-weight: 600;
                margin: 15px 0 8px 0;
                color: #2F4F4F;
                line-height: 1.3;
                min-height: 3.4rem;
            }
            .book-author {
                font-size: 0.9rem;
                color: #666666;
                margin-bottom: 12px;
            }
            .stTextInput>div>div>input {
                padding: 12px 18px;
                border-radius: 25px;
            }
            .error-message {
                background: #FFEBEE;
                color: #B71C1C;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #FFCDD2;
                margin: 20px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # App header
    st.markdown('<p class="title-text">📚 Book Recommendation Explorer</p>', unsafe_allow_html=True)

    # Initialize recommender system
    recommender = BookRecommendationSystem(
        similarity_matrix_file='artifacts/similarity_scores.pkl', 
        pivot_table_file='artifacts/user_book_pt.pkl', 
        dataset_file='artifacts/final_filtered_data.pkl'
    )

    # Search input
    with st.container():
        book_title = st.text_input(
            " ",
            placeholder="Enter a book title you enjoy... (e.g., The Hobbit)",
            key="book_search"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    if book_title:
        with st.spinner('Discovering great recommendations...'):
            recommendations = recommender.get_top_recommendations(book_title)

        if 'message' in recommendations[0]:
            st.markdown(
                f'<div class="error-message">⚠️ {recommendations[0]["message"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.subheader(f"Recommended reads for fans of *{book_title}*")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create responsive columns
            cols = st.columns(len(recommendations))
            for idx, rec in enumerate(recommendations):
                with cols[idx]:
                    card_content = f"""
                        <div class="recommendation-card">
                            <img src="{rec['Image URL']}" 
                                style="width:100%; 
                                       height:220px; 
                                       object-fit:contain;
                                       border-radius: 6px;">
                            <div class="book-title">{rec['Title']}</div>
                            <div class="book-author">by {rec['Author']}</div>
                        </div>
                    """
                    st.markdown(card_content, unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    run_app()