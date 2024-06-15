from data_processor.calcul_statistics_closeState import calculate_pr_statistics_close

def calculate_more_pages_close(repo, state, access_token, start_date=None, end_date=None):
    totalClosed = total_pr_approved_closed = totalTime = total_pr_without_reviews_closed = 0
    total_pr_with_change_requests_closed = []
    page = 1
    per_page = 100 

    while True:
        total_closed, pr_approved, pr_with_change_requests, total_time, pr_without_reviews = calculate_pr_statistics_close(repo, state, page, access_token, start_date,end_date)
        
        totalClosed += total_closed
        total_pr_approved_closed += pr_approved
        totalTime += total_time
        total_pr_without_reviews_closed += pr_without_reviews

        for pr_detail in pr_with_change_requests:
            total_pr_with_change_requests_closed.append(pr_detail)

        if total_closed < per_page:
            break
        page += 1

    acceptance_rate = (total_pr_approved_closed / totalClosed * 100) if totalClosed > 0 else 0
    total_changes_requested = sum(pr['changesRequestedCount'] for pr in total_pr_with_change_requests_closed)
    rejection_rate = (total_changes_requested / totalClosed * 100) if totalClosed > 0 else 0
    average_time = totalTime / total_pr_approved_closed if total_pr_approved_closed > 0 else 0
    avg_time = "{:.2f} days".format(average_time)
    acceptance_rate = "{:.2f}".format(acceptance_rate)
    rejection_rate = "{:.2f}".format(rejection_rate)
    
    return totalClosed, total_pr_approved_closed, total_pr_with_change_requests_closed, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_closed
