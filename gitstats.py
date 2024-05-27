from data_processor.calcul_more_pages_close import calculate_more_pages_close
from data_processor.calcul_more_pages_open import calculate_more_pages_open
from data_processor.calcul_more_pages_all import calculate_more_pages_all
from models.models import ClosedPrStats, OpenedPrStats, AllPrStats, ChangeRequestedPr


repository = {
    # "QL-Software-Development/clive-test-tracking-ux",
    # "QL-Software-Development/CliveQlp",
    # "QL-Software-Development/CLIVE.QLP.Provider",
    # "QL-Software-Development/clive-documents",
    # "QL-Software-Development/Clive.TestTracking"
    "alexiadraghin/RepoTest1", 
    "alexiadraghin/RepoTest2",
    "alexiadraghin/RepoTest3",
    "alexiadraghin/RepoTest4",
    "alexiadraghin/RepoTest5"
}

state_filter = {"close", "open", "all"}
total_prs_all=0
total_review_req_all =0
total_prs_all_approved=0
total_prs_all_changes_requested=0
total_time_prs_avg_all=0

def process_closed_prs(repository, access_token, start_date=None, end_date=None):
    close_repo_stats = []
    for repo in repository:
        totalClosed, total_pr_approved_closed, total_pr_with_change_requests_closed, acceptance_rate, rejection_rate, avg_time, total_pr_without_reviews_closed = calculate_more_pages_close(repo, "close", access_token, start_date, end_date)

        repo_stats = ClosedPrStats(
            repo,
            totalClosed,
            total_pr_approved_closed,
            total_pr_with_change_requests_closed,  
            acceptance_rate,
            rejection_rate,
            avg_time,
            total_pr_without_reviews_closed,
            start_date, 
            end_date
        )
        
        close_repo_stats.append(repo_stats.to_dict())
    return close_repo_stats

        
def process_open_prs(repository, access_token,  start_date=None, end_date=None):
    open_repo_stats = []

    for repo in repository:
        total, total_pr_approved, total_pr_with_change_requests, total_pr_without_reviews = calculate_more_pages_open(repo, "open", access_token,  start_date, end_date)

        repo_stats = OpenedPrStats(
            repo,
            total, 
            total_pr_approved, 
            total_pr_with_change_requests, 
            total_pr_without_reviews,
            start_date, 
            end_date
        )
        open_repo_stats.append(repo_stats.to_dict())
    return open_repo_stats


def process_all_prs(repository, access_token,  start_date=None, end_date=None):
    all_repo_stats = []  
    for repo in repository:
        totalAll, total_approved, total_changes_requested, acceptance_rate, rejection_rate, avg_time, total_no_action = calculate_more_pages_all(repo, "all", access_token, start_date, end_date)

        repo_stats = AllPrStats(repo, 
                                totalAll, 
                                total_approved, 
                                total_changes_requested, 
                                acceptance_rate, 
                                rejection_rate, 
                                avg_time, 
                                total_no_action,
                                start_date, 
                                end_date)
        all_repo_stats.append(repo_stats.to_dict())

    return all_repo_stats

def process_all_prs2(repository, access_token,  start_date=None, end_date=None):
    all_repo_stats = []  
    total_prs_all = total_review_req_all = total_prs_all_approved = 0
    total_prs_all_changes_requested = [] 
    for repo in repository:
        totalAll, total_approved, pr_changes_requested_details, acceptance_rate, rejection_rate, avg_time, total_no_action = calculate_more_pages_all(repo, "all", access_token,  start_date, end_date)

        total_prs_all += totalAll
        total_prs_all_approved += total_approved
        total_review_req_all += total_no_action

        total_prs_all_changes_requested.extend(pr_changes_requested_details) 

        repo_stats = AllPrStats(repo, 
                                totalAll, 
                                total_approved, 
                                pr_changes_requested_details, 
                                acceptance_rate, 
                                rejection_rate, 
                                avg_time, 
                                total_no_action,
                                start_date, 
                                end_date)
        all_repo_stats.append(repo_stats.to_dict())

    summary_stats = {
        "total": total_prs_all,
        "reviewRequired": total_review_req_all,
        "totalApproved": total_prs_all_approved,
        "totalRejected": total_prs_all_changes_requested, 
        "all_repo_stats": all_repo_stats,
        "startDate": start_date,
        "endDate" : end_date
    }

    return summary_stats

def process_for_all_stats(summary_stats):
    total_prs_all = summary_stats["total"]
    total_prs_all_approved = summary_stats["totalApproved"]
    total_prs_all_changes_requested = summary_stats["totalRejected"]  
    start_date=summary_stats['startDate']
    end_date=summary_stats['endDate']

    acceptance_rate_AllState = (total_prs_all_approved / total_prs_all * 100) if total_prs_all > 0 else 0
    rejection_rate_AllState = (len(total_prs_all_changes_requested) / total_prs_all * 100) if total_prs_all > 0 else 0
    acceptance_rate_AllState = "{:.2f}".format(acceptance_rate_AllState)
    rejection_rate_AllState = "{:.2f}".format(rejection_rate_AllState)
    all_repos_stats = {
        "total": total_prs_all,
        "totalApproved": total_prs_all_approved,
        "totalRejected": total_prs_all_changes_requested,  
        "acceptanceRate": acceptance_rate_AllState,
        "rejectionRate": rejection_rate_AllState,
        "reviewRequired": summary_stats["reviewRequired"],
        "startDate": start_date,
        "endDate" : end_date
    }
    return all_repos_stats

def get_all_repos_stats(start_date=None, end_date=None):
    summary_stats= process_all_prs2(repository, access_token,  start_date, end_date)
    all_stats= process_for_all_stats(summary_stats)
    return all_stats