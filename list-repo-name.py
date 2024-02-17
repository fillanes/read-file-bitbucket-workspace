import requests

# Configuration of values can be by auth user and password, or token
# bitbucket_username = 'fillanes'
# bitbucket_password = '*****' 
headers = {'Authorization': f'Bearer *****'}
workspace = 'work_space_name' # workspace
search_file = 'file_name'  # file path
branch = 'development' # branch name
page_len = '25' # Page length of the request to obtain list or repos. Max number is 100
project_key = '' 
project_name = '' 
total_values = True # Conditional used to stop the loop in case of change

# Page number. If the script stop by 429 http error, or other option you can chenge this parameter with the last paged executed.
page_number = 1 

while total_values != False:

    repo_url = f'https://api.bitbucket.org/2.0/repositories/{workspace}?page={str(page_number)}&pagelen={page_len}'

    # repo_response = requests.get(repo_url, auth=HTTPBasicAuth(bitbucket_username, bitbucket_password))
    repo_response = requests.get(repo_url, headers=headers)

    if repo_response.status_code == 200:
        json_data = repo_response.json()

        if json_data['values'] == []:
            print('json_data está vacio')
            total_values = False

        # OObtain the name of the repositories
        repo_names = [repo['name'] for repo in json_data.get('values', [])]

        # Print the name of a repository
        for repo_name in repo_names:
            print(f"Nombre del repositorio: {repo_name}")

            file_url = f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/src/{branch}/{search_file}'

            # file_response = requests.get(file_url, auth=HTTPBasicAuth(bitbucket_username, bitbucket_password))
            file_response = requests.get(file_url, headers=headers)
            print(file_response)

            if file_response.status_code == 200:
                lines = file_response.text.split('\n')

                for line in lines:

                    if "PROJECT_NAME=" in line:
                        project_name = line
                    
                    if "PROJECT_KEY=" in line:
                        project_key = line

                with open('repo_names.txt', 'a') as file:
                    # If was http 200 , add all context to the file
                    file.write(str(file_response.status_code) + ',' + str(repo_name) + ',' + str(search_file) + ',' + str(branch) + ',' + project_name.strip() + ',' + project_key.strip() + '\n')
            
            elif file_response.status_code == 404:

                with open('repo_names.txt', 'a') as file:
                    # If was http 404 , only add http status code, repository name and file searched
                    file.write(str(file_response.status_code) + ',' + str(repo_name) + ',' + str(search_file) + ',' + str(branch) + ',' + ',' +  '\n')

            else: 
                print('Ups! page_number: ' + str(page_number))
                total_values = False

                with open('repo_names.txt', 'a') as file:
                    # If was http 429 , the script stop
                    file.write(str(file_response.status_code) + ',' + str(repo_name) + ',' + str(search_file) + ',' + str(branch) + ',' + ',' +  '\n')
                break

        print('page_number: ' + str(page_number)) # Print that show the next page (consider -1 to re run the script)
        page_number += 1
    else:
        print(f"Error en la solicitud: {repo_response.status_code}")
        break  # Quit bucle