from datetime import datetime
from data_processor.date import getTime  # Assuming this is the correct import path for your getTime function

# def reviews_filter(review, state, start_date, end_date):
#     print("review: ")
#     review_date = datetime.strptime(review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
#     return review['state'] == state and start_date <= review_date <= end_date

# def get_review_count(reviews, state, start_date_str=None, end_date_str=None):
#     # Convert datetime to string before passing if necessary
#     if isinstance(start_date_str, datetime):
#         start_date_str = start_date_str.strftime('%d-%m-%Y')
#     if isinstance(end_date_str, datetime):
#         end_date_str = end_date_str.strftime('%d-%m-%Y')
    
#     start_date, end_date = getTime(start_date_str, end_date_str)
#     filtered_reviews = [review for review in reviews if reviews_filter(review, state, start_date, end_date)]
#     return len(filtered_reviews), filtered_reviews


def reviews_filter(review, state, start_date, end_date):
    review_date = datetime.strptime(review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")
    # Adaugă loguri pentru a verifica datele
    # print(f"Filtering between {start_date} and {end_date}")
    return review['state'] == state and start_date <= review_date <= end_date

def get_review_count(reviews, state, start_date_str=None, end_date_str=None):
    # Verifică dacă transformarea din str în datetime este necesară
    if isinstance(start_date_str, str):
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
    else:
        start_date = start_date_str

    if isinstance(end_date_str, str):
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    else:
        end_date = end_date_str

    filtered_reviews = [review for review in reviews if reviews_filter(review, state, start_date, end_date)]
    # print(f"Filtered {len(filtered_reviews)} reviews for state {state}")
    return len(filtered_reviews), filtered_reviews
