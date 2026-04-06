import os 
import requests

def download_answer_files(cloud_url, path_to_data_folder, respondent_index): 
    url = cloud_url 
    
    for i in range (1, respondent_index + 1): 
        file_url = f"{url}/a{i}.txt"
        response = requests.get(file_url) 
        
        """
        This generates the URL of each respondent from 1 inclusive of the last
        respondent. 
        Then requests pulls the file
        """
        
        if response.status_code == 200: 
            
            """
            200 is used because it shows there's no error. e.g. if the status
            code was 404, it would return an error
            """
            
            file_path = os.path.join(path_to_data_folder,f"answers_respondent_{i}.txt")
            
            """
            This defines the output files from this function of all respondents
            {i} is used from the for loop to makes sure all answer files are 
            the same value as their corrospondent respondent files
            """

            with open(file_path, "w") as f: 
                f.write(response.text)
            
            print(f"Saved answers_respondent_{i}.txt")
            
            """
            This puts the file into the correct space in the repository
            """

        else:
            print(f"Could not download a{i}.txt")
            
            """
            e.g. could be due to an 404 error code if file does not exist
            """
            
def collate_answer_files(data_folder_path): 
    files = sorted(os.listdir(data_folder_path))
    
    """
    sorted makes sure that all the files are in the correct order
    e.g. 1,2,3,4 and not 4,2,1,3
    """
    
    with open("output/collated_answers.txt", "w") as outfile:
        
        """
        Creates a file that the outputed file will go into
        """

        for file_name in files:

            file_path = os.path.join(data_folder_path, file_name)
            
            """
            combines the folder path and name
            """

            with open(file_path, "r") as infile:
                content = infile.read()
            outfile.write(content)
            outfile.write("\n*\n")
            
            """
            creates a seperator so that there will be an asteriks between
            each file's content
            """ 
