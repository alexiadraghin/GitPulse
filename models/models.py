
class AllPrStats:
    def __init__(self, repo_name, pull_nr, total_accepted, total_rejected, acceptance_rate, rejection_rate, avg_time,  pr_no_action, start_date, end_date):
        self.repo_name = repo_name
        self.pull_nr = pull_nr        
        self.total_accepted = total_accepted
        self.total_rejected = total_rejected
        self.acceptance_rate = acceptance_rate
        self.rejection_rate = rejection_rate
        self.avg_time = avg_time
        self.pr_no_action = pr_no_action   
        self.end_date = end_date
        self.start_date = start_date         
        
    def to_dict(self):
       return {
            "repository": self.repo_name,  
            "total" : self.pull_nr,            
            "approved": self.total_accepted,
            "changeRequestsDetails": [pr.to_dict() if hasattr(pr, 'to_dict') else pr for pr in self.total_rejected],
            "acceptanceRate": self.acceptance_rate,
            "rejectionRate": self.rejection_rate,
            "averageTime": self.avg_time,
            "reviewRequired": self.pr_no_action,
            "startDate":self.start_date, 
            "endDate": self.end_date          
        }
             
class OpenedPrStats:
    def __init__(self, repo_name, pull_nr, total_accepted, total_rejected,  pr_no_action,  start_date, end_date ):
        self.repo_name = repo_name
        self.pull_nr = pull_nr        
        self.total_accepted = total_accepted
        self.total_rejected = total_rejected
        self.pr_no_action = pr_no_action 
        self.end_date = end_date
        self.start_date = start_date             
        
    def to_dict(self):
       return {
            "repository": self.repo_name,  
            "total" : self.pull_nr,            
            "approved": self.total_accepted,
            "changeRequestsDetails": [pr.to_dict() if hasattr(pr, 'to_dict') else pr for pr in self.total_rejected],
            "reviewRequired": self.pr_no_action, 
            "startDate":self.start_date, 
            "endDate": self.end_date      
        }
            
class ClosedPrStats:
    def __init__(self, repo_name, totalClosed, total_pr_approved_closed, total_pr_with_change_requests_closed, acceptance_rate, rejection_rate, avg_time, pr_no_action,  start_date, end_date):
        self.repo_name = repo_name
        self.totalClosed = totalClosed
        self.total_pr_approved_closed = total_pr_approved_closed
        self.total_pr_with_change_requests_closed = total_pr_with_change_requests_closed
        self.acceptance_rate = acceptance_rate
        self.rejection_rate = rejection_rate
        self.avg_time = avg_time
        self.pr_no_action = pr_no_action  
        self.end_date = end_date
        self.start_date = start_date     

    def to_dict(self):
        return {
            "repository": self.repo_name,
            "totalClosed": self.totalClosed,
            "totalApproved": self.total_pr_approved_closed,
            "changeRequestsDetails": [pr.to_dict() if hasattr(pr, 'to_dict') else pr for pr in self.total_pr_with_change_requests_closed],
            "acceptanceRate": self.acceptance_rate,
            "rejectionRate": self.rejection_rate,
            "averageTime": self.avg_time,
            "noActionRequired": self.pr_no_action, 
            "startDate":self.start_date, 
            "endDate": self.end_date  
        }
        
class ChangeRequestedPr:
    def __init__(self, pr_number, changes_requested_count):
        self.pr_number = pr_number
        self.changes_requested_count = changes_requested_count 
    
    def to_dict(self):
        return{
            "prNumber":self.pr_number,
            "changesRequestedCount": self.changes_requested_count
        }        

