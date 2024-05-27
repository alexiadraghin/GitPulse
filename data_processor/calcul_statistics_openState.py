import api.client as client
from datetime import datetime
from datetime import timedelta
from data_processor.review_functions import get_review_count
import requests
from data_processor.date import getTime
from models.models import ChangeRequestedPr





def calculate_pr_statistics_open(repository, state, page, access_token, start_date=None, end_date=None):
    pr_data = client.list_pr(repository=repository, state=state, page=page, access_token=access_token)
    
    if start_date is None or end_date is None:
        end_date, start_date = getTime()
        
    total_opened = 0
    pr_with_change_requests = []
    pr_approved = 0
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
                    change_requested_count, _ = get_review_count(reviews, 'CHANGES_REQUESTED', start_date, end_date)
                    approved_count, approved_reviews = get_review_count(reviews, 'APPROVED', start_date, end_date)

                    if change_requested_count > 0:
                        change_requested_pr = ChangeRequestedPr(pr_number, change_requested_count)
                        pr_with_change_requests.append(change_requested_pr.to_dict())
                    if approved_count > 0 and change_requested_count == 0 and approved_reviews[-1]["state"] == "APPROVED":
                        pr_approved += 1
                    elif not reviews:
                        pr_without_reviews += 1
                else:
                    print(f"Error fetching reviews for PR #{pr_number}: {response.status_code}")
                
    return total_opened, pr_approved, pr_with_change_requests, pr_without_reviews
