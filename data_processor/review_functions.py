from datetime import datetime  

def reviews_filter(review, state, start_date, end_date):
    review_date = datetime.strptime(review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
    return review['state'] == state and start_date <= review_date <= end_date

def get_review_count(reviews, state, start_date_str=None, end_date_str=None):
    if isinstance(start_date_str, str):
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
    else:
        start_date = start_date_str

    if isinstance(end_date_str, str):
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    else:
        end_date = end_date_str
    filtered_reviews = [review for review in reviews if reviews_filter(review, state, start_date, end_date)]
    return len(filtered_reviews), filtered_reviews


