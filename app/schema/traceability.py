import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType, String, Boolean, ID, Field, Int,List
from app.models import *
from graphql import GraphQLError
from django.db import IntegrityError
from app.schema.validation import Validation
from .utils import *
from .descriptions import *
import json
import collections
import requests

from types import SimpleNamespace
# class S(ObjectType):
#     stage =String()

class T(ObjectType):
    touchPoint =String()
    metricCount = Int()
    variance = String()

class Data(ObjectType):
    # touchPoints = List(Touchpointss)
    stage = String()
    touchPoints = List(T)

class D(ObjectType):
    stages =List(Data)

def _json_object_hook(d):
        return collections.namedtuple('X', d.keys())(*d.values())

def json2obj(data):
        obj = json.loads(data, object_hook=_json_object_hook)
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        # return json.loads(data, object_hook=_json_object_hook)
        
        return x
class DataQuery(ObjectType):
    results = Field( D, 
                    trace_id=String(required=True),
                    dt=String(required=True),
                    metric=String(required=True),
                    brand=String(required=True)
                    )
    
    
    def resolve_results(self,info,size=100, page=1,**kwargs):
        obj = Trace_ids.objects.all().filter(trace_id=kwargs['trace_id']) 
        sys = None
        for each in obj:
            if each.type == 'system':
                sys = System_traceability.objects.all().filter(**kwargs).order_by('step')
                break
            elif each.type == 'pipeline':
                sys = Pipeline_traceability.objects.all().filter(**kwargs).order_by('step')
                break
        mainlist = []
        maindict = {}
        res =Traceability_results.objects.all()
        res = res.filter(trace_id=kwargs['trace_id']).filter(dt=kwargs['dt'])
        for sy in sys:
            subdict = {}
            data = ''
            for each in res:
                data = each.results
            json_data =json.loads(data)
            subdict['touchPoint']=sy.step_detail
            subdict['metricCount']=int(json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Totals'][sy.system])
            subdict['variance']=json_data['breakdown'][kwargs['metric']][kwargs['brand']]['Variance%age'] 
            maindict['stage'] = sy.system
            maindict['touchPoints']=[subdict]
            if mainlist ==[]:
                mainlist.append({'stage':sy.system,'touchPoints':[subdict]})
            else :
                if sy.system not in [val['stage'] for val in mainlist]:
                    mainlist.append({'stage':sy.system,'touchPoints':[subdict]})
        final_dict ={}
        final_dict["stages"] = mainlist
        # json_data = '{"stages":[{"stage":"ghgjfghdgfmhsdvjhegfkeghehgj","touchPoints":[{"touchPoint":"fhfhfh","metricCount":7364575,"variance":"67"},{"touchPoint":"uiui","metricCount":7,"variance":"90"}]},{"stage":"sellapandi","touchPoints":[{"touchPoint":"memo","metricCount":910,"variance":"90"},{"touchPoint":"xi","metricCount":0,"variance":"99"}]}]}'
        return json2obj(json.dumps(final_dict))