from calcul_statistics_openState import calculate_pr_statistics_open


def calculate_more_pages_open(repo, state, access_token):
    total = 0
    page = 1
    total_pr_approved =0
    total_pr_with_change_requests =0
    total_pr_without_reviews =0
    
    total_opened, pr_approved, pr_with_change_requests, pr_without_reviews = calculate_pr_statistics_open(repo, state, page, access_token)
   
    total = total_opened
    total_pr_approved = pr_approved
    total_pr_with_change_requests =pr_with_change_requests
    
    total_pr_without_reviews = pr_without_reviews 
    while(total_opened == 100):
        page += 1
        
        total_opened, pr_approved, pr_with_change_requests, pr_without_reviews = calculate_pr_statistics_open(repo, state, page, access_token)
        total += total_opened
        total_pr_approved += pr_approved
        total_pr_with_change_requests += pr_with_change_requests
        total_pr_without_reviews += pr_without_reviews 
        
    return total,total_pr_approved, total_pr_with_change_requests , total_pr_without_reviews 

