import datetime
from models import RepoStats
from calcul_more_pages_all import calculate_more_pages_all

end_date = datetime.now() 
start_date = end_date - datetime.timedelta(days=14)
    
def get_repo_stats (repo, state, access_token):
    totalAll, total_approved, total_changes_requested, acceptance_rate, rejection_rate, avg_time, pr_no_action = calculate_more_pages_all(repo, state, access_token)

    my_repo_stats = RepoStats(repo, totalAll, total_approved, total_changes_requested, f"{acceptance_rate:.2f}%", f"{rejection_rate:.2f}%", avg_time, pr_no_action)
    json_data = my_repo_stats.convert_to_json()
    with open('repo_stats.json', 'w') as file:
        file.write(json_data)
