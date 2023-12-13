import requests

def list_pr(repository, state, page, access_token):
    #print("Loading ... ")
    url = f"https://github.geo.conti.de/api/v3/repos/{repository}/pulls?state={state}&per_page=100&page={page}"

    headers = { "Authorization":f"token {access_token}" }
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        pr_data = response.json()
        return pr_data
    else:
        print(f"Eroare : {response.status_code}")
