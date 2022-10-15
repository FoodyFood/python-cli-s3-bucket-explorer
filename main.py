import os
import boto3
from simple_term_menu import TerminalMenu


bucket_name = '<bucket name>'
aws_profile = '<aaws profile name>'


# Create our boto3 session and client using the desired credentials
boto3_session = boto3.session.Session(profile_name=aws_profile)
s3_client = boto3_session.client('s3')


# Start off with empty string to get top level folder list
selected_folder=""


# Alow the user to select folders till we run out of folders to select and break
while True:
    # Get list of folders in current selected_folder (if empty string, get's top level folders)
    list_of_objects = s3_client.list_objects(Bucket=bucket_name, Prefix=selected_folder, Delimiter="/")

    # If there are no folders, exit the while loop
    if 'CommonPrefixes' not in list_of_objects:
        break

    # Extract the folder paths from the list of objects
    folder_paths = [x['Prefix'] for x in list_of_objects['CommonPrefixes']]

    # Remove the start of each folder path so we display only the current folders in the menu, not the whole path
    folders: list = []
    for folder_path in folder_paths:
        folders.append(folder_path[len(selected_folder):-1])
    
    if "/" in selected_folder:
        folders.append("Back To Previous Folder")
    folders.append("Exit Bucket Browser")

    # Display the menu to select the folder
    folder_menu = TerminalMenu(folders)
    folder_menu_selection_index = folder_menu.show()

    # If user wants to navigate up a folder, remove the last flder name from the path and reapend the "/" if needed
    if folders[folder_menu_selection_index] == "Back To Previous Folder":
        selected_folder = ("/".join(selected_folder.split("/")[:-2]))
        if selected_folder != "":
                selected_folder = selected_folder + "/"
                
    # If the user wants to exit the downoad menu
    elif folders[folder_menu_selection_index] == "Exit Bucket Browser":
        exit()

    # Otherwise, we populate the selected_folder variable with the full key seleted
    else:
        selected_folder=folder_paths[folder_menu_selection_index]



# Print the full path of the older the user landed on
print(f"\nSelected Folder: {selected_folder}\n")


# Catch in case there were no folders in the bucket
if selected_folder == "":
    print("No folders found in bucket.")


# End of tree reached, ask the user if they would like to download the folder or browse and download single files
print("No more folder levels, would you like to:\n")
download_options=["Download Single File From The Folder", "Download The Complete Folder", "Exit Download Menu"]
download_menu = TerminalMenu(download_options)
download_menu_selection_index = download_menu.show()


# In case the user jsut wanted to browse files, not download them
if(download_options[download_menu_selection_index] == "Exit Download Menu"):
    print("Exiting Download Menu")
    exit()


# Get the list of files in the folder the user selected
files_in_selected_folder = s3_client.list_objects_v2(Bucket = bucket_name, Prefix=selected_folder) 


# If user wants to download a single file, we displayy a menu to select the file
if(download_options[download_menu_selection_index] == "Download Single File From The Folder"):
    # Remove the path prefix from each file
    files: list = []
    for file in files_in_selected_folder['Contents']:
        files.append(file['Key'][len(selected_folder):])

    # Display the menu to select the file
    file_menu = TerminalMenu(files)
    file_menu_selection_index = file_menu.show()
    selected_file=files_in_selected_folder['Contents'][file_menu_selection_index]['Key']

    # Download the selected file
    print("Downloading: " + selected_file)
    s3_client.download_file(bucket_name, selected_file, selected_file[len(selected_folder):])
    print("")


# If the user wants to download the whole folder, we just loop over the files one by one and download them
if(download_options[download_menu_selection_index] == "Download The Complete Folder"):
    print(f"Downloading {len(files_in_selected_folder['Contents'])} files..\n")
    confirm_download_folder = input("Are you sure you want to download these files? (y/n) ")
    if(confirm_download_folder == 'N' or confirm_download_folder == 'n'):
        print("Download aborted, no files downloaded.\n")
        exit()

    elif (confirm_download_folder == 'Y' or confirm_download_folder == 'y'):
        # Create a folder of the same name as the one we are downloading, in the current directory, if it doesnt exist
        folder_to_download_into = selected_folder.split('/')[-2]
        if not os.path.exists(folder_to_download_into):
            os.mkdir(folder_to_download_into)

        # Loop over al the files to download, and put them in the folder
        for file in files_in_selected_folder['Contents']:
            selected_file = file['Key']
            print("Downloading: " + file['Key'][len(selected_folder):])
            s3_client.download_file(bucket_name, selected_file, f"{folder_to_download_into}/" + selected_file[len(selected_folder):])

    else:
        print("y/n or Y/N only.")


