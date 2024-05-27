from datetime import datetime, timedelta

def getTime(start_date_str=None, end_date_str=None):
    if start_date_str is None or end_date_str is None:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=14)
    else:
        # Verifică dacă start_date_str și end_date_str sunt string-uri
        if isinstance(start_date_str, datetime) or isinstance(end_date_str, datetime):
            raise TypeError("Expected string type for start_date_str and end_date_str")
        
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
        
    return end_date, start_date
