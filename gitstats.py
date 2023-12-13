from calcul_more_pages_close import calculate_more_pages_close
from calcul_more_pages_open import calculate_more_pages_open
from calcul_more_pages_all import calculate_more_pages_all


repository = {"QL-Software-Development/clive-test-tracking-ux", 
              "QL-Software-Development/CliveQlp", 
              "QL-Software-Development/CLIVE.QLP.Provider", 
              "QL-Software-Development/clive-documents", 
              "QL-Software-Development/Clive.TestTracking"
              }

access_token = "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" 

state_filter = {"close", "open", "all"}


total_prs_close=0
total_review_req_close =0
total_prs_close_approved=0
total_prs_close_changes_requested=0
total_time_prs_avg_close=0

total_prs_open=0
total_review_req_open =0

total_prs_all=0
total_review_req_all =0
total_prs_all_approved=0
total_prs_all_changes_requested=0
total_time_prs_avg_all=0

for state in state_filter:
    if state == "close":
        for repo in repository:
            totalClosed, total_pr_approved_closed, total_pr_with_change_requests_closed, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_closed= calculate_more_pages_close(repo, state, access_token)


            total_prs_close += totalClosed
            total_prs_close_approved += total_pr_approved_closed
            total_prs_close_changes_requested += total_pr_with_change_requests_closed
            total_review_req_close += total_pr_without_reviews_closed


            print(f"State: {state}")
            print(f"Repository: {repo}")
            print(f"Number of PR excluding review req: {totalClosed}")
            print(f"Number of PRs with status APPROVED: {total_pr_approved_closed}")
            print(f"Number of PRs with status CHANGES_REQUESTED: {total_pr_with_change_requests_closed}")
            print(f"Acceptance Rate: {acceptance_rate:.2f}%")
            print(f"Rejection Rate: {rejection_rate:.2f}%")
            print(f"Average Time: {avg_time:.2f} days")
            print(f"Number of PRs with status REVIEW_REQUIRED: {total_pr_without_reviews_closed}")
            print("-" * 30)
            
            
    elif state == "open":
        for repo in repository:
            total, total_pr_approved, total_pr_with_change_requests , total_pr_without_reviews  = calculate_more_pages_open(repo, state, access_token)
            
            total_prs_open += total
            total_review_req_open += total_pr_without_reviews
        
            
            print(f"State: {state}")
            print(f"Repository: {repo}")
            print(f"Number of PR excluding review req: {total}")
            print(f"Number of PRs with status APPROVED: {total_pr_approved}")
            print(f"Number of PRs with status CHANGES_REQUESTED: {total_pr_with_change_requests}")
            print(f"Number of PRs with status REVIEW_REQUIRED: {total_pr_without_reviews}")
            print("-" * 30)

    
    elif state == "all":
        for repo in repository:
            totalAll, total_pr_approved_all, total_pr_with_change_requests_all, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_all= calculate_more_pages_all(repo, state, access_token)


            total_prs_all += totalAll
            total_prs_all_approved += total_pr_approved_all
            total_prs_all_changes_requested += total_pr_with_change_requests_all
            total_review_req_all += total_pr_without_reviews_all


            print(f"State: {state}")
            print(f"Repository: {repo}")
            print(f"Number of PR excluding review req: {totalAll}")
            print(f"Number of PRs with status APPROVED: {total_pr_approved_all}")
            print(f"Number of PRs with status CHANGES_REQUESTED: {total_pr_with_change_requests_all}")
            print(f"Acceptance Rate: {acceptance_rate:.2f}%")
            print(f"Rejection Rate: {rejection_rate:.2f}%")
            print(f"Average Time: {avg_time:.2f} days")
            print(f"Number of PRs with status REVIEW_REQUIRED: {total_pr_without_reviews_all}")
            print("-" * 30)
            
            
    acceptance_rate_AllState = (total_prs_all_approved / total_prs_all * 100) if total_prs_all > 0 else 0
    rejection_rate_AllState = (total_prs_all_changes_requested / total_prs_all * 100) if total_prs_all > 0 else 0
    
print("-" * 30)
print(f"Total PRs excluding review req: {total_prs_all}")
print(f"Accepted PRs : {total_prs_all_approved}")
print(f"Rejected PRs : {total_prs_all_changes_requested}")
print(f"Acceptance Rate: {acceptance_rate_AllState:.2f}%")
print(f"Rejection Rate : {rejection_rate_AllState:.2f}%")
print(f"Number of PRs with review required: {total_review_req_all}")
print("-" * 30)
print("-" * 30)

# print(f"Total PRs opened excluding review req: {total_prs_open}")
# print(f"Number of PRs with review required open state: {total_review_req_open}")
# print("-" * 30)