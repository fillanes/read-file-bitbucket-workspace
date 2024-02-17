# The Purpose

The purpose of this script, was to obtain some values from a file, project-name and project-key, and added if they exist or not in a text file. To do that, script iterates over all workspace in bitbucket, first get a list of repositories separated by a pagination system (bitbucket api) and second, with the name of the repository call an url with the branch name and the file name.  

The script authentication can be managed by user and password or with Bearer token. It was tested with boths, but for my opinion y prefer the Bearer token.

All the request to the bitbucket api works inside while and for loops. 

Some of the problems ocurred during the requests, was a 429 http response from the api. That number mean **too many requests**. So in that case the script stopped and i had to run the script again. 

## Recomendations

I recommend use virtualenv and then install the requirements. Check the file repo_names.txt to validate the response of the script.

## To run the script

    python list-repo-name.py

