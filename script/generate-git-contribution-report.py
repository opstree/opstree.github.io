import os
import requests as github
import json, yaml

SOURCE_YAML_DATA = '../config/ot-git-details-source.yml'
OUTPUT_YAML_DATA = 'ot-osc-repo-info.yml'


# To Load Input data in yml format
def _yamlLoader(source_yaml_file):
    with open(SOURCE_YAML_DATA) as source_yaml:
        load_input_data = json.dumps(yaml.load(source_yaml, Loader=yaml.FullLoader))  # In String
        input_data_in_dict = json.loads(load_input_data)  # In Dictionary
        return input_data_in_dict

#Hit the Github API to fetch the data
def _hit_github_api(api_url):
    # send get request to github API
    github_response = github.get(api_url)
    data = github_response.json()
    repo_link = data["repos_url"]
    github_repo_link = github.get(repo_link)

    # Convert the API result into json format
    repo_data = github_repo_link.json()
    return repo_data


#Filter the required data fetched through github that is in JSON Format
def _generate_filtered_data(repo_data,category):

    final_data = []
    final_output_data = ()

    for repo in range(len(repo_data)):
        Required_info = dict(Name=repo_data[repo]["name"],
                                description=(repo_data[repo]["description"]),
                                repo=(repo_data[repo]["html_url"]))
        final_data.append(Required_info)
        final_output_data = ({category: final_data})

    return final_output_data

# To fetch the user data from github
def _generate_user_contribution_report(users_info):
    for users in users_info:
        github_username = users
        category = users

        # api url to fetch github data
        api_url = f"https://api.github.com/users/{github_username}"
        repo_data = _hit_github_api(api_url)

        # Append all the required fetched repo info into the array
        final_output_data = _generate_filtered_data(repo_data,category)

        _generate_git_contribution_report("user",github_username,final_output_data)

# To fetch the Organizations data from github
def _generate_orgs_contribution_report(orgs_info):
    for orgs in orgs_info:
        github_orgs = orgs
        category = orgs.split("-")[1]

        # api url to fetch github data
        api_url = f"https://api.github.com/orgs/{github_orgs}"

        repo_data=_hit_github_api(api_url)

        # Append all the required fetched repo info into the array

        final_output_data = _generate_filtered_data(repo_data,category)

        _generate_git_contribution_report("orgs",github_orgs,final_output_data)


# Write the yaml file with the required data
def _generate_git_contribution_report(source_type,github_username,final_output_data):
        
        try:
            yaml_output = open('../'+ OUTPUT_YAML_DATA, mode='r').read()
            if ((os.path.exists('../'+ OUTPUT_YAML_DATA)) == False):
                raise FileNotFoundError("File not found")
            if yaml.safe_dump(final_output_data, default_flow_style=False) not in yaml_output:
                with open('../'+ OUTPUT_YAML_DATA, 'a') as yaml_output:
                    yaml_output.write(yaml.safe_dump(final_output_data, default_flow_style=False))
            print(f"Yaml for {source_type} {github_username} has been generated")

        except FileNotFoundError:
            open('../'+ OUTPUT_YAML_DATA, "w").close()
            yaml_output = open('../'+ OUTPUT_YAML_DATA, mode='r').read()
            if yaml.safe_dump(final_output_data, default_flow_style=False) not in yaml_output:
                with open('../'+ OUTPUT_YAML_DATA, 'a') as yaml_output:
                    yaml_output.write(yaml.safe_dump(final_output_data, default_flow_style=False))
            print(f"Yaml for {source_type} {github_username} has been generated")


if __name__ == "__main__":
    users_and_orgs_info = _yamlLoader(SOURCE_YAML_DATA)
    _generate_user_contribution_report(users_and_orgs_info['users'])
    _generate_orgs_contribution_report(users_and_orgs_info['orgs'])
