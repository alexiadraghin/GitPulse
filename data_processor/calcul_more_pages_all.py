from data_processor.calcul_statistics_allState import calculate_pr_statistics_all

def calculate_more_pages_all(repo, state, access_token, start_date=None, end_date=None):
    totalAll = total_pr_approved_all = totalTime = total_pr_without_reviews_all = total_Apprv = total_Rej = 0
    total_pr_with_change_requests_all = []
    page = 1

    # Apelul inițial pentru a obține statisticile PR-urilor
    total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews, total_approved, total_rejected = calculate_pr_statistics_all(repo, state, page, access_token, start_date, end_date)
    
    totalAll += total_all
    total_pr_approved_all += pr_approved
    totalTime += total_time
    total_pr_without_reviews_all += pr_without_reviews
    total_Apprv += total_approved
    total_Rej += total_rejected
    
    # Actualizarea PR-urilor cu cereri de modificare
    for pr_details in pr_with_change_requests:
        total_pr_with_change_requests_all.append(pr_details)

    while total_all == 100:  # Presupunând că 100 este maximul pe pagină, ajustați după necesitate
        page += 1
        total_all, pr_approved, pr_with_change_requests, total_time, pr_without_reviews, total_approved, total_rejected = calculate_pr_statistics_all(repo, state, page, access_token)

        totalAll += total_all
        total_pr_approved_all += pr_approved
        totalTime += total_time
        total_pr_without_reviews_all += pr_without_reviews
        total_Apprv += total_approved
        total_Rej += total_rejected

        for pr_details in pr_with_change_requests:
            total_pr_with_change_requests_all.append(pr_details)
        
    acceptance_rate = (total_pr_approved_all / totalAll * 100) if totalAll > 0 else 0
    total_changes_requested = sum(pr['changesRequestedCount'] for pr in total_pr_with_change_requests_all)

    rejection_rate = (total_changes_requested / totalAll * 100) if totalAll > 0 else 0
    average_time = totalTime / total_pr_approved_all if total_pr_approved_all > 0 else 0
    avg_time = "{:.2f} days".format(average_time)
    acceptance_rate = "{:.2f}".format(acceptance_rate)
    rejection_rate = "{:.2f}".format(rejection_rate)


    return totalAll, total_pr_approved_all, total_pr_with_change_requests_all, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_all
