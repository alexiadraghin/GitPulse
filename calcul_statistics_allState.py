from datetime import datetime
from datetime import timedelta
import client
import requests
from review_functions import get_review_count


end_date = datetime.now() 
start_date = end_date - timedelta(days=14)

def calculate_pr_statistics_all(repository, state, page, access_token):
    pr_data = client.list_pr(repository=repository, state=state, page=page, access_token=access_token)
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    total_time = 0
    closed_pr_count = 0
    total_pr_all = 0
    pr_with_change_requests = 0
    pr_approved = 0
    pr_without_reviews = 0
    
    for pr in pr_data:
        opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        closed_at_str = pr.get("closed_at")
        closed_at = datetime.strptime(closed_at_str, "%Y-%m-%dT%H:%M:%SZ") if closed_at_str else None

        if start_date <= opened_at <= end_date and (closed_at is None or start_date <= closed_at <= end_date):
            pr_number = pr['number']
            reviews_url = pr["url"] + "/reviews"

            response = requests.get(reviews_url, headers=headers)
            change_requested_count = 0
            approved_count = 0

            if response.status_code == 200:
                reviews = response.json()

                if reviews:
                    change_requested_reviews = get_review_count(reviews, 'CHANGES_REQUESTED')
                    approved_reviews = get_review_count(reviews, 'APPROVED')
                    
                    change_requested_count = len(change_requested_reviews)
                    approved_count = len(approved_reviews)
                    

                    if change_requested_reviews:
                        pr_with_change_requests += 1
                    elif approved_reviews:
                        pr_approved += 1

                        if closed_at:
                            time_diff = closed_at - opened_at
                            total_time += time_diff.days
                            closed_pr_count += 1
                    print(f"PR #{pr_number}: Changes Requested - {change_requested_count}, Approved - {approved_count}")        
                else:
                    pr_without_reviews += 1
            else:
                print(f"Error obtaining reviews for PR {pr_number}: {response.status_code}")
                
            

    total_pr_all = pr_with_change_requests + pr_approved 

    average_time = total_time / closed_pr_count if closed_pr_count > 0 else 0
    return total_pr_all, pr_approved, pr_with_change_requests, average_time, pr_without_reviews
 
            