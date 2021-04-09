import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType, String, Boolean, ID, Field, Int,List
from app.models import *
from graphql import GraphQLError
from django.db import IntegrityError
from .utils import *
from .descriptions import *
import json
import collections
from django.db.models import Q
import requests
from .validation import validate_data
from types import SimpleNamespace
class T(ObjectType):
    touchPoint =String()
    metricCount = Int()
    variancePercent = String()
class Data(ObjectType):
    stage = String()
    touchPoints = List(T)
class Breakdown(ObjectType):
    unknown = Int()
class D(ObjectType):
    traceId = String()
    metric = String()
    brand =String()
    breakdown = Field(Breakdown)
    metrics = List(String)
    brands = List(String)
    stages =List(Data)

def _json_object_hook(d):
        return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
        obj = json.loads(data, object_hook=_json_object_hook)
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        # return json.loads(data, object_hook=_json_object_hook)
        
        return x
class DataQuery(ObjectType):
    traceability_flow = Field( D, 
                    trace_id=String(required=True),
                    dt=String(required=False),
                    metric=String(required=False),
                    brand=String(required=False)
                    )
    
    
    def resolve_traceability_flow(self,info,size=100, page=1,**kwargs):
        validate_data(**kwargs)
        final_dict = {}
        filter_dict = {}
        for key,value in kwargs.items():
            if value != '':
                filter_dict[key] = value

        obj = Trace_ids.objects.all().filter(trace_id=kwargs['trace_id']) 
        sys = None
        metrics = None
        brands = None
        for each in obj:
            if each.type == 'system':
                
                sys = System_traceability.objects.all().filter(**filter_dict).order_by('step')
                metrics = System_traceability.objects.filter(Q(metric__isnull=False)).values_list('metric').distinct()
                brands = System_traceability.objects.filter(Q(brand__isnull=False)).values_list('brand').distinct()
                break
            elif each.type == 'pipeline':
                
                sys = Pipeline_traceability.objects.all().filter(**filter_dict).order_by('step')
                metrics = System_traceability.objects.filter(Q(metric__isnull=False)).values_list('metric').distinct()
                brands = System_traceability.objects.filter(Q(brand__isnull=False)).values_list('brand').distinct()
                break
        mainlist = []
        maindict = {}
        res=None
        try:
            res =Traceability_results.objects.all()
            res = res.filter(trace_id=kwargs['trace_id']).filter(dt=kwargs['dt'])
        except Exception as e:
            print(e)

        for sy in sys:
            subdict = {}
            data = ''
            for each in res:
                data = each.results
            json_data =json.loads(data)
            
            sublist = []
            if 'brand' not in kwargs.keys():
                for brand in json_data['breakdown'][sy.metric].keys():
                    sublist.append({'touchPoint':sy.step_detail,'metricCount':int(json_data['breakdown'][sy.metric][brand]['Totals'][sy.system]),'variance':json_data['breakdown'][sy.metric][brand]['Variance%age']}) 
                final_dict['breakdown'] = {}
            else:
                sublist.append({'touchPoint':sy.step_detail,'metricCount':int(json_data['breakdown'][sy.metric][sy.brand]['Totals'][sy.system]),'variancePercent':json_data['breakdown'][sy.metric][sy.brand]['Variance%age']})
                final_dict['breakdown'] = {'unknown':int(json.loads(data)['breakdown'][kwargs['metric']][kwargs['brand']]['VarianceBreakdown']['Unknown'])}
            maindict['stage'] = sy.system
            maindict['touchPoints']=sublist
            if mainlist ==[]:
                mainlist.append({'stage':sy.system,'touchPoints':sublist})
            else :
                if sy.system not in [val['stage'] for val in mainlist]:
                    mainlist.append({'stage':sy.system,'touchPoints':sublist})
        final_dict["traceId"] = kwargs['trace_id']
        final_dict['metric'] = kwargs['metric']
        final_dict['brand'] = kwargs['brand']
        metric_list = []
        brand_list = []
        for metric in metrics:
            metric_list.append(metric[0])
        for brand in brands:
            brand_list.append(brand[0])
        final_dict['metrics'] = metric_list
        final_dict['brands'] = brand_list
        final_dict["stages"] = mainlist
        return json2obj(json.dumps(final_dict))