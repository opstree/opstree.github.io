import os
import requests as github
import json, yaml

source_yaml_data = 'Open_Source_Input.yml'
output_yaml_file = 'Output_File.yml'


# To Load Input data in yml format
def getDictFromYaml(source_yaml_file):
    with open(source_yaml_data) as source_yaml:
        load_input_data = json.dumps(yaml.load(source_yaml, Loader=yaml.FullLoader))  # In String
        input_data_in_dict = json.loads(load_input_data)  # In Dictionary
        return input_data_in_dict

getDataFromYaml = getDictFromYaml(source_yaml_data)


# #To fetch the Username from github
def processUsers(getDataFromYaml):
    for users in getDataFromYaml['users']:
        github_username = users
        category = users

        # api url to fetch github data
        api_url = f"https://api.github.com/users/{github_username}"

        # send get request to github API
        github_response = github.get(api_url)
        data = github_response.json()
        repo_link = data["repos_url"]
        github_repo_link = github.get(repo_link)

        # Convert the API result into json format
        repo_data = github_repo_link.json()

        final_data = []  # Data in Array format

        # Append all the required fetched repo info into the array
        for i in range(len(repo_data)):
            Required_info = dict(Name=repo_data[i]["name"],
                                 description=(repo_data[i]["description"]),
                                 repo=(repo_data[i]["html_url"]))
            final_data.append(Required_info)
        output_data = ({category: final_data})

        # Write the yaml file with the required data
        try:
            out = open(output_yaml_file, mode='r').read()
            if ((os.path.exists(output_yaml_file)) == False):
                raise FileNotFoundError("File not found")          
            if yaml.safe_dump(output_data, default_flow_style=False) not in out:
                with open(output_yaml_file, 'a') as out:
                    out.write(yaml.safe_dump(output_data, default_flow_style=False))
            print(f"Yaml for User {github_username} has been generated")

        except FileNotFoundError:
            open('Output_File.yml', "w").close()
            out = open(output_yaml_file, mode='r').read()
            if yaml.safe_dump(output_data, default_flow_style=False) not in out:
                print(output_yaml_file)
                with open(output_yaml_file, 'a') as out:
                    out.write(yaml.safe_dump(output_data, default_flow_style=False))
            print(f"Yaml for User {github_username} has been generated")


# To fetch the Organizations data from github
def processOrgs(getDataFromYaml):
    for orgs in getDataFromYaml['orgs']:
        github_orgs = orgs
        category = orgs.split("-")[1]

        # api url to fetch github data
        api_url = f"https://api.github.com/orgs/{github_orgs}"

        # send get request to github API
        github_response = github.get(api_url)
        data = github_response.json()
        repo_link = data["repos_url"]
        github_repo_link = github.get(repo_link)

        # Convert the API result into json format
        repo_data = github_repo_link.json()

        final_data = []  # Data in Array format

        # Append all the required fetched repo info into the array

        for i in range(len(repo_data)):
            Required_info = dict(Name=repo_data[i]["name"],
                                 description=(repo_data[i]["description"]),
                                 repo=(repo_data[i]["html_url"]))
            final_data.append(Required_info)

        output_data = ({category: final_data})

        # Write the yaml file with the required data
        try:
            out = open(output_yaml_file, mode='r').read()
            if ((os.path.exists(output_yaml_file)) == False):
                raise FileNotFoundError("File not found")
                print(output_yaml_file)
            if yaml.safe_dump(output_data, default_flow_style=False) not in out:
                print(output_yaml_file)
                with open(output_yaml_file, 'a') as out:
                    out.write(yaml.safe_dump(output_data, default_flow_style=False))
            print(f"Yaml for Organization {github_orgs} has been generated")

        except FileNotFoundError:
            open('Output_File.yml', "w").close()


processUsers(getDataFromYaml)
processOrgs(getDataFromYaml)
