import boto3
from simple_term_menu import TerminalMenu


bucket_name = '<bucket name>'
aws_profile = '<aaws profile name>'


boto3_session = boto3.session.Session(profile_name=aws_profile)
s3_client = boto3_session.client('s3')


selected_folder="" # Start off with empty string to get top level folder list


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

    # Display the menu to select the folder
    folder_menu = TerminalMenu(folders)
    folder_menu_selection_index = folder_menu.show()

    # Populate the selected_folder variable with the full key seleted
    selected_folder=folder_paths[folder_menu_selection_index]


# Catch in case there were no folders in the bucket
if selected_folder == "":
    print("No folders found in bucket.")



# End of tree reached, can ask user if they would like to download the folder or browse and download single files


# Get the list of files in the folder the user selected
files_in_selected_folder = s3_client.list_objects_v2(Bucket = bucket_name, Prefix=selected_folder) 

# Remove the path prefix from each file
files: list = []
for file in files_in_selected_folder['Contents']:
    files.append(file['Key'][len(selected_folder):])

# Display the menu to select the folder
file_menu = TerminalMenu(files)
file_menu_selection_index = file_menu.show()

selected_file=files_in_selected_folder['Contents'][file_menu_selection_index]['Key']

print(selected_file)

s3_client.download_file(bucket_name, selected_file, selected_file[len(selected_folder):])


