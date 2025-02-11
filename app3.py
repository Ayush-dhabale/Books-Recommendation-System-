import streamlit as st
import pandas as pd
import pickle
import requests

# First App Class: BookRecommendationApp (Displays top 60 curated books)
class BookRecommendationApp:
    def __init__(self, books_data):
        self.books_data = books_data
        self._inject_custom_css()

    def _inject_custom_css(self):
        """Inject custom CSS for overall styling"""
        st.markdown("""
            <style>
            :root {
                --primary-color: #4A90E2;
                --secondary-color: #6E48AA;
                --accent-color: #9D50BB;
                --text-color: #2C3E50;
                --background-color: #F9F9F9;
            }

            html {
                font-family: 'Segoe UI', system-ui, sans-serif;
            }

            .main {
                background-color: var(--background-color);
            }

            .book-card {
                background: white;
                border-radius: 12px;
                padding: 1.2rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                overflow: hidden;
            }

            .book-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            }

            .book-image-container {
                width: 100%;
                height: 220px;
                border-radius: 8px;
                overflow: hidden;
                margin-bottom: 1rem;
                background: #f8f9fa;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .book-image {
                max-height: 100%;
                width: auto;
                border-radius: 4px;
                transition: transform 0.3s ease;
            }

            .book-title {
                color: var(--text-color);
                font-weight: 600;
                font-size: 1.1rem;
                line-height: 1.4;
                margin-bottom: 0.5rem;
                height: 60px;
                overflow: hidden;
                text-align: center;
                padding: 0.5rem;
                background-color: var(--primary-color);
                color: white;
                border-radius: 8px;
                text-overflow: ellipsis;
            }

            .book-author {
                color: #6C757D;
                font-size: 0.95rem;
                text-align: center;
                margin-bottom: 1rem;
                font-style: italic;
            }

            .rating-badge {
                background: linear-gradient(135deg, #ffd700 0%, #ffb300 100%);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.9rem;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                margin: 0 auto;
            }

            .votes-badge {
                background: #e9ecef;
                color: var(--text-color);
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            .stats-container {
                display: flex;
                justify-content: center;
                gap: 1rem;
                margin-top: auto;
                padding-top: 1rem;
            }

            .book-card-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 1.5rem;
                padding: 1rem 0;
            }

            .header-container {
                background: linear-gradient(135deg, #4A90E2 0%, #6E48AA 100%);
                padding: 3rem 1rem;
                border-radius: 0 0 20px 20px;
                margin-bottom: 2.5rem;
                text-align: center;
                color: white;
            }

            .header-container h1 {
                font-weight: 700;
                margin: 0;
                font-size: 2.8rem;
            }

            .header-container p {
                font-size: 1.1rem;
                opacity: 0.95;
                margin-top: 0.5rem;
            }

            </style>
        """, unsafe_allow_html=True)

    def _create_book_card(self, book):
        """Generate HTML for a single book card"""
        return f"""
        <div class="book-card">
            <div class="book-image-container">
                <img src="{book['Image-URL-M']}" class="book-image" alt="{book['Book-Title']}">
            </div>
            <h3 class="book-title">{book['Book-Title']}</h3>
            <p class="book-author">{book['Book-Author']}</p>
            <div class="stats-container">
                <div class="rating-badge">
                    ★ {book['avg_of_ratings']:.2f}
                </div>
                <div class="votes-badge">
                    👥 {book['num_of_ratings']:,}
                </div>
            </div>
        </div>
        """

    def display_books(self):
        """Display books in a responsive grid layout"""
        st.markdown('<div class="book-card-container">', unsafe_allow_html=True)

        for _, book in self.books_data.iterrows():
            st.markdown(self._create_book_card(book), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def load_books_data(pickle_file):
    """Load books data from pickle file."""
    with open(pickle_file, 'rb') as file:
        return pickle.load(file)


# Second App Class: BookRecommendationSystem (Searches for book recommendations)
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


# Main Streamlit App Logic
def main():
    st.set_page_config(page_title="Book Recommender", layout="wide")

    # Sidebar to choose between the apps
    app_choice = st.sidebar.radio("Choose an option", ["Top 60 Curated Books", "Book Recommendations by Title"])

    # Load the curated books data
    books_data = load_books_data('artifacts/top_60_books.pkl')
    app = BookRecommendationApp(books_data)

    # Handle the selection from sidebar
    if app_choice == "Top 60 Curated Books":
        # Display curated book recommendations
        st.markdown("""
            <div class="header-container">
                <h1>Premium Book Recommendations</h1>
                <p>Curated Collection of Top-Rated Titles</p>
            </div>
        """, unsafe_allow_html=True)
        app.display_books()

    elif app_choice == "Book Recommendations by Title":
        # Keep the original layout for book recommendations
        st.markdown('<p class="title-text">📚 Book Recommendation Explorer</p>', unsafe_allow_html=True)

        # Initialize recommender system
        recommender = BookRecommendationSystem(
            similarity_matrix_file='artifacts/similarity_scores.pkl', 
            pivot_table_file='artifacts/user_book_pt.pkl', 
            dataset_file='artifacts/final_filtered_data.pkl'
        )

        # Search input
        book_title = st.text_input(
            " ",
            placeholder="Enter Book Title",
            max_chars=100,
            label_visibility="collapsed",
            key="book_input"
        ).strip()

        if book_title:
            recommendations = recommender.get_top_recommendations(book_title)
            if "message" in recommendations[0]:
                st.error(recommendations[0]["message"])
            else:
                st.write(f"### Recommendations for '{book_title}':")
                for rec in recommendations:
                    st.write(f"**Title:** {rec['Title']}")
                    st.write(f"**Author:** {rec['Author']}")
                    st.image(rec['Image URL'], use_container_width=True)

if __name__ == "__main__":
    main()
