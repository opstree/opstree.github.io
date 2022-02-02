import os
import requests as github
import json, yaml

SOURCE_YAML_DATA = '../ot-git-details-source.yml'
OUTPUT_YAML_DATA = 'ot-osc-repo-info.yml'


# To Load Input data in yml format
def getDictFromYaml(source_yaml_file):
    with open(SOURCE_YAML_DATA) as source_yaml:
        load_input_data = json.dumps(yaml.load(source_yaml, Loader=yaml.FullLoader))  # In String
        input_data_in_dict = json.loads(load_input_data)  # In Dictionary
        return input_data_in_dict

# To fetch the Username from github
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
        for repo in range(len(repo_data)):
            Required_info = dict(Name=repo_data[repo]["name"],
                                 description=(repo_data[repo]["description"]),
                                 repo=(repo_data[repo]["html_url"]))
            final_data.append(Required_info)
        output_data = ({category: final_data})

        # Write the yaml file with the required data
        try:
            yaml_output = open('../'+ OUTPUT_YAML_DATA, mode='r').read()
            if ((os.path.exists('../'+ OUTPUT_YAML_DATA)) == False):
                raise FileNotFoundError("File not found")
            if yaml.safe_dump(output_data, default_flow_style=False) not in yaml_output:
                with open('../'+ OUTPUT_YAML_DATA, 'a') as yaml_output:
                    yaml_output.write(yaml.safe_dump(output_data, default_flow_style=False))
            print(f"Yaml for User {github_username} has been generated")

        except FileNotFoundError:
            open('../'+ OUTPUT_YAML_DATA, "w").close()
            yaml_output = open('../'+ OUTPUT_YAML_DATA, mode='r').read()
            if yaml.safe_dump(output_data, default_flow_style=False) not in yaml_output:
                with open('../'+ OUTPUT_YAML_DATA, 'a') as yaml_output:
                    yaml_output.write(yaml.safe_dump(output_data, default_flow_style=False))
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

        for repo in range(len(repo_data)):
            Required_info = dict(Name=repo_data[repo]["name"],
                                 description=(repo_data[repo]["description"]),
                                 repo=(repo_data[repo]["html_url"]))
            final_data.append(Required_info)

        output_data = ({category: final_data})

        # Write the yaml file with the required data
        try:
            yaml_output = open('../'+ OUTPUT_YAML_DATA, mode='r').read()
            if ((os.path.exists('../'+ OUTPUT_YAML_DATA)) == False):
                raise FileNotFoundError("File not found")
            if yaml.safe_dump(output_data, default_flow_style=False) not in yaml_output:
                with open('../'+ OUTPUT_YAML_DATA, 'a') as yaml_output:
                    yaml_output.write(yaml.safe_dump(output_data, default_flow_style=False))
            print(f"Yaml for Organization {github_orgs} has been generated")

        except FileNotFoundError:
            open('../'+ OUTPUT_YAML_DATA, "w").close()


if __name__ == "__main__":
    getDataFromYaml = getDictFromYaml(SOURCE_YAML_DATA)
    processUsers(getDataFromYaml)
    processOrgs(getDataFromYaml)
