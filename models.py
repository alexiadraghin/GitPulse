import json

class RepoStats:
    def __init__(self, repo_name, pull_nr, total_accepted, total_rejected, acceptance_rate, rejection_rate, avg_time,  pr_no_action ):
        self.repo_name = repo_name
        self.pull_nr = pull_nr        
        self.total_accepted = total_accepted
        self.total_rejected = total_rejected
        self.acceptance_rate = acceptance_rate
        self.rejection_rate = rejection_rate
        self.avg_time = avg_time
        self.pr_no_action = pr_no_action             
        
    def to_dict(self):
       return {
            "repository": self.repo_name,  
            "total" : self.pull_nr,            
            "approved": self.total_accepted,
            "changesRequested": self.total_rejected,
            "acceptanceRate": self.acceptance_rate,
            "rejectionRate": self.rejection_rate,
            "averageTime": self.avg_time,
            "reviewRequired": self.pr_no_action     
        }
             
class AllReposStats:
    def __init__(self, total_prs, accepted, rejected, acceptance_rate, rejection_rate, review_required):
        self.total_prs = total_prs
        self.accepted = accepted
        self.rejected = rejected
        self.acceptance_rate = acceptance_rate
        self.rejection_rate = rejection_rate
        self.review_required = review_required

    def to_dict(self):
        return {
            "total": self.total_prs,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "acceptanceRate": f"{self.acceptance_rate:.2f}%",
            "rejectionRate": f"{self.rejection_rate:.2f}%",
            "reviewRequired": self.review_required
        }
# # Crearea unei instanțe a clasei RepoStats
# my_repo_stats = RepoStats("RepoName", 100,  75, 25,"75%", "25%",12, 0)

# # Serializarea în JSON
# json_data = my_repo_stats.convert_to_json()

# # Afișarea datelor serializate
# print(json_data)

# # Sau, pentru a salva într-un fișier
# with open('repo_stats.json', 'w') as file:
#     file.write(json_data)