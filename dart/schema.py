import graphene
# from app.schema.data_gaps import Data_gapsQuery,DataMutation
# from app.schema.Pipeline_traceability import Pipeline_traceabilityQuery,Pipeline_traceabilityMutation
# from app.schema.system_traceability import system_traceabilityQuery,systemtraceabilityMutation
from app.schema.traceability import Trace_idsQuery
# from app.schema.Traceability_results import Traceability_resultsQuery,Traceability_resultsMutation
# from app.schema.sample import SQuery
# from graphql_auth.schema import UserQuery, MeQuery

class Query(Trace_idsQuery, graphene.ObjectType):
    pass
class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=None)
