from datetime import datetime, timedelta
import api.client as client
import requests
from data_processor.review_functions import get_review_count
from models.models import ChangeRequestedPr
from data_processor.date import getTime

def calculate_pr_statistics_all(repository, state, page, access_token, start_date= None,  end_date= None):
    pr_data = client.list_pr(repository=repository, state=state, page=page, access_token=access_token)
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    total_time = 0
    closed_pr_count = 0
    total_pr_all = 0
    pr_with_change_requests = []
    pr_approved = 0
    pr_without_reviews = 0 
    total_approved = 0
    total_rejected = 0
    
    if start_date is None or end_date is None:
        end_date, start_date = getTime()
    
    for pr in pr_data:
        opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        closed_at_str = pr.get("closed_at")
        closed_at = datetime.strptime(closed_at_str, "%Y-%m-%dT%H:%M:%SZ") if closed_at_str else None
        merged_at_str = pr.get("merged_at")
        merged_at= datetime.strptime(merged_at_str, "%Y-%m-%dT%H:%M:%SZ") if merged_at_str else None

        if start_date <= opened_at <= end_date and (closed_at is None or start_date <= closed_at <= end_date):
            pr_number = pr['number']
            reviews_url = pr["url"] + "/reviews"
            response = requests.get(reviews_url, headers=headers)

            if response.status_code == 200:
                reviews = response.json()
                change_requested_count, _ = get_review_count(reviews, 'CHANGES_REQUESTED', start_date, end_date)
                approved_count, approved_reviews = get_review_count(reviews, 'APPROVED', start_date, end_date)     
    
                if change_requested_count > 0:
                    change_requested_pr= ChangeRequestedPr(pr_number, change_requested_count)
                    pr_with_change_requests.append(change_requested_pr.to_dict())

                if closed_at is not None:
                    if approved_count > 0 and change_requested_count == 0 and approved_reviews[-1]["state"] == "APPROVED":
                        pr_approved += 1
                        time_diff = closed_at - opened_at
                        total_time += time_diff.days
                    elif not reviews and merged_at  is None: 
                        pr_without_reviews += 1
                    else :
                        pr_approved += 1
                elif closed_at is None:
                    if approved_count > 0 and change_requested_count == 0 and approved_reviews[-1]["state"] == "APPROVED":
                        pr_approved += 1
    
                    elif not reviews:
                        pr_without_reviews += 1    
            else:
                print(f"Error obtaining reviews for PR {pr_number}: {response.status_code}")
            total_approved += pr_approved
            total_rejected += len(pr_with_change_requests) 
    total_pr_all =len(pr_with_change_requests) + pr_approved 
    average_time = total_time / closed_pr_count if closed_pr_count > 0 else 0
    return total_pr_all, pr_approved, pr_with_change_requests, average_time, pr_without_reviews, total_approved, total_rejected
