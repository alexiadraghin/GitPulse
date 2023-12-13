import client
from datetime import datetime
from datetime import timedelta
from review_functions import get_review_count
import requests

    
end_date = datetime.now() 
start_date = end_date - timedelta(days=14)
access_token = "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" 


def calculate_pr_statistics_open(repository, state, page,  access_token):
    pr_data = client.list_pr(repository=repository, state=state,page=page, access_token=access_token)
    
    
    total_opened = 0
    pr_with_change_requests = 0
    pr_approved=0
    pr_without_reviews = 0
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    if pr_data:
        for pr in pr_data:
            opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if start_date <= opened_at <= end_date:
                total_opened += 1
                pr_number = pr['number']
                reviews_url = pr["url"] + "/reviews"
                
                response = requests.get(reviews_url, headers=headers)
                
                if response.status_code == 200:
                    reviews = response.json()
                    if reviews:
                        change_requested_reviews = get_review_count(reviews, 'CHANGES_REQUESTED')
                        approved_reviews = get_review_count(reviews, 'APPROVED')

                        if change_requested_reviews:
                            pr_with_change_requests += 1
                        if approved_reviews:
                            pr_approved += 1
                    else:
                        pr_without_reviews += 1
                else:
                    print(f"Eroare la obținerea review-urilor pentru PR {pr_number}: {response.status_code}")
        total_opened = pr_with_change_requests + pr_approved
    
    return total_opened, pr_approved, pr_with_change_requests, pr_without_reviews