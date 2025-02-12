from src.components.datacleaning import DataIngestion

if __name__ == "__main__":
    #Data Cleaning
    #Create a object for data cleaning/Ingestion class
    object_dataIngestion = DataIngestion()
    
    #Loading the data sets
    raw_books_df,raw_ratings_df,raw_users_df = object_dataIngestion.initiate_data_ingestion()
    
    #Spliting the laction feature
    splitted_users_df = object_dataIngestion.split_location(users_df= raw_users_df)
    
    #Handling the nan values of books dataset
    null_val_free_books_df = object_dataIngestion.handle_nullvalues_booksdataset(books_df= raw_books_df)
    
    #Dropping the urls of books
    url_dropped_books_df = object_dataIngestion.remove_imageUrls(books_df= null_val_free_books_df)
    
    #Cleanning the year of publication feature
    cleaned_year_of_publication_books_df = object_dataIngestion.clean_year_of_publication(books_df= url_dropped_books_df)
    
    #Merging all the cleaned datasets
    merged_df = object_dataIngestion.megring_datasets(users_df= splitted_users_df,
                                     ratings_df= raw_ratings_df,
                                     books_df= cleaned_year_of_publication_books_df)
    
    #Cleaning the age feature of the data set
    cleaned_merged_df = object_dataIngestion.handling_age_nan_values(final_merged_df= merged_df)
    
    #Saving the cleaned file
    object_dataIngestion.save_cleaned_csv(df=cleaned_merged_df)