import os
import requests as github
import json, yaml

out_file='Open_Source_output.yml'

#Exception handeling to handle error due to the absence of input yaml file
try:
    os.remove('Open_Source_output.yml')
except:
    print("Output file does not exist Creating output file....")
finally:
    source_yaml_data='Open_Source_Input.yml'

    #To Load Input data in yml format
    with open(source_yaml_data) as f:
        load_input_data=json.dumps(yaml.load(f,Loader=yaml.FullLoader))  #In String

        input_data_in_dict=json.loads(load_input_data)  #In Dictionary


    #To fetch the Username from github url
    for i in input_data_in_dict['orgs']:
            github_username = i
            category = i.split("-")[1]

    #api url to fetch github data
            api_url = f"https://api.github.com/users/{github_username}"

            #send get request to github API
            github_response = github.get(api_url)
            data =  github_response.json()

            repo_link = data["repos_url"]
            github_repo_link = github.get(repo_link)

            #Convert the API result into json format
            repo_data = github_repo_link.json()


            final_data=[]   #Data in Array format
           #Append all the required fetched repo info into the array
            for i in range (len(repo_data)):
                Required_info=dict(Name=repo_data[i]["name"],
                description = (repo_data[i]["description"]),
                repo = (repo_data[i]["html_url"]))
                final_data.append(Required_info)



            output_data = ({category: final_data})



         #Write the yaml file with the required data
            with open(out_file,'a') as of:
                yaml.safe_dump(output_data, of, default_flow_style=False)

           
