from datetime import datetime, timedelta
from api.client import list_pr
import requests
from data_processor.review_functions import get_review_count
from models.models import ChangeRequestedPr
from data_processor.date import getTime


def calculate_pr_statistics_close(repository, state, page, access_token, start_date=None,end_date=None):
    pr_data = list_pr(repository=repository, state=state, page=page, access_token=access_token)
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    total_time = 0
    total_closed = 0
    pr_with_change_requests = []
    pr_approved=0
    pr_without_reviews = 0
    if start_date is None or end_date is None:
        end_date, start_date = getTime()
        
    for pr in pr_data:

        opened_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        merged_at_str = pr.get("merged_at")
        merged_at= datetime.strptime(merged_at_str, "%Y-%m-%dT%H:%M:%SZ") if merged_at_str else None

        closed_at_str = pr.get("closed_at")
        closed_at = datetime.strptime(closed_at_str, "%Y-%m-%dT%H:%M:%SZ") if closed_at_str else None

        if start_date <= opened_at <= end_date and (closed_at is not None and start_date <= closed_at <= end_date):
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
                    print(f"PR #{pr_number} has {change_requested_count} changes requested.")

                if approved_count > 0 and change_requested_count == 0 and approved_reviews[-1]["state"] == "APPROVED":

                    pr_approved += 1
                    time_diff = closed_at - opened_at
                    total_time += time_diff.days
                elif not reviews and merged_at  is None: 
                    pr_without_reviews += 1
                else :
                    pr_approved += 1
            else:
                print(f"Error fetching reviews for PR #{pr_number}: {response.status_code}")
                
    total_closed = len(pr_with_change_requests) + pr_approved 
    return total_closed, pr_approved, pr_with_change_requests ,  total_time, pr_without_reviews