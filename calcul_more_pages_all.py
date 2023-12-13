from calcul_statistics_allState import calculate_pr_statistics_all

def calculate_more_pages_all(repo, state, access_token):
    totalAll = total_pr_approved_all = total_pr_with_change_requests_all = totalTime = total_pr_without_reviews_all = 0
    page = 1
    
    total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews= calculate_pr_statistics_all(repo, state, page, access_token)
    totalAll = total_all
    total_pr_approved_all = pr_approved
    total_pr_with_change_requests_all = pr_with_change_requests
    totalTime = total_time
    total_pr_without_reviews_all = pr_without_reviews
    
    while(total_all == 100):
        page += 1
        total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews = calculate_pr_statistics_all(repo, state, page, access_token)
        totalAll += total_all
        total_pr_approved_all += pr_approved
        total_pr_with_change_requests_all += pr_with_change_requests
        totalTime += total_time
        total_pr_without_reviews_all += pr_without_reviews

    acceptance_rate = (pr_approved / totalAll * 100) if totalAll > 0 else 0
    rejection_rate = (pr_with_change_requests / totalAll * 100) if totalAll > 0 else 0
    avg_time = totalTime / pr_approved if pr_approved > 0 else 0
    
    return totalAll, total_pr_approved_all, total_pr_with_change_requests_all, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_all
