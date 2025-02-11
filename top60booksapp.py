import streamlit as st
import pandas as pd
import pickle

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

def main():
    st.set_page_config(page_title="Book Recommender", layout="wide")
    
    # Load data
    books_data = load_books_data('artifacts/top_60_books.pkl')
    app = BookRecommendationApp(books_data)
    
    # Header Section
    st.markdown("""
        <div class="header-container">
            <h1>Premium Book Recommendations</h1>
            <p>Curated Collection of Top-Rated Titles</p>
        </div>
    """, unsafe_allow_html=True)

    # Main Content
    with st.container():
        app.display_books()

if __name__ == "__main__":
    main()
