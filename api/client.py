import requests

def list_pr(repository, state, page, access_token):
    
    url = f"https://api.github.com/repos/{repository}/pulls?state={state}&per_page=100&page={page}"

    headers = { "Authorization":f"token {access_token}" }
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        pr_data = response.json()
        return pr_data
    elif response.status_code == 404:
        print(f"Repository not found: {response.status_code}")
    elif response.status_code == 401:
        print(f"Authentication error: Check your access token.")
    else:
        print(f"Failed to fetch PR data: {response.status_code}")

