from datetime import datetime, timedelta
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
    
    total_approved = 0
    total_rejected = 0
    
    for pr in pr_data:
        opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        closed_at_str = pr.get("closed_at")
        closed_at = datetime.strptime(closed_at_str, "%Y-%m-%dT%H:%M:%SZ") if closed_at_str else None

        if start_date <= opened_at <= end_date and (closed_at is None or start_date <= closed_at <= end_date):
            pr_number = pr['number']
            reviews_url = pr["url"] + "/reviews"

            response = requests.get(reviews_url, headers=headers)

            if response.status_code == 200:
                reviews = response.json()
                last_modification_date = datetime.strptime(pr["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                last_review_date = None

                change_requested_reviews = len(get_review_count(reviews, 'CHANGES_REQUESTED'))
                approved_reviews = len(get_review_count(reviews, 'APPROVED'))

                if reviews:
                    last_review = max(reviews, key=lambda x: datetime.strptime(x["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")) if reviews else None
                    last_review_date = datetime.strptime(last_review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ") if last_review else None

                    if last_modification_date > last_review_date:
                        print(f"PR #{pr_number} requires a new review")
                        pr_without_reviews += 1
                    else:
                        if change_requested_reviews > 0:
                            pr_with_change_requests += 1
                        if approved_reviews > 0:
                            pr_approved += 1
                            if closed_at:
                                time_diff = closed_at - opened_at
                                total_time += time_diff.days
                                closed_pr_count += 1
                        print(f"PR #{pr_number}: Changes Requested - {change_requested_reviews}, Approved - {approved_reviews}")        
                else:
                    pr_without_reviews += 1
            else:
                print(f"Error obtaining reviews for PR {pr_number}: {response.status_code}")
                
            total_approved += approved_reviews
            total_rejected += change_requested_reviews

    total_pr_all = pr_with_change_requests + pr_approved 

    average_time = total_time / closed_pr_count if closed_pr_count > 0 else 0
    return total_pr_all, pr_approved, pr_with_change_requests, average_time, pr_without_reviews, total_approved, total_rejected
