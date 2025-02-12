from src.components.helper import Helper
from src.utils import load_object

if __name__ == "__main__":
    ##Artifacts
    #Create object of the helper class
    helper_obj = Helper() 
    
    #Saving the filtered data file
    helper_obj.filter_data()
    
    #Loading the filtered data        
    books_dataset = load_object(file_path=helper_obj.helper_config.final_filtered_data_path)
            
    #Saving the pivot table data        
    helper_obj.pivot_table_data(filtered_data=books_dataset)
    
    #Loading the pivot table 
    books_titles = load_object(file_path=helper_obj.helper_config.users_books_pivot_table_path)
    
    #Saving thr similarity_score data
    helper_obj.similarity_score(pivot_table=books_titles)
