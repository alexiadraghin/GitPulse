from datetime import datetime
from datetime import timedelta

end_date = datetime.now() 
start_date = end_date - timedelta(days=14)
access_token = "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" 

def reviews_filter(review, state, start_date, end_date):
    review_date = datetime.strptime(review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
    return review['state'] == state and start_date <= review_date <= end_date

    
def get_review_count(reviews, state ):
    # review_date = datetime.strptime(reviews['submitted_at'], '%Y-%m-%d').date()
    filtered_reviews = [r for r in reviews if reviews_filter(r, state, start_date, end_date)]
    return filtered_reviews
