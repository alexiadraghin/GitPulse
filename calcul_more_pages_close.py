from calcul_statistics_closeState import calculate_pr_statistics_close

def calculate_more_pages_close(repo, state, access_token):
    totalClosed = total_pr_approved_closed = total_pr_with_change_requests_closed = totalTime = total_pr_without_reviews_closed = 0
    page = 1
    
    total_closed, pr_approved, pr_with_change_requests, total_time, pr_without_reviews= calculate_pr_statistics_close(repo, state, page, access_token)
    totalClosed = total_closed
    total_pr_approved_closed = pr_approved
    total_pr_with_change_requests_closed = pr_with_change_requests
    totalTime = total_time
    total_pr_without_reviews_closed = pr_without_reviews
    
    while(total_closed == 100):
        page += 1
        total_closed, pr_approved, pr_with_change_requests, total_time, pr_without_reviews = calculate_pr_statistics_close(repo, state, page, access_token)
        totalClosed += total_closed
        total_pr_approved_closed += pr_approved
        total_pr_with_change_requests_closed += pr_with_change_requests
        totalTime += total_time
        total_pr_without_reviews_closed += pr_without_reviews

    acceptance_rate = (pr_approved / totalClosed * 100) if totalClosed > 0 else 0
    rejection_rate = (pr_with_change_requests / totalClosed * 100) if totalClosed > 0 else 0
    avg_time = totalTime / pr_approved if pr_approved > 0 else 0
    
    return totalClosed, total_pr_approved_closed, total_pr_with_change_requests_closed, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_closed
