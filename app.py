from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api, abort
from gitstats import process_all_prs, get_all_repos_stats, process_closed_prs, process_open_prs
from datetime import datetime
from data_processor.date import getTime

start_date, end_date = getTime()
        
app = Flask(__name__)
api = Api(app)

repository = {
    "alexiadraghin/RepoTest1", 
    "alexiadraghin/RepoTest2",
    "alexiadraghin/RepoTest3",
    "alexiadraghin/RepoTest4",
    "alexiadraghin/RepoTest5"
}
access_token = "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"


def is_status_valid(status):
    return status in {'open', 'close', 'all'}

def get_repo_stats(status, start_date=None, end_date=None):
    if status == 'all':
        return process_all_prs(repository, access_token, start_date, end_date)
    elif status == 'close':
        return process_closed_prs(repository, access_token, start_date, end_date)
    elif status == 'open':
        return process_open_prs(repository, access_token, start_date, end_date)

class PrList(Resource):
    def get(self, status):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
            except ValueError:
                abort(400, message="Invalid date format. Please use 'DD-MM-YYYY'.")
        else:
            end_date, start_date = getTime()

        app.logger.info(f"Processed dates - Start: {start_date}, End: {end_date}")

        if not is_status_valid(status):
            abort(400, message="Invalid status provided.")
        try:
            data = get_repo_stats(status, start_date, end_date)
            return jsonify({
                "title": "PR Status List",
                "status": status,
                "data": data,
                "startDate": start_date.strftime('%d-%m-%Y') if start_date else "Not specified",
                "endDate": end_date.strftime('%d-%m-%Y') if end_date else "Not specified"
            })
        except Exception as e:
            abort(500, message=str(e))



class ForAllRepos(Resource):
    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        try:
            all_stats = process_all_prs(repository, access_token, start_date, end_date)
            return jsonify({
                "title": "Statistics for all repos",
                "data": all_stats,
                "startDate": start_date or "Not specified",
                "endDate": end_date or "Not specified"
            })
        except Exception as e:
            abort(500, message=str(e))

@app.route("/getData", methods=["GET", "POST"])
def get_data():
    start_date = request.args.get('start_date', default=None)
    end_date = request.args.get('end_date', default=None)
    
    if not start_date or not end_date:
        end_date, start_date = getTime()
    else:
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

    formatted_start_date = start_date.strftime("%d-%m-%Y")
    formatted_end_date = end_date.strftime("%d-%m-%Y")

    all_repos_data = get_all_repos_stats(start_date, end_date)
    closed_prs_data = process_closed_prs(repository, access_token, start_date, end_date)
    open_prs_data = process_open_prs(repository, access_token, start_date, end_date)
    all_prs_data = process_all_prs(repository, access_token, start_date, end_date)

    return render_template("home.html", 
                            all_repos_data=all_repos_data,
                            closed_prs_data=closed_prs_data, 
                            open_prs_data=open_prs_data, 
                            all_prs_data=all_prs_data, 
                            start_date=formatted_start_date,
                            end_date=formatted_end_date)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("first_page.html")


api.add_resource(PrList, '/api/pr/<status>')
api.add_resource(ForAllRepos, '/api/repos')

if __name__ == "__main__":
    app.run(debug=True)
