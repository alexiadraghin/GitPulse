from calcul_statistics_allState import calculate_pr_statistics_all

def calculate_more_pages_all(repo, state, access_token):
    totalAll = total_pr_approved_all = total_pr_with_change_requests_all = totalTime = total_pr_without_reviews_all = total_Apprv = total_Rej = total_review = 0
    page = 1
    
    total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews, total_approved, total_rejected = calculate_pr_statistics_all(repo, state, page, access_token)
    totalAll = total_all
    total_pr_approved_all = pr_approved
    total_pr_with_change_requests_all = pr_with_change_requests
    totalTime = total_time
    total_pr_without_reviews_all = pr_without_reviews
    total_Apprv = total_approved
    total_Rej = total_rejected
    
    while(total_all == 100):
        page += 1
        total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews, total_approved, total_rejected = calculate_pr_statistics_all(repo, state, page, access_token)
        totalAll += total_all
        total_pr_approved_all += pr_approved
        total_pr_with_change_requests_all += pr_with_change_requests
        totalTime += total_time
        total_pr_without_reviews_all += pr_without_reviews
        total_Apprv += total_approved
        total_Rej += total_rejected
        
    total_review = total_Apprv + total_Rej
    acceptance_rate = (total_Apprv / total_review * 100) if total_review > 0 else 0
    rejection_rate = (total_Rej / total_review * 100) if total_review > 0 else 0
    avg_time = totalTime / pr_approved if pr_approved > 0 else 0
    
    return totalAll, total_pr_approved_all, total_pr_with_change_requests_all, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_all
