from graphql import GraphQLError
import datetime

def get_wrapper_details(data_wrapper, qs,page, size):
    
    print('..........................',qs)
    
    keyword_args = {
        'stages': qs
        # 'touch_point':qs,
                
    }
    return data_wrapper(**keyword_args)


def wrapper_without_pagination(data_wrapper, qs):
    keyword_args = {
        'stages': qs  
    }
    return data_wrapper(**keyword_args)


def get_logdate_info(start_logdate, end_logdate):

    if start_logdate:
        start_logdate = datetime.datetime.strptime(start_logdate, '%Y-%m-%d').date()
    if end_logdate:
        end_logdate = datetime.datetime.strptime(end_logdate, '%Y-%m-%d').date()

    key = None
    value = None

    if start_logdate and not end_logdate:
        key = 'logdate__gte'
        value = start_logdate
    elif end_logdate and not start_logdate:
        key = 'logdate__lte'
        value = end_logdate
    else:
        if end_logdate >= start_logdate:
            key = 'logdate__range' 
            value = (start_logdate,end_logdate)
        else:
            raise GraphQLError("StartDate should be <= EndDate")
    return (key, value)