from graphql import GraphQLError
import datetime
def validate_data(**kwargs):
    try:
        dt = datetime.datetime.strptime(kwargs['dt'],'%Y-%m-%d')
    except Exception as e:
        raise GraphQLError("Invalid Date Format") 
    if kwargs['trace_id'] == '':
        raise GraphQLError("Trace ID should not be empty")