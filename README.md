# Book Recommendation System

## Overview
This project is a **Book Recommendation System** that suggests 5 books based on a given input book. The system utilizes data analysis and machine learning techniques to find similarities between books and generate relevant recommendations.

## Features
- Provides book recommendations based on user input
- Uses **collaborative filtering** and **content-based filtering** techniques
- Conducts **Exploratory Data Analysis (EDA)** to understand data distribution
- Built with **Streamlit** for an interactive web application
- Deployed on **Streamlit Cloud** for easy accessibility

## Dataset
- Source: **Kaggle Dataset**
- Contains book details, ratings, and user interactions

## Installation & Usage

### 1. Set Up the Environment
```bash
conda create --name book-recommender python=3.12 -y
conda activate book-recommender
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Data Preprocessing Pipeline
```bash
python datacleaningpipeline.py
python artifactspipeline.py
```

### 4. Run the Streamlit App
```bash
streamlit run recommendationsystemapp.py
```

## Libraries Used
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **seaborn** - Data visualization
- **matplotlib** - Plotting graphs
- **scipy** - Scientific computing
- **scikit-learn** - Machine learning algorithms
- **streamlit** - Web application framework

## Key Insights from EDA
- The dataset contains user ratings and book metadata.
- Popular books have higher user engagement.
- Rating distributions show a preference for certain genres.
- Similar books can be grouped based on textual and rating similarities.

## Deployment
- The application is deployed on **Streamlit Cloud** for public access.


