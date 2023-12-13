from datetime import datetime
from datetime import timedelta
import client
import requests
from review_functions import get_review_count


end_date = datetime.now() 
start_date = end_date - timedelta(days=14)

def calculate_pr_statistics_close(repository, state, page, access_token):
    pr_data = client.list_pr(repository=repository, state=state, page=page, access_token=access_token)
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    total_time = 0
    total_closed = 0
    pr_with_change_requests = 0
    pr_approved=0
    pr_without_reviews = 0
        
        
    for pr in pr_data:
        opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        closed_at = datetime.strptime(pr["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
        
        if start_date <= opened_at <= end_date and start_date <= closed_at <= end_date :
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
                        time_diff = closed_at - opened_at
                        total_time += time_diff.days
                            
                else:
                    pr_without_reviews += 1
            else:
                print(f"Eroare la obținerea review-urilor pentru PR {pr_number}: {response.status_code}")
    total_closed = pr_with_change_requests + pr_approved
    return total_closed, pr_approved, pr_with_change_requests, total_time, pr_without_reviews
