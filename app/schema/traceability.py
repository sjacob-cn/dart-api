import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType
from app.models import *
from graphql import GraphQLError
from django.db import IntegrityError
from app.schema.validation import Validation
from .utils import *
from .descriptions import *
import json



class Touchpoints(ObjectType):
    step_detail = graphene.String()
    # metric_count = graphene.Int()
    # results =graphene.String()
    variance = graphene.String()
    
class Stages(DjangoObjectType):
    system =graphene.String()
    touch_points =graphene.List(Touchpoints,trace_id = graphene.String(),
            metric =graphene.String(),
            dt = graphene.Date(),  
            brand = graphene.String())
    class Meta:
        model = System_traceability
    def resolve_touch_points(self, info, size=100, page=1, **kwargs):
        print(kwargs)
        trace_id = kwargs['trace_id']
        qs = Trace_ids.objects.all()
        qs=qs.filter(trace_id=trace_id)
        obj = None
        
        for each in qs:
            
            if each.type == 'system':
                obj = System_traceability.objects.all()
                obj = obj.filter(**kwargs).distinct().order_by('-step')
                print(obj,'ghefgeku')
                break
            elif each.type == 'pipeline':
                obj = Pipeline_traceability.objects.all()
                obj = obj.filter(**kwargs).distinct().order_by('-step')
                break
        
        res =Traceability_results.objects.all()
        res = res.filter(trace_id=trace_id).filter(dt=kwargs['dt'])
        data = ''
        for each in res:
            data = each.results
        json_data =json.loads(data)
        # print(json_data)
        v=json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Variance%age']
        # print(json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Totals'][sys_name])
        # return get_wrapper_detail(Touchpoints, obj, page, size) 
        return obj
class Wrapper(ObjectType):
    stages = graphene.List(Stages)
    total_elements = graphene.Int()
    number_of_elements = graphene.Int()
    size = graphene.Int()
    total_pages = graphene.Int()
    current_page = graphene.Int()
    has_next_page = graphene.Boolean()

    class Meta:
        description = desc_wrapper
        
class Trace_idsQuery(ObjectType):
    trace_ids = graphene.Field(
            Wrapper ,
            trace_id = graphene.String(),
            metric =graphene.String(),
            dt = graphene.Date(),  
            brand = graphene.String()
    )
    

    def resolve_trace_ids(self, info, size=100, page=1, **kwargs):
        print(kwargs)
        trace_id = kwargs['trace_id']
        qs = Trace_ids.objects.all()
        qs=qs.filter(trace_id=trace_id)
        obj = None
        
        for each in qs:
            
            if each.type == 'system':
                obj = System_traceability.objects.all()
                obj = obj.filter(**kwargs).distinct().order_by('-step')
                print(obj,'ghefgeku')
                break
            elif each.type == 'pipeline':
                obj = Pipeline_traceability.objects.all()
                obj = obj.filter(**kwargs).distinct().order_by('-step')
                break
        
        # res =Traceability_results.objects.all()
        # res = res.filter(trace_id=trace_id).filter(dt=kwargs['dt'])
        # data = ''
        # for each in res:
        #     data = each.results
        # json_data =json.loads(data)
        # print(json_data)
        # print(json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Variance%age'])
        # print(json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Totals'][sys_name])
        return get_wrapper_details(Wrapper, obj, page, size) 

