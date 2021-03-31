import graphene

from app.schema.traceability import DataQuery
class Query(DataQuery , graphene.ObjectType):
    pass
class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
