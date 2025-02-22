import streamlit as st
import requests
from src.components.recommender import BookRecommendationSystem

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
                background: linear-gradient(45deg, #4B79A1, #4CA1AF);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                text-align: center;
                margin-bottom: 1rem;
            }
            .recommendation-card {
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
                background: white;
                margin: 10px;
                text-align: center;
                max-width: 200px;
                overflow: hidden;
                min-height: 320px;
                border: 1px solid #e0e0e0;
            }
            .recommendation-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            .book-title {
                font-size: 1rem;
                font-weight: 600;
                margin: 10px 0 5px 0;
                color: #2F4F4F;
                line-height: 1.3;
                min-height: 2.8rem;
                word-wrap: break-word;
            }
            .book-author {
                font-size: 0.9rem;
                color: #666666;
                margin-bottom: 10px;
                word-wrap: break-word;
            }
            .error-message {
                background: #FFEBEE;
                color: #B71C1C;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #FFCDD2;
                margin: 20px 0;
            }
            /* Only the button alignment is changed below */
            .stButton>button {
                background: linear-gradient(45deg, #4B79A1, #4CA1AF);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
                /* Removed margin-top for better alignment with input */
                height: 3rem;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                white-space: nowrap;
                padding: 0 24px;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .footer {
                text-align: center;
                margin-top: 3rem;
                color: #666;
                font-size: 0.9rem;
            }
            .input-column {
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # App header
    st.markdown('<p class="title-text">📚 Book Recommendation Explorer</p>', unsafe_allow_html=True)
    st.markdown(
        """<div style="text-align: center; margin-bottom: 2rem; color: #666;">
            Discover personalized book recommendations based on your reading history
        </div>""",
        unsafe_allow_html=True
    )

    # Initialize recommender system
    recommender = BookRecommendationSystem()

    # Input section with aligned button
    col1, col2 = st.columns([4, 1])
    with col1:
        user_id = st.text_input("Enter your User ID", placeholder="e.g., 123456")
    with col2:
        st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
        recommend_button = st.button("🌟 Get My Recommendations")
        st.markdown("</div>", unsafe_allow_html=True)

    if recommend_button:
        if not user_id.strip():
            st.markdown(
                '<div class="error-message">⚠️ Please enter a User ID to get recommendations</div>',
                unsafe_allow_html=True
            )
        else:
            try:
                user_id_int = int(user_id)
                with st.spinner('🔍 Analyzing your reading preferences...'):
                    recommendations = recommender.get_top_recommendations(user_id_int)

                if 'message' in recommendations[0]:
                    st.markdown(
                        f'<div class="error-message">⚠️ {recommendations[0]["message"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.subheader(f"📖 Recommended for You (User {user_id})")
                    st.markdown("<br>", unsafe_allow_html=True)

                    # Create responsive columns
                    cols = st.columns(len(recommendations))
                    for idx, rec in enumerate(recommendations):
                        with cols[idx]:
                            card_content = f"""
                                <div class="recommendation-card">
                                    <img src="{rec['Image URL']}" 
                                        style="width:100%; 
                                               height:200px; 
                                               object-fit:contain;
                                               border-radius: 6px;
                                               margin-bottom: 12px;">
                                    <div class="book-title">{rec['Title']}</div>
                                    <div class="book-author">by {rec['Author']}</div>
                                </div>
                            """
                            st.markdown(card_content, unsafe_allow_html=True)
                    
                    # Footer
                    st.markdown(
                        """<div class="footer">
                            Recommendations powered by our advanced AI engine
                        </div>""",
                        unsafe_allow_html=True
                    )

            except ValueError:
                st.markdown(
                    '<div class="error-message">⚠️ Please enter a valid numeric User ID</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    run_app()
