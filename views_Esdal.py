
import django
django.setup()
import os
from os import remove

from django.shortcuts import render, redirect
from django.http import HttpResponse
import numpy as np
import simplejson as json
import json
from datetime import datetime
from pymongo import MongoClient
import threading
import time
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import http.client
import ssl
from multiprocessing import Process
import copy




uri = "mongodb://alsatdb:uCMYWsmL1BbfPuAWbOaAIdsvULu7JU1FMg2Gqu6bER6NViVpYW1niEHz7MRrtwbcy0K2Q8K0VznTB1ll7NNNfw==@alsatdb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@alsatdb@&retrywrites=false"

try:
        connect = MongoClient(uri)
        print("DB connection works!!")
except:
        print("DB connection failed")

db = connect.demoDB
collection_summary = db.DBsummary
collection_results = db.DBResults
collection_errors = db.DBErrors

#Esdal conectivity
#certificate_file = 'alsat.francecentral.cloudapp.azure.com.cert.pem'
certificate_file = 'alsatpoc.uksouth.cloudapp.azure.com.cer.pem'
#certificate_file = 'test.cer.pem'
#certificate_secret = 'alsat.francecentral.cloudapp.azure.com.key.pem'
certificate_secret = 'alsatpoc.uksouth.cloudapp.azure.com.key.new.pem'
#certificate_secret = 'test.key.pem'
#host = 'alsat-api.uksouth.cloudapp.azure.com'
host = 'alsatstagnew.esdal2.com'


import pyodbc

## SQL connectivity##

# Structures Database
server = 'svrhalfjointdb.database.windows.net'
database_structure = 'structures_db'
username = 'dbadmin'
password = 'Akka_Di_2020'

driver= '{ODBC Driver 17 for SQL Server}'
cnxn_Structures = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database_structure+';UID='+username+';PWD='+ password)
cursor_structure = cnxn_Structures.cursor()


threads = list()
threads2 = list()


def summary_recalculate(request):
    global d_current_status
    global d_HB_or_SV
    global d_HB_or_SV_value
    global d_r_St_type
    global d_r_HB1
    global d_r_text_HB
    global d_r_HB2
    global d_r_d_result_HB
    global d_r_SHR1
    global d_r_text_SHR
    global d_r_SHR2
    global d_r_d_result_SHR
    global d_r_text_HB_pin
    global d_r_text_SHR_pin
    global d_r_HB1_pin
    global d_r_SHR1_pin
    global d_r_HB2_pin
    global d_r_SHR2_pin
    global d_r_d_result_HB_pin
    global d_r_d_result_SHR_pin
    global d_r_text_HB_fix
    global d_r_text_SHR_fix 
    global d_r_HB1_fix 
    global d_r_SHR1_fix 
    global d_r_HB2_fix
    global d_r_SHR2_fix 
    global d_r_d_result_HB_fix 
    global d_r_d_result_SHR_fix 
    global d_fallaContinouos
    global d_r_HB1_hjs 
    global d_r_SHR1_hjs 
    global d_r_HB2_hjs 
    global d_r_SHR2_hjs 
    global d_r_d_result_HB_hjs
    global d_r_d_result_SHR_hjs 
    global d_r_text_HB_hjs 
    global d_r_text_SHR_hjs
    global d_current_status_hb 
    global d_current_status_shr 
    global d_sf 
    global d_Span_SVRating
    global d_estructure_Type_convert 
    global d_current_status_hb_hjs 
    global d_current_status_shr_hjs
    global d_ldds_f 
    global d_ldds_position_f 
    global valid_data 
    global d_extra_check_hj
    global d_current_status_localRecalculate
    global d_HB_or_SV_localRecalculate
    global d_HB_or_SV_value_localRecalculate
    global d_r_St_type_localRecalculate
    global d_r_HB1_localRecalculate
    global d_r_text_HB_localRecalculate
    global d_r_HB2_localRecalculate
    global d_r_d_result_HB_localRecalculate
    global d_r_SHR1_localRecalculate
    global d_r_text_SHR_localRecalculate
    global d_r_SHR2_localRecalculate
    global d_r_d_result_SHR_localRecalculate
    global d_r_text_HB_pin_localRecalculate
    global d_r_text_SHR_pin_localRecalculate
    global d_r_HB1_pin_localRecalculate
    global d_r_SHR1_pin_localRecalculate
    global d_r_HB2_pin_localRecalculate
    global d_r_SHR2_pin_localRecalculate
    global d_r_d_result_HB_pin_localRecalculate
    global d_r_d_result_SHR_pin_localRecalculate
    global d_r_text_HB_fix_localRecalculate
    global d_r_text_SHR_fix_localRecalculate 
    global d_r_HB1_fix_localRecalculate 
    global d_r_SHR1_fix_localRecalculate 
    global d_r_HB2_fix_localRecalculate
    global d_r_SHR2_fix_localRecalculate 
    global d_r_d_result_HB_fix_localRecalculate 
    global d_r_d_result_SHR_fix_localRecalculate 
    global d_fallaContinouos_localRecalculate
    global d_r_HB1_hjs_localRecalculate 
    global d_r_SHR1_hjs_localRecalculate 
    global d_r_HB2_hjs_localRecalculate 
    global d_r_SHR2_hjs_localRecalculate 
    global d_r_d_result_HB_hjs_localRecalculate
    global d_r_d_result_SHR_hjs_localRecalculate 
    global d_r_text_HB_hjs_localRecalculate 
    global d_r_text_SHR_hjs_localRecalculate
    global d_current_status_hb_localRecalculate 
    global d_current_status_shr_localRecalculate 
    global d_sf_localRecalculate 
    global d_Span_SVRating_localRecalculate
    global d_estructure_Type_convert_localRecalculate 
    global d_current_status_hb_hjs_localRecalculate 
    global d_current_status_shr_hjs_localRecalculate
    global d_ldds_f_localRecalculate 
    global d_ldds_position_f_localRecalculate 
    global valid_data_localRecalculate 
    global d_extra_check_hj_localRecalculate
    global d_StructureKey
    global notice_reference
    global vehicle_assessed
    global d_workssheetLB4coma2masI
    global d_workssheetLB5coma2masI
    global workssheetLB10masIcoma22
    global workssheetLB10masIcoma24
    global d_calc_type_localRecalculate
    global d_comments_localRecalculate
    global total_structures
    global title
    global jtype
    global definitions
    global schema
    global timestamp
    global global_status
    global d_ESRN
    global d_all_Span_SVRating
    global sequence_number



    data={}    
    data['variables'] = []
    data['variables'].append({
    'd_StructureKey':d_StructureKey,
    'd_current_status':d_current_status_localRecalculate,
    'd_HB_or_SV':d_HB_or_SV_localRecalculate,
    'd_HB_or_SV_value':d_HB_or_SV_value_localRecalculate,
    'notice_reference':notice_reference,
    'd_r_St_type':d_r_St_type_localRecalculate,
    'd_r_HB1':d_r_HB1_localRecalculate,
    'd_r_text_HB':d_r_text_HB_localRecalculate,
    'd_r_HB2':d_r_HB2_localRecalculate,
    'd_r_d_result_HB':d_r_d_result_HB_localRecalculate,
    'd_r_SHR1':d_r_SHR1_localRecalculate,
    'd_r_text_SHR':d_r_text_SHR_localRecalculate,
    'd_r_SHR2':d_r_SHR2_localRecalculate,
    'd_r_d_result_SHR':d_r_d_result_SHR_localRecalculate,
    'vehicle_assessed':vehicle_assessed,
    'd_r_text_HB_pin':d_r_text_HB_pin_localRecalculate,
    'd_r_text_SHR_pin': d_r_text_SHR_pin_localRecalculate,
    'd_r_HB1_pin':d_r_HB1_pin_localRecalculate,
    'd_r_SHR1_pin':d_r_SHR1_pin_localRecalculate,
    'd_r_HB2_pin':d_r_HB2_pin_localRecalculate,
    'd_r_SHR2_pin':d_r_SHR2_pin_localRecalculate,
    'd_r_d_result_HB_pin': d_r_d_result_HB_pin_localRecalculate,
    'd_r_d_result_SHR_pin': d_r_d_result_SHR_pin_localRecalculate,
    'd_r_text_HB_fix':d_r_text_HB_fix_localRecalculate,
    'd_r_text_SHR_fix': d_r_text_SHR_fix_localRecalculate,
    'd_r_HB1_fix':d_r_HB1_fix_localRecalculate,
    'd_r_SHR1_fix':d_r_SHR1_fix_localRecalculate,
    'd_r_HB2_fix':d_r_HB2_fix_localRecalculate,
    'd_r_SHR2_fix':d_r_SHR2_fix_localRecalculate,
    'd_r_d_result_HB_fix': d_r_d_result_HB_fix_localRecalculate,
    'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix_localRecalculate,
    'd_fallaContinouos':d_fallaContinouos_localRecalculate,
    'd_r_HB1_hjs':d_r_HB1_hjs_localRecalculate,
    'd_r_SHR1_hjs':d_r_SHR1_hjs_localRecalculate,
    'd_r_HB2_hjs':d_r_HB2_hjs_localRecalculate,
    'd_r_SHR2_hjs':d_r_SHR2_hjs_localRecalculate,
    'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs_localRecalculate,
    'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs_localRecalculate,
    'd_r_text_HB_hjs': d_r_text_HB_hjs_localRecalculate,
    'd_r_text_SHR_hjs':d_r_text_SHR_hjs_localRecalculate,
    'd_current_status_hb':d_current_status_hb_localRecalculate,
    'd_current_status_shr':d_current_status_shr_localRecalculate,
    'd_sf':d_sf_localRecalculate,
    'd_Span_SVRating':d_Span_SVRating_localRecalculate,
    'd_estructure_Type_convert':d_estructure_Type_convert_localRecalculate,
    'd_current_status_hb_hjs': d_current_status_hb_hjs_localRecalculate,
    'd_current_status_shr_hjs':d_current_status_shr_hjs_localRecalculate,
    'd_ldds_f':d_ldds_f_localRecalculate,
    'd_ldds_position_f':d_ldds_position_f_localRecalculate,
    'valid_data':valid_data,
    'd_extra_check_hj':d_extra_check_hj_localRecalculate,
    'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI,
    'd_workssheetLB5coma2masI':d_workssheetLB5coma2masI,
    'workssheetLB10masIcoma22':workssheetLB10masIcoma22,
    'workssheetLB10masIcoma24':workssheetLB10masIcoma24,
    'd_calc_type':d_calc_type_localRecalculate,
    'd_comments':d_comments_localRecalculate,
    'd_all_Span_HBRating':d_all_Span_HBRating_localRecalculate,
    'd_ESRN':d_ESRN,
    'd_all_Span_SVRating':d_all_Span_SVRating
    })
    data["id"]=notice_reference

    data["dolar_id"]=dolar_id
    data["title"]=title
    data["type"]=jtype
    data["definitions"]=definitions
    data["schema"]=schema
    data["timestamp"]=timestamp
    data["sequence_number"]=sequence_number


    collection_results.update({'id':notice_reference},data,upsert=True)

    jsontosave=request.GET['save']


    #### save data into collection_summary #############
    myquery = { "id": jsontosave }
    mydoc = collection_summary.find_one(myquery)
    matrix_output=mydoc["variables"][0]["matrix_output"]
    global_status=mydoc["variables"][0]["global result"]
    

    matrix_output=[[None for c in range(5)] for r in range(len(matrix_output))]
    i=-1
    for key in d_StructureKey:
        i=i+1
        matrix_output[i][0]=key
        matrix_output[i][1]=d_StructureKey[key]

    i=-1
    gstatus=0
    gstatus_caution=0
    for key in d_current_status_localRecalculate:
        i=i+1        
        matrix_output[i][2]=d_current_status_localRecalculate[key]
        if d_current_status_localRecalculate[key]=='FAIL':
            gstatus=1
        elif d_current_status_localRecalculate[key]=='CAUTION':
            gstatus_caution=1
    if(gstatus==1):
        global_status='FAIL'
    elif(gstatus_caution==1):
        global_status='CAUTION'
    else:
        global_status='OK'

    i=-1
    for key in d_comments_localRecalculate:
        i=i+1
        matrix_output[i][3]=d_comments_localRecalculate[key]
    i=-1
    for key in d_ESRN:
        i=i+1
        matrix_output[i][4]=d_ESRN[key]


    string_comments="Lorem ipsum dolor"
    
    for key in d_comments_localRecalculate:
        if d_comments_localRecalculate[key]=="Unable to perform assessment - structure not assessed due to data issue":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Structure type not supported by Alsat":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Weight restriction applayed":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Data issue span sequence position duplicated":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Data issue span sequence position missing":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Data issue span length missing":
            string_comments="Unable to assess one or more structures"
        elif d_comments_localRecalculate[key]=="Unable to perform assessment - Data issue structure rating missing":
            string_comments="Unable to assess one or more structures"

    data={}      
    data['variables'] = []
    data['variables'].append({
    "global result": global_status,
    "matrix_output":matrix_output,
    "d_comments":string_comments,
    "d_ESRN":d_ESRN,
    })
    data["id"]=jsontosave
    collection_summary.update({'id':jsontosave}, data, upsert=True)


    datatext=writejson_save()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certificate_file, keyfile=certificate_secret)
    
    data='/app/' + datatext
    with open(data) as outfile:
        data = json.load(outfile)
        json_data = json.dumps(data)
        try:
            request_url_upload='/uploader'
            headers_req={'Content-Type': 'application/json'}
            connection = http.client.HTTPSConnection(host, port=443, context=context)
            connection.request('PUT', request_url_upload, json_data, headers_req)
            response2=connection.getresponse()
            print("_______response recalculate________")
            print(response2.read().decode())
        except ConnectionError:
            print("NO CONNECTION")



    return render(request, 'summary.html',{'matrix_output':matrix_output,'global_status':global_status, 'json':jsontosave})

def writejson_save():
    global timestamp
    global ESRN
    global global_status
    global d_current_status_localRecalculate
    global d_estructure_Type_convert
    global sequence_number
    global d_ESRN
    global global_status

    data_json={}
    esdalstructureresults={}
    dateTimeObj = datetime.now()

    
    esdalstructureresultsVector=[]
    for i in range(1,total_structures+1):
        str_current_status= d_current_status_localRecalculate[str(i)]
        string_d_comments=""
        esdalstructureresultsValues = {}
        esdalstructureresultsValues["ESRN"]=d_ESRN[str(i)]
        esdalstructureresultsValues["StructureKey"]=d_StructureKey[str(i)]
        esdalstructureresultsValues["StructureCalculationType"]=d_estructure_Type_convert[str(i)]
        esdalstructureresultsValues["result_structure"]=str_current_status 
        esdalstructureresultsValues["sf"]=sf
        esdalstructureresultsValues["comments_for_haulier"]=""
        esdalstructureresultsValues["assessment_comments"]=string_d_comments

        esdalstructureresultsVector.append(esdalstructureresultsValues)

    esdalstructureresults['EsdalStructure'] = esdalstructureresultsVector


    data_json['$id'] = dolar_id
    data_json['title'] = title
    data_json['type'] = jtype
    data_json['definitions'] = definitions
    data_json['schema'] = schema


    data_json['properties'] = []
    data_json['properties'].append({   
        "sequence_number":sequence_number,
        "timestamp": timestamp,
        "timestamp_finish":str(dateTimeObj),
        "movement_id":notice_reference,
        "global_result": global_status,
        "global_comments":"",
    })

    data_json['properties'].append(esdalstructureresults)

    v=notice_reference.split("/")
    string_notice_reference=""
    for x in range(0,len(v)):
        if x<len(v)-1:
            string_notice_reference=string_notice_reference+v[x]+"-"
        else:
            string_notice_reference=string_notice_reference+v[x]
    datatext=string_notice_reference+'.json'

    with open(datatext, 'w') as outfile:
        json.dump(data_json, outfile , indent=4)

    return datatext

def recalculate_previous(request):
    structureVSjson=request.GET['structureAndJson']
    structureVSjson=structureVSjson.split("&&")

    structure=structureVSjson[0]
    json=(structureVSjson[1])

    myquery = { "id": json }
    mydoc = collection_results.find_one(myquery)
    

    d_StructureKey=mydoc["variables"][0]["d_StructureKey"]
    d_current_status=mydoc["variables"][0]["d_current_status"]
    d_HB_or_SV=mydoc["variables"][0]["d_HB_or_SV"]
    d_HB_or_SV_value=mydoc["variables"][0]["d_HB_or_SV_value"]
    notice_reference=mydoc["variables"][0]["notice_reference"]
    d_r_St_type=mydoc["variables"][0]["d_r_St_type"]
    d_r_HB1=mydoc["variables"][0]["d_r_HB1"]
    d_r_HB2=mydoc["variables"][0]["d_r_HB2"]
    d_r_d_result_HB=mydoc["variables"][0]["d_r_d_result_HB"]
    d_r_SHR1=mydoc["variables"][0]["d_r_SHR1"]
    d_r_text_SHR=mydoc["variables"][0]["d_r_text_SHR"]
    d_r_SHR2=mydoc["variables"][0]["d_r_SHR2"]
    d_r_d_result_SHR=mydoc["variables"][0]["d_r_d_result_SHR"]
    d_r_text_HB=mydoc["variables"][0]["d_r_text_HB"]
    d_r_text_HB=mydoc["variables"][0]["d_r_text_HB"]
    vehicle_assessed=mydoc["variables"][0]["vehicle_assessed"]
    d_r_text_HB_pin=mydoc["variables"][0]["d_r_text_HB_pin"]
    d_r_text_SHR_pin=mydoc["variables"][0]["d_r_text_SHR_pin"]
    d_r_HB1_pin=mydoc["variables"][0]["d_r_HB1_pin"]
    d_r_SHR1_pin=mydoc["variables"][0]["d_r_SHR1_pin"]
    d_r_HB2_pin=mydoc["variables"][0]["d_r_HB2_pin"]
    d_r_SHR2_pin=mydoc["variables"][0]["d_r_SHR2_pin"]
    d_r_d_result_HB_pin=mydoc["variables"][0]["d_r_d_result_HB_pin"]
    d_r_d_result_SHR_pin=mydoc["variables"][0]["d_r_d_result_SHR_pin"]
    d_r_text_HB_fix=mydoc["variables"][0]["d_r_text_HB_fix"]
    d_r_text_SHR_fix=mydoc["variables"][0]["d_r_text_SHR_fix"]
    d_r_HB1_fix=mydoc["variables"][0]["d_r_HB1_fix"]
    d_r_SHR1_fix=mydoc["variables"][0]["d_r_SHR1_fix"]
    d_r_HB2_fix=mydoc["variables"][0]["d_r_HB2_fix"]
    d_r_SHR2_fix=mydoc["variables"][0]["d_r_SHR2_fix"]
    d_r_d_result_HB_fix=mydoc["variables"][0]["d_r_d_result_HB_fix"]
    d_r_d_result_SHR_fix=mydoc["variables"][0]["d_r_d_result_SHR_fix"]
    d_fallaContinouos=mydoc["variables"][0]["d_fallaContinouos"]
    d_r_HB1_hjs=mydoc["variables"][0]["d_r_HB1_hjs"]
    d_r_SHR1_hjs=mydoc["variables"][0]["d_r_SHR1_hjs"]
    d_r_HB2_hjs=mydoc["variables"][0]["d_r_HB2_hjs"]
    d_r_SHR2_hjs=mydoc["variables"][0]["d_r_SHR2_hjs"]
    d_r_d_result_HB_hjs=mydoc["variables"][0]["d_r_d_result_HB_hjs"]
    d_r_d_result_SHR_hjs=mydoc["variables"][0]["d_r_d_result_SHR_hjs"]
    d_r_text_HB_hjs=mydoc["variables"][0]["d_r_text_HB_hjs"]
    d_r_text_SHR_hjs=mydoc["variables"][0]["d_r_text_SHR_hjs"]
    d_current_status_hb=mydoc["variables"][0]["d_current_status_hb"]
    d_current_status_shr=mydoc["variables"][0]["d_current_status_shr"]
    d_sf=mydoc["variables"][0]["d_sf"]
    d_Span_SVRating=mydoc["variables"][0]["d_Span_SVRating"]
    d_estructure_Type_convert=mydoc["variables"][0]["d_estructure_Type_convert"]
    d_current_status_hb_hjs=mydoc["variables"][0]["d_current_status_hb_hjs"]
    d_current_status_shr_hjs=mydoc["variables"][0]["d_current_status_shr_hjs"]
    d_ldds_f=mydoc["variables"][0]["d_ldds_f"]    
    d_ldds_position_f=mydoc["variables"][0]["d_ldds_position_f"]
    valid_data=mydoc["variables"][0]["valid_data"]
    d_extra_check_hj=mydoc["variables"][0]["d_extra_check_hj"]
    d_workssheetLB4coma2masI=mydoc["variables"][0]["d_workssheetLB4coma2masI"]
    d_calc_type=mydoc["variables"][0]["d_calc_type"]
    d_comments=mydoc["variables"][0]["d_comments"]
    d_all_Span_HBRating=mydoc["variables"][0]["d_all_Span_HBRating"]
    d_all_Span_SVRating=mydoc["variables"][0]["d_all_Span_SVRating"]
    d_ESRN=mydoc["variables"][0]["d_ESRN"]


    d_estructure_Type_convert_modify={}
    for key in d_estructure_Type_convert:
        if d_estructure_Type_convert[key]=="Not Defined":
            d_estructure_Type_convert_modify[key]="Continuous"
        else:
            d_estructure_Type_convert_modify[key]=d_estructure_Type_convert[key]


    d_calc_type_modify={}
    for key in d_calc_type:
        if d_calc_type[key]=="Not Defined":
            d_calc_type_modify[key]="Factored"
        else:
            d_calc_type_modify[key]=d_calc_type[key]



    d_workssheetLB4coma2masI_f={}
    count=0
    v_workssheetLB4coma2masI_f=[]
    for x in d_workssheetLB4coma2masI:
        for y in d_workssheetLB4coma2masI[x]:
            if int(y)==0:
                count=count+1
            elif ( (int(y)!=0) and count<2):
                v_workssheetLB4coma2masI_f.append(y)
        count=0
        d_workssheetLB4coma2masI_f[x]=v_workssheetLB4coma2masI_f
        v_workssheetLB4coma2masI_f=[]



    
    return render(request, 'result_engineer_mofier.html',{'structure':structure, 'd_StructureKey':d_StructureKey, 'd_current_status':d_current_status ,'d_HB_or_SV':d_HB_or_SV,\
        'd_HB_or_SV_value':d_HB_or_SV_value,  'notice_reference':notice_reference,'d_r_St_type':d_r_St_type, 'd_r_HB1':d_r_HB1, 'd_r_text_HB':d_r_text_HB,\
        'd_r_HB2':d_r_HB2, 'd_r_d_result_HB':d_r_d_result_HB,'d_r_SHR1':d_r_SHR1 ,'d_r_text_SHR':d_r_text_SHR, 'd_r_SHR2':d_r_SHR2, 'd_r_d_result_SHR':d_r_d_result_SHR,\
        'vehicle_assessed':vehicle_assessed, 'd_r_text_HB_pin':d_r_text_HB_pin,'d_r_text_SHR_pin': d_r_text_SHR_pin, 'd_r_HB1_pin':d_r_HB1_pin,'d_r_SHR1_pin':d_r_SHR1_pin,\
        'd_r_HB2_pin':d_r_HB2_pin, 'd_r_SHR2_pin':d_r_SHR2_pin, 'd_r_d_result_HB_pin': d_r_d_result_HB_pin,'d_r_d_result_SHR_pin': d_r_d_result_SHR_pin,\
        'd_r_text_HB_fix':d_r_text_HB_fix,'d_r_text_SHR_fix': d_r_text_SHR_fix, 'd_r_HB1_fix':d_r_HB1_fix,'d_r_SHR1_fix':d_r_SHR1_fix, 'd_r_HB2_fix':d_r_HB2_fix,\
        'd_r_SHR2_fix':d_r_SHR2_fix, 'd_r_d_result_HB_fix': d_r_d_result_HB_fix, 'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix, 'd_fallaContinouos':d_fallaContinouos,\
        'd_r_HB1_hjs':d_r_HB1_hjs, 'd_r_SHR1_hjs':d_r_SHR1_hjs, 'd_r_HB2_hjs':d_r_HB2_hjs, 'd_r_SHR2_hjs':d_r_SHR2_hjs, 'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs,\
        'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs, 'd_r_text_HB_hjs': d_r_text_HB_hjs, 'd_r_text_SHR_hjs':d_r_text_SHR_hjs,\
        'd_current_status_hb':d_current_status_hb, 'd_current_status_shr':d_current_status_shr, 'd_sf':d_sf, 'd_Span_SVRating':d_Span_SVRating,\
        'd_estructure_Type_convert':d_estructure_Type_convert_modify, 'd_current_status_hb_hjs': d_current_status_hb_hjs, 'd_current_status_shr_hjs':d_current_status_shr_hjs,\
        'd_ldds_f':d_ldds_f, 'd_ldds_position_f':d_ldds_position_f, 'valid_data':valid_data, 'd_extra_check_hj':d_extra_check_hj,\
        'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI_f, 'd_calc_type':d_calc_type_modify, 'd_comments':d_comments, 'd_all_Span_HBRating':d_all_Span_HBRating,\
        'd_all_Span_SVRating':d_all_Span_SVRating,'d_ESRN':d_ESRN,
        })

def recalculate(request):
    global MaxMoveMomHB11
    global MaxMoveMomHB22
    global MaxMoveShrHB11
    global MaxMoveShrHB22
    global HB_rating
    global Reserve_Factor
    global d_StructureKey
    global d_HB_or_SV_value
    global d_HB_or_SV
    global workssheetLB4coma2masI
    global d_workssheetLB4coma2masI
    global workssheetLB5coma2masI
    global d_workssheetLB5coma2masI
    global OPTlhfixed
    global OPTlhpin
    global OPTrhfixed
    global OPTrhpin
    global sf
    global SV_Rating
    global workssheetLB10masIcoma22
    global workssheetLB10masIcoma24
    global HB_or_SV
    global Ldds
    global Ldds_position
    global valid_data
    global notice_reference
    global vehicle_assessed
    global Factored
    global NoOF
    global NoDF
    global NoFact
    global global_hj
    global d_all_Span_HBRating
    global total_structures
    global dolar_id
    global title
    global jtype
    global definitions
    global schema
    global timestamp
    global d_estructure_Type_convert
    global sequence_number
    global d_ESRN
    global d_all_Span_SVRating


    valid_data=1
    
    

    v1 = request.GET['vCalcType']
    v2 = request.GET['vEstType']
    v3 = request.GET['vFactor']
    v4 = request.GET['vSF']
    v5 = request.GET['vCalcTypeButton']

    try:
        Ldds=int(request.GET['ldds'])
    except:
        Ldds=0

    try:
        Ldds_position=int(request.GET['ldds_position'])
    except:
        Ldds_position=0



    structureAndJson = request.GET['structureAndJson']
    v_structureAndJson=structureAndJson.split("&&")
    structure=v_structureAndJson[0]
    json=v_structureAndJson[1]


    myquery = { "id": json }
    mydoc = collection_results.find_one(myquery)

    d_workssheetLB4coma2masI=mydoc["variables"][0]["d_workssheetLB4coma2masI"]
    d_workssheetLB5coma2masI=mydoc["variables"][0]["d_workssheetLB5coma2masI"]
    d_HB_or_SV_value=mydoc["variables"][0]["d_HB_or_SV_value"]
    d_HB_or_SV=mydoc["variables"][0]["d_HB_or_SV"]
    workssheetLB10masIcoma22=mydoc["variables"][0]["workssheetLB10masIcoma22"]
    workssheetLB10masIcoma24=mydoc["variables"][0]["workssheetLB10masIcoma24"]
    d_Span_SVRating=mydoc["variables"][0]["d_Span_SVRating"]
    d_StructureKey=mydoc["variables"][0]["d_StructureKey"]
    notice_reference=mydoc["variables"][0]["notice_reference"]
    vehicle_assessed=mydoc["variables"][0]["vehicle_assessed"]
    d_r_HB1=mydoc["variables"][0]["d_r_HB1"]
    d_r_SHR1=mydoc["variables"][0]["d_r_SHR1"]
    d_r_HB2=mydoc["variables"][0]["d_r_HB2"]
    d_r_SHR2=mydoc["variables"][0]["d_r_SHR2"]
    d_r_d_result_HB=mydoc["variables"][0]["d_r_d_result_HB"]
    d_r_d_result_SHR=mydoc["variables"][0]["d_r_d_result_SHR"]      
    d_r_HB1_pin=mydoc["variables"][0]["d_r_HB1_pin"]
    d_r_SHR1_pin=mydoc["variables"][0]["d_r_SHR1_pin"]
    d_r_HB2_pin=mydoc["variables"][0]["d_r_HB2_pin"]
    d_r_SHR2_pin=mydoc["variables"][0]["d_r_SHR2_pin"]
    d_r_d_result_HB_pin=mydoc["variables"][0]["d_r_d_result_HB_pin"]
    d_r_d_result_SHR_pin=mydoc["variables"][0]["d_r_d_result_SHR_pin"]
    d_r_HB1_fix=mydoc["variables"][0]["d_r_HB1_fix"]
    d_r_SHR1_fix=mydoc["variables"][0]["d_r_SHR1_fix"]
    d_r_HB2_fix=mydoc["variables"][0]["d_r_HB2_fix"]
    d_r_SHR2_fix=mydoc["variables"][0]["d_r_SHR2_fix"]
    d_r_d_result_HB_fix=mydoc["variables"][0]["d_r_d_result_HB_fix"]
    d_r_d_result_SHR_fix=mydoc["variables"][0]["d_r_d_result_SHR_fix"]
    d_r_HB1_hjs=mydoc["variables"][0]["d_r_HB1_hjs"]
    d_r_SHR1_hjs=mydoc["variables"][0]["d_r_SHR1_hjs"]
    d_r_HB2_hjs=mydoc["variables"][0]["d_r_HB2_hjs"]
    d_r_SHR2_hjs=mydoc["variables"][0]["d_r_SHR2_hjs"]
    d_r_d_result_HB_hjs=mydoc["variables"][0]["d_r_d_result_HB_hjs"]
    d_r_d_result_SHR_hjs=mydoc["variables"][0]["d_r_d_result_SHR_hjs"]
    #d_r_fallaContinouos=mydoc["variables"][0]["d_r_fallaContinouos"]
    d_r_St_type=mydoc["variables"][0]["d_r_St_type"]
    ####return variables#####
    d_r_text_HB=mydoc["variables"][0]["d_r_text_HB"]
    d_r_text_SHR=mydoc["variables"][0]["d_r_text_SHR"]
    d_current_status=mydoc["variables"][0]["d_current_status"]
    d_r_text_HB_pin=mydoc["variables"][0]["d_r_text_HB_pin"]
    d_r_text_SHR_pin=mydoc["variables"][0]["d_r_text_SHR_pin"]
    ###############################################d_current_status_pin=mydoc["variables"][0]["d_current_status_pin"]
    d_r_text_HB_fix=mydoc["variables"][0]["d_r_text_HB_fix"]
    d_r_text_SHR_fix=mydoc["variables"][0]["d_r_text_SHR_fix"]
    ###############################################d_current_status_fix=mydoc["variables"][0]["d_current_status_fix"]
    d_fallaContinouos=mydoc["variables"][0]["d_fallaContinouos"]
    d_r_text_HB_hjs=mydoc["variables"][0]["d_r_text_HB_hjs"]
    d_r_text_SHR_hjs=mydoc["variables"][0]["d_r_text_SHR_hjs"]
    d_current_status_hb=mydoc["variables"][0]["d_current_status_hb"]
    d_current_status_shr=mydoc["variables"][0]["d_current_status_shr"]
    d_sf=mydoc["variables"][0]["d_sf"]
    d_estructure_Type_convert=mydoc["variables"][0]["d_estructure_Type_convert"]
    d_current_status_hb_hjs=mydoc["variables"][0]["d_current_status_hb_hjs"]
    d_current_status_shr_hjs=mydoc["variables"][0]["d_current_status_shr_hjs"]
    d_extra_check_hj=mydoc["variables"][0]["d_extra_check_hj"]
    d_ldds_f=mydoc["variables"][0]["d_ldds_f"]
    d_ldds_position_f=mydoc["variables"][0]["d_ldds_position_f"]
    d_all_Span_HBRating=mydoc["variables"][0]["d_all_Span_HBRating"]
    d_comments=mydoc["variables"][0]["d_comments"]
    d_calc_type=mydoc["variables"][0]["d_calc_type"]
    d_ESRN=mydoc["variables"][0]["d_ESRN"]
    d_all_Span_SVRating=mydoc["variables"][0]["d_all_Span_SVRating"]


    dolar_id=mydoc['dolar_id']
    title=mydoc['title']
    jtype=mydoc['type']
    definitions=mydoc['definitions']
    schema=mydoc['schema']
    timestamp=mydoc['timestamp']
    sequence_number=mydoc['sequence_number']

    d_r_text_m_HB={}
    d_r_text_m_SHR={}
    d_current_status_pin={}
    d_current_status_fix={}


    globalvariables()

    total_structures=len(d_StructureKey)
    ##########inputs variables#######
    sf=float(v4)

    if v2=='Continuous':
        St_type="1"
    elif v2=='Box/Frame':
        St_type="2"
    elif v2=='Simply-Supported':
        St_type="3"
    elif v2=='Half Joint':
        St_type="4"

    d_r_St_type[structure]=St_type
    T_E=structure


    d_calc_type[str(T_E)]=''

    if (v5=='Factored'):
        Factored=1
        NoOF=0
        NoDF=0
        NoFact=0
        d_calc_type[str(T_E)]='Factored'
    elif (v5=='NoOF'):
        Factored=0
        NoOF=1
        NoDF=0
        NoFact=0
        d_calc_type[str(T_E)]='NoOF'
    elif (v5=='NoDF'):
        Factored=0
        NoOF=0
        NoDF=1
        NoFact=0
        d_calc_type[str(T_E)]='NoDF'
    elif (v5=='NoFact'):
        Factored=0
        NoOF=0
        NoDF=0
        NoFact=1
        d_calc_type[str(T_E)]='NoFact'


    ######################inicializar los diccionarios pero solo para la estructura a recalcular################
    d_current_status[T_E]=''
    d_HB_or_SV[T_E]=''
    d_r_HB1[T_E]=''
    d_r_text_HB[T_E]=''
    d_r_HB2[T_E]=''
    d_r_d_result_HB[T_E]=''
    d_r_SHR1[T_E]=''
    d_r_text_SHR[T_E]=''
    d_r_SHR2[T_E]=''
    d_r_d_result_SHR[T_E]=''
    d_r_text_HB_pin[T_E]=''
    d_r_text_SHR_pin[T_E]=''
    d_r_HB1_pin[T_E]=''
    d_r_SHR1_pin[T_E]=''
    d_r_HB2_pin[T_E]=''
    d_r_SHR2_pin[T_E]=''
    d_r_d_result_HB_pin[T_E]=''
    d_r_d_result_SHR_pin[T_E]=''
    d_r_text_HB_fix[T_E]=''
    d_r_text_SHR_fix[T_E]=''
    d_r_HB1_fix[T_E]=''
    d_r_SHR1_fix[T_E]=''
    d_r_HB2_fix[T_E]=''
    d_r_SHR2_fix[T_E]=''
    d_r_d_result_HB_fix[T_E]=''
    d_r_d_result_SHR_fix[T_E]=''
    d_fallaContinouos[T_E]=''
    d_r_HB1_hjs[T_E]=''
    d_r_SHR1_hjs[T_E]=''
    d_r_HB2_hjs[T_E]=''
    d_r_SHR2_hjs[T_E]=''
    d_r_d_result_HB_hjs[T_E]=''
    d_r_d_result_SHR_hjs[T_E]=''
    d_r_text_HB_hjs[T_E]=''
    d_r_text_SHR_hjs[T_E]=''
    d_current_status_hb[T_E]=''
    d_current_status_shr[T_E]=''
    d_sf[T_E]=''
    d_Span_SVRating[T_E]=''
    d_estructure_Type_convert[T_E]=''
    d_current_status_hb_hjs[T_E]=''
    d_current_status_shr_hjs[T_E]=''
    d_ldds_f[T_E]=''
    d_ldds_position_f[T_E]=''
    d_extra_check_hj[T_E]=''
    d_comments[T_E]=''

    d_ldds_f[T_E]=Ldds
    d_ldds_position_f[T_E]=Ldds_position
    ################################################3
    
    if (v1=='HB'): 
        HB_or_SV="HB"
        HB_rating=float(v3) 
        d_HB_or_SV_value[T_E]=HB_rating

    else:    
        HB_or_SV="SV"
        Reserve_Factor=float(v3)
        d_HB_or_SV_value[T_E]=Reserve_Factor
        SV_Rating=v1
        d_Span_SVRating[T_E]=SV_Rating

    
    ##################################
    d_HB_or_SV[T_E]=HB_or_SV
    d_sf[T_E]=sf

    global_hj=0

    d_comments[T_E]="Lorem ipsum dolor"

    v_all=[]
    for x in d_workssheetLB4coma2masI:
        if x==T_E:
            for y in d_workssheetLB4coma2masI[x]:
                v_all.append(y)
            workssheetLB4coma2masI=v_all
            v_all=[]

    #workssheetLB5coma2masI=d_workssheetLB5coma2masI[T_E]
    v_all=[]
    for x in d_workssheetLB5coma2masI:
        if x==T_E:
            for y in d_workssheetLB5coma2masI[x]:
                v_all.append(y)
            workssheetLB5coma2masI=v_all
            v_all=[]


    if(St_type=="1"):      
        d_estructure_Type_convert[T_E]='Continuous'     
        #####botones#####
        OPTlhfixed=0
        OPTlhpin=1
        OPTrhfixed=0
        OPTrhpin=1           


        PREPARE_CALCS()

        if(HB_or_SV=="HB"):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]

        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0########?????
        
        workssheetLB3coma2masI=np.zeros(31)


        PREPARE_CALCS()
        MaxMoveMomHB2, MaxMoveShrHB2=Load_Axles_AIL()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]

        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]


        HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR =comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)

        d_r_HB1[T_E]=HB1
        d_r_SHR1[T_E]=SHR1
        d_r_HB2[T_E]=HB2
        d_r_SHR2[T_E]=SHR2
        d_r_d_result_HB[T_E]=d_result_HB
        d_r_d_result_SHR[T_E]=d_result_SHR

       
        ##################################### RETURN VALUES ########################            
        ######## HB1 ########
        v_text_m_HB=[]
        i=1           
        nciclos=int(len(d_r_HB1[T_E])/2)
        for i in range(1,nciclos+1):
            a="Mom at sup " + str(i)
            b="Mom at span " + str(i)
            v_text_m_HB.append(a)
            v_text_m_HB.append(b)
        c="Mom at sup " + str(i+1)
        v_text_m_HB.append(c)

        d_r_text_HB[T_E]=v_text_m_HB


        ###### SHR1 #####
        v_text_m_SHR=[]
        i=1
        nciclos=int(len(d_r_SHR1[T_E])/2)
        for i in range(1,nciclos+1):
            a="Span " + str(i) + " left end"
            b="Span " + str(i) + " right end"
            v_text_m_SHR.append(a)
            v_text_m_SHR.append(b)

        d_r_text_SHR[T_E]=v_text_m_SHR

        fail_hb=0
        fail_shr=0
        fail=0

        caution=0
        caution_hb=0
        caution_shr=0
        for x in d_r_d_result_HB[T_E]:
            if (d_r_d_result_HB[T_E][x]=='FAIL'):
                fail=1
                fail_hb=1
            elif (d_r_d_result_HB[T_E][x]=='CAUTION'):
                caution=1
                caution_hb=1

        if fail_hb==1:
            d_current_status_hb[T_E]="FAIL"
        elif caution_hb==1:
            d_current_status_hb[T_E]="CAUTION"
        else:
            d_current_status_hb[T_E]="OK"

        for x in d_r_d_result_SHR[T_E]:
            if (d_r_d_result_SHR[T_E][x]=='FAIL'):
                fail=1
                fail_shr=1
            elif (d_r_d_result_SHR[T_E][x]=='CAUTION'):
                caution=1
                caution_shr=1

        if fail_shr==1:
            d_current_status_shr[T_E]="FAIL"
        elif caution_shr==1:
            d_current_status_shr[T_E]="CAUTION"
        else:
            d_current_status_shr[T_E]="OK"

        if fail==1:
            d_current_status[T_E]="FAIL"
        elif caution==1:
            d_current_status[T_E]="CAUTION"
        else:
            d_current_status[T_E]="OK"
                
    if(St_type=="2"):  
        d_estructure_Type_convert[T_E]='Box/Frame'   
        
        #####botones#####
        OPTlhfixed=0
        OPTlhpin=1
        OPTrhfixed=0
        OPTrhpin=1        

        Factored=1
        NoOF=0
        NoDF=0
        NoFact=0

        PREPARE_CALCS()
        if(HB_or_SV=="HB"):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]
        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))
        MaxMoveMomHB22=np.zeros((100,7))
        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))        
        OpeninFlag=0########?????               
        workssheetLB3coma2masI=np.zeros(31)       


        PREPARE_CALCS()
        MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]
        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]
    
        HB1_pin, SHR1_pin, HB2_pin, SHR2_pin, d_result_HB_pin, d_result_SHR_pin = comparative(MaxMoveMomHB11, MaxMoveMomHB22, MaxMoveShrHB11, MaxMoveShrHB22)

        d_r_HB1_pin[T_E]=HB1_pin
        d_r_SHR1_pin[T_E]=SHR1_pin
        d_r_HB2_pin[T_E]=HB2_pin
        d_r_SHR2_pin[T_E]=SHR2_pin
        d_r_d_result_HB_pin[T_E]=d_result_HB_pin
        d_r_d_result_SHR_pin[T_E]=d_result_SHR_pin



        ##################################### RETURN VALUES ########################            
        ######## HB1 ########
        v_text_m_HB=[]
        i=1           
        nciclos=int(len(d_r_HB1_pin[T_E])/2)
        for i in range(1,nciclos+1):
            a="Mom at sup " + str(i)
            b="Mom at span " + str(i)
            v_text_m_HB.append(a)
            v_text_m_HB.append(b)
        c="Mom at sup " + str(i+1)
        v_text_m_HB.append(c)

        d_r_text_HB_pin[T_E]=v_text_m_HB


        ###### SHR1 #####
        v_text_m_SHR=[]
        i=1
        nciclos=int(len(d_r_SHR1_pin[T_E])/2)
        for i in range(1,nciclos+1):
            a="Span " + str(i) + " left end"
            b="Span " + str(i) + " right end"
            v_text_m_SHR.append(a)
            v_text_m_SHR.append(b)

        d_r_text_SHR_pin[T_E]=v_text_m_SHR


        fail=0
        caution=0
        for x in d_r_d_result_HB_pin[T_E]:
            if (d_r_d_result_HB_pin[T_E][x]=='FAIL'):
                fail=1
            elif (d_r_d_result_HB_pin[T_E][x]=='CAUTION'):
                caution=1
        for x in d_r_d_result_SHR_pin[T_E]:
            if (d_r_d_result_SHR_pin[T_E][x]=='FAIL'):
                fail=1
            elif (d_r_d_result_SHR_pin[T_E][x]=='CAUTION'):
                caution=1
        if fail==1:
            d_current_status_pin[T_E]="FAIL"
        elif caution==1:
            d_current_status_pin[T_E]="CAUTION"
        else:
            d_current_status_pin[T_E]="OK"



        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))
        MaxMoveMomHB11=np.zeros((100,7))
        MaxMoveMomHB22=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0

        #####botones#####3
        OPTlhfixed=1
        OPTlhpin=0
        OPTrhfixed=1
        OPTrhpin=0
        
        workssheetLB3coma2masI=np.zeros(31)


        PREPARE_CALCS()

        if(HB_or_SV=="HB"):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]
        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))
        MaxMoveMomHB22=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0            
        workssheetLB3coma2masI=np.zeros(31)


        PREPARE_CALCS()
        MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]
        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]
    
        HB1_fix, SHR1_fix, HB2_fix, SHR2_fix, d_result_HB_fix, d_result_SHR_fix=comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11, MaxMoveShrHB22)

        d_r_HB1_fix[T_E]=HB1_fix
        d_r_SHR1_fix[T_E]=SHR1_fix
        d_r_HB2_fix[T_E]=HB2_fix
        d_r_SHR2_fix[T_E]=SHR2_fix
        d_r_d_result_HB_fix[T_E]=d_result_HB_fix
        d_r_d_result_SHR_fix[T_E]=d_result_SHR_fix

        ##################################### RETURN VALUES ########################            
        ######## HB1 ########
        v_text_m_HB=[]
        i=1           
        nciclos=int(len(d_r_HB1_fix[T_E])/2)
        for i in range(1,nciclos+1):
            a="Mom at sup " + str(i)
            b="Mom at span " + str(i)
            v_text_m_HB.append(a)
            v_text_m_HB.append(b)
        c="Mom at sup " + str(i+1)
        v_text_m_HB.append(c)

        d_r_text_HB_fix[T_E]=v_text_m_HB


        ###### SHR1 #####
        v_text_m_SHR=[]
        i=1
        nciclos=int(len(d_r_SHR1_pin[T_E])/2)
        for i in range(1,nciclos+1):
            a="Span " + str(i) + " left end"
            b="Span " + str(i) + " right end"
            v_text_m_SHR.append(a)
            v_text_m_SHR.append(b)

        d_r_text_SHR_fix[T_E]=v_text_m_SHR


        fail=0
        caution=0
        for x in d_r_d_result_HB_fix[T_E]:
            if (d_r_d_result_HB_fix[T_E][x]=='FAIL'):
                fail=1
            elif (d_r_d_result_HB_fix[T_E][x]=='CAUTION'):
                caution=1

        for x in d_r_d_result_SHR_fix[T_E]:
            if (d_r_d_result_SHR_fix[T_E][x]=='FAIL'):
                fail=1
            elif (d_r_d_result_SHR_fix[T_E][x]=='CAUTION'):
                caution=1
        if fail==1:
            d_current_status_fix[T_E]="FAIL"
        elif caution==1:
            d_current_status_fix[T_E]="CAUTION"
        else:
            d_current_status_fix[T_E]="OK"


        fail_hb=0
        fail_shr=0
        fail=0

        caution_hb=0
        caution_shr=0
        caution=0
        for x in d_r_d_result_HB_pin[T_E]:
            if (d_r_d_result_HB_pin[T_E][x]=='FAIL'):
                fail=1
                fail_hb=1
            elif (d_r_d_result_HB_pin[T_E][x]=='CAUTION'):
                caution=1
                caution_hb=1

        for x in d_r_d_result_HB_fix[T_E]:
            if (d_r_d_result_HB_fix[T_E][x]=='FAIL'):
                fail=1
                fail_hb=1
            elif (d_r_d_result_HB_fix[T_E][x]=='CAUTION'):
                caution=1
                caution_hb=1
        if fail_hb==1:
            d_current_status_hb[T_E]="FAIL"
        elif caution_hb==1:
            d_current_status_hb[T_E]="CAUTION"
        else:
            d_current_status_hb[T_E]="OK"


        for x in d_r_d_result_SHR_pin[T_E]:
            if (d_r_d_result_SHR_pin[T_E][x]=='FAIL'):
                fail=1
                fail_shr=1
            elif (d_r_d_result_SHR_pin[T_E][x]=='CAUTION'):
                caution=1
                caution_shr=1
        for x in d_r_d_result_SHR_fix[T_E]:
            if (d_r_d_result_SHR_fix[T_E][x]=='FAIL'):
                fail=1
                fail_shr=1
            elif (d_r_d_result_SHR_fix[T_E][x]=='CAUTION'):
                caution=1
                caution_shr=1

        if fail_shr==1:
            d_current_status_shr[T_E]="FAIL"
        elif caution_shr==1:
            d_current_status_shr[T_E]="CAUTION"
        else:
            d_current_status_shr[T_E]="OK"

        if (fail_hb==1 or fail_shr==1):
            d_current_status[T_E]='FAIL'
        elif (caution_hb==1 or caution_shr==1):
            d_current_status[T_E]='CAUTION'
        else:
            d_current_status[T_E]='OK'

    if(St_type=="3"):     
        d_estructure_Type_convert[T_E]='Simply-Supported'
        Simply_Supported=1

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))
        MaxMoveMomHB11=np.zeros((100,7))
        MaxMoveMomHB22=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0
        #####botones#####
        OPTlhfixed=0
        OPTlhpin=1
        OPTrhfixed=0
        OPTrhpin=1
        #################        
        workssheetLB3coma2masI=np.zeros(31)

        PREPARE_CALCS()
        v_HB1, v_SHR1, v_HB2, v_SHR2, v_d_result_HB, v_d_result_SHR=CALC_SS_HB_AIL() 

        d_r_HB1[T_E]=v_HB1
        d_r_SHR1[T_E]=v_SHR1
        d_r_HB2[T_E]=v_HB2
        d_r_SHR2[T_E]=v_SHR2
        d_r_d_result_HB[T_E]=v_d_result_HB
        d_r_d_result_SHR[T_E]=v_d_result_SHR   

        
        fail=0
        fail_hb=0
        fail_shr=0

        caution=0
        caution_hb=0
        caution_shr=0
        for x in range(0,len(d_r_d_result_HB[T_E])):
            for xx in range(0,len(d_r_d_result_HB[T_E][x])):
                if (d_r_d_result_HB[T_E][x][xx]=='FAIL'):
                    fail=1
                    fail_hb=1
                if (d_r_d_result_HB[T_E][x][xx]=='CAUTION'):
                    caution=1
                    caution_hb=1
        if fail_hb==1:
            d_current_status_hb[T_E]="FAIL"
        elif caution_hb==1:
            d_current_status_hb[T_E]="CAUTION"
        else:
            d_current_status_hb[T_E]="OK"


        for x in range(0,len(d_r_d_result_SHR[T_E])):
            for xx in range(0,len(d_r_d_result_SHR[T_E][x])):
                if (d_r_d_result_SHR[T_E][x][xx]=='FAIL'):
                    fail=1
                    fail_shr=1
                elif (d_r_d_result_SHR[T_E][x][xx]=='CAUTION'):
                    caution=1
                    caution_shr=1
        if fail_shr==1:
            d_current_status_shr[T_E]="FAIL"
        elif caution_shr==1:
            d_current_status_shr[T_E]="CAUTION"
        else:
            d_current_status_shr[T_E]="OK"

        if fail==1:
            d_current_status[T_E]="FAIL"
        elif caution==1:
            d_current_status[T_E]="CAUTION"
        else:
            d_current_status[T_E]="OK"


        #################################  RETURN  VALUES  ########################
        ###### HB1 #####
        v_text_m_HB=[]
        i=1

        for y in range(0,len(d_r_HB1[T_E])):  
            nciclos=int(len(d_r_HB1[T_E][y])/2)
            for i in range(1,nciclos+1):
                a="Mom at sup " + str(y+1)
                b="Mom at span " + str(y+1)
                v_text_m_HB.append(a)
                v_text_m_HB.append(b)
            c="Mom at sup " + str(y+1+1)
            v_text_m_HB.append(c)
            d_r_text_m_HB[str(y)]=v_text_m_HB
            v_text_m_HB=[]

        d_r_text_HB[T_E]=d_r_text_m_HB
        d_r_text_m_HB={}

        ###### SHR1 #####
        v_text_m_SHR=[]
        i=1
        for y in range(0,len(d_r_SHR1[T_E])):             
            nciclos=int(len(d_r_SHR1[T_E][y])/2)
            for i in range(1,nciclos+1):
                a="Span " + str(y+1) + " left end"
                b="Span " + str(y+1) + " right end"
                v_text_m_SHR.append(a)
                v_text_m_SHR.append(b)
            d_r_text_m_SHR[y]=v_text_m_SHR
            v_text_m_SHR=[]

        d_r_text_SHR[T_E]=d_r_text_m_SHR
        d_r_text_m_SHR={}

    if(St_type=="4"):
        d_estructure_Type_convert[T_E]='Half-Joint'

        OPTlhfixed=0
        OPTlhpin=1
        OPTrhfixed=0
        OPTrhpin=1 

        PREPARE_CALCS()
        if(HB_or_SV=="HB"):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]

        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0########?????        
        workssheetLB3coma2masI=np.zeros(31)

        PREPARE_CALCS()
        MaxMoveMomHB2, MaxMoveShrHB2=Load_Axles_AIL()

        for I in range(1, 100):
            for J in range(1, 7):
                MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]

        for I in range(1, 100):
            for J in range(1, 6):
                MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]


        HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR = comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)

        d_r_HB1[T_E]=HB1
        d_r_SHR1[T_E]=SHR1
        d_r_HB2[T_E]=HB2
        d_r_SHR2[T_E]=SHR2
        d_r_d_result_HB[T_E]=d_result_HB
        d_r_d_result_SHR[T_E]=d_result_SHR


        ##################################### RETURN VALUES ########################            
        ######## HB1 ########
        v_text_m_HB=[]
        i=1           
        nciclos=int(len(d_r_HB1[T_E])/2)
        for i in range(1,nciclos+1):
            a="Mom at sup " + str(i)
            b="Mom at span " + str(i)
            v_text_m_HB.append(a)
            v_text_m_HB.append(b)
        c="Mom at sup " + str(i+1)
        v_text_m_HB.append(c)

        d_r_text_HB[T_E]=v_text_m_HB


        ###### SHR1 #####
        v_text_m_SHR=[]
        i=1
        nciclos=int(len(d_r_SHR1[T_E])/2)
        for i in range(1,nciclos+1):
            a="Span " + str(i) + " left end"
            b="Span " + str(i) + " right end"
            v_text_m_SHR.append(a)
            v_text_m_SHR.append(b)

        d_r_text_SHR[T_E]=v_text_m_SHR
        ##################################### END RETURN VALUES ######################## 

        ##IF COUNTINOUS WORKS##    DO JUST ONE SIMPLY SUPPORTED

        fail=0
        fail_hb=0
        fail_shr=0
        fallaContinouos=0

        caution=0
        caution_hb=0
        caution_shr=0
        for x in d_r_d_result_HB[T_E]:
            if (d_r_d_result_HB[T_E][x]=='FAIL'):
                fail=1
                fail_hb=1
            elif (d_r_d_result_HB[T_E][x]=='CAUTION'):
                caution=1
                caution_hb=1
        for x in d_r_d_result_SHR[T_E]:
            if (d_r_d_result_SHR[T_E][x]=='FAIL'):
                fail=1
                fail_shr=1
            elif (d_r_d_result_SHR[T_E][x]=='CAUTION'):
                caution=1
                caution_shr=1


        if fail_hb==1:
            d_current_status_hb[T_E]='FAIL'
        elif caution_hb==1:
            d_current_status_hb[T_E]='CAUTION'
        else:
            d_current_status_hb[T_E]='OK'

        if fail_shr==1:
            d_current_status_shr[T_E]='FAIL'
        elif caution_shr==1:
            d_current_status_shr[T_E]='CAUTION'
        else:
            d_current_status_shr[T_E]='OK'

        if (fail==0):
            d_fallaContinouos[T_E]='OK'
            HB1_hjs, SHR1_hjs, HB2_hjs, SHR2_hjs, d_result_HB_hjs, d_result_SHR_hjs=HalfJointedSpan(HB_or_SV)               
        else:
            fallaContinouos=1
            d_fallaContinouos[T_E]='FAIL'


        if (fail==0 and valid_data==1):
            d_r_HB1_hjs[T_E]=HB1_hjs
            d_r_SHR1_hjs[T_E]=SHR1_hjs 
            d_r_HB2_hjs[T_E]=HB2_hjs
            d_r_SHR2_hjs[T_E]=SHR2_hjs
            d_r_d_result_HB_hjs[T_E]=d_result_HB_hjs
            d_r_d_result_SHR_hjs[T_E]=d_result_SHR_hjs

            ##################################### RETURN VALUES ########################            
            ######## HB1 ########
            v_text_m_HB=[]
            i=1
            nciclos=int(len(d_r_HB1_hjs[T_E])/2)
            for i in range(Ldds_position-1, Ldds_position-1 + nciclos):
                a="Mom at sup " + str(i)
                b="Mom at span " + str(i)
                v_text_m_HB.append(a)
                v_text_m_HB.append(b)
            c="Mom at sup " + str(i+1)
            v_text_m_HB.append(c)

            d_r_text_HB_hjs[T_E]=v_text_m_HB


            ###### SHR1 #####
            v_text_m_SHR=[]
            i=1
            nciclos=int(len(d_r_SHR1_hjs[T_E])/2)
            for i in range(Ldds_position-1, Ldds_position-1 + nciclos):
                a="Span " + str(i) + " left end"
                b="Span " + str(i) + " right end"
                v_text_m_SHR.append(a)
                v_text_m_SHR.append(b)

            d_r_text_SHR_hjs[T_E]=v_text_m_SHR
            

            #### if ok o fail
            fail_hjs=0
            fail_hb_hjs=0
            fail_shr_hjs=0

            caution_hjs=0
            caution_hb_hjs=0
            caution_shr_hjs=0
            for x in d_r_d_result_HB_hjs[T_E]:
                if (d_r_d_result_HB_hjs[T_E][x]=='FAIL'):
                    fail_hjs=1
                    fail_hb_hjs=1
                elif (d_r_d_result_HB_hjs[T_E][x]=='CAUTION'):
                    caution_hjs=1
                    caution_hb_hjs=1
            for x in d_r_d_result_SHR_hjs[T_E]:
                if (d_r_d_result_SHR_hjs[T_E][x]=='FAIL'):
                    fail_hjs=1
                    fail_shr_hjs=1
                elif (d_r_d_result_SHR_hjs[T_E][x]=='CAUTION'):
                    caution_hjs=1
                    caution_shr_hjs=1

            if fail_hjs==1:
                d_current_status[T_E]="FAIL"
            elif caution_hjs==1 or caution==1:
                d_current_status[T_E]="CAUTION"
            else:
                d_current_status[T_E]="OK"


            if fail_hb_hjs==1:
                d_current_status_hb_hjs[T_E]='FAIL'
            elif caution_hb_hjs==1:
                d_current_status_hb_hjs[T_E]='CAUTION'
            else:
                d_current_status_hb_hjs[T_E]='OK'

            if fail_shr_hjs==1 :
                d_current_status_shr_hjs[T_E]='FAIL'
            elif caution_shr_hjs==1 :
                d_current_status_shr_hjs[T_E]='CAUTION'
            else:
                d_current_status_shr_hjs[T_E]='OK'

        else:
            d_current_status[T_E]="FAIL"




    global d_current_status_localRecalculate
    global d_HB_or_SV_localRecalculate
    global d_HB_or_SV_value_localRecalculate
    global d_r_St_type_localRecalculate
    global d_r_HB1_localRecalculate
    global d_r_text_HB_localRecalculate
    global d_r_HB2_localRecalculate
    global d_r_d_result_HB_localRecalculate
    global d_r_SHR1_localRecalculate
    global d_r_text_SHR_localRecalculate
    global d_r_SHR2_localRecalculate
    global d_r_d_result_SHR_localRecalculate
    global d_r_text_HB_pin_localRecalculate
    global d_r_text_SHR_pin_localRecalculate
    global d_r_HB1_pin_localRecalculate
    global d_r_SHR1_pin_localRecalculate
    global d_r_HB2_pin_localRecalculate
    global d_r_SHR2_pin_localRecalculate
    global d_r_d_result_HB_pin_localRecalculate
    global d_r_d_result_SHR_pin_localRecalculate
    global d_r_text_HB_fix_localRecalculate
    global d_r_text_SHR_fix_localRecalculate 
    global d_r_HB1_fix_localRecalculate 
    global d_r_SHR1_fix_localRecalculate 
    global d_r_HB2_fix_localRecalculate
    global d_r_SHR2_fix_localRecalculate 
    global d_r_d_result_HB_fix_localRecalculate 
    global d_r_d_result_SHR_fix_localRecalculate 
    global d_fallaContinouos_localRecalculate
    global d_r_HB1_hjs_localRecalculate 
    global d_r_SHR1_hjs_localRecalculate 
    global d_r_HB2_hjs_localRecalculate 
    global d_r_SHR2_hjs_localRecalculate 
    global d_r_d_result_HB_hjs_localRecalculate
    global d_r_d_result_SHR_hjs_localRecalculate 
    global d_r_text_HB_hjs_localRecalculate 
    global d_r_text_SHR_hjs_localRecalculate
    global d_current_status_hb_localRecalculate 
    global d_current_status_shr_localRecalculate 
    global d_sf_localRecalculate 
    global d_Span_SVRating_localRecalculate
    global d_estructure_Type_convert_localRecalculate 
    global d_current_status_hb_hjs_localRecalculate 
    global d_current_status_shr_hjs_localRecalculate
    global d_ldds_f_localRecalculate 
    global d_ldds_position_f_localRecalculate 
    global valid_data_localRecalculate 
    global d_extra_check_hj_localRecalculate
    global d_calc_type_localRecalculate
    global d_all_Span_HBRating_localRecalculate
    global d_comments_localRecalculate
    



    d_current_status_localRecalculate={}
    d_current_status_localRecalculate=d_current_status
    d_HB_or_SV_localRecalculate={}
    d_HB_or_SV_localRecalculate=d_HB_or_SV
    d_HB_or_SV_value_localRecalculate={}
    d_HB_or_SV_value_localRecalculate=d_HB_or_SV_value
    d_r_St_type_localRecalculate={}
    d_r_St_type_localRecalculate=d_r_St_type
    d_calc_type_localRecalculate={}
    d_calc_type_localRecalculate=d_calc_type


    d_r_HB1_localRecalculate={}
    for x in d_r_HB1:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1[x]))]
        for y in range(0,  len(d_r_HB1[x]) ):
            try:
                if len(d_r_HB1[x][y][0]) > 1:
                    for w in d_r_HB1[x][y][0]:
                        matrix_output[y][0]=d_r_HB1[x][y][0].tolist()
                        matrix_output[y][1]=d_r_HB1[x][y][1].tolist()
                        matrix_output[y][2]=d_r_HB1[x][y][2].tolist()

            except:
                matrix_output[y][0]=d_r_HB1[x][y][0]
                matrix_output[y][1]=d_r_HB1[x][y][1]
                matrix_output[y][2]=d_r_HB1[x][y][2]
        d_r_HB1_localRecalculate[str(x)]=matrix_output

    d_r_text_HB_localRecalculate={}
    d_r_text_HB_l0={}
    d={}
    v=[]        
    for x in d_r_text_HB:#falla para Continuous(añadido [str(y)] en linea despues del for y  )
        if isinstance(d_r_text_HB[x], list):
            matrix_output=[[None for c in range( len(d_r_text_HB[x])) ] for r in range(1)]
            for w in d_r_text_HB[x]:
                v.append(w)
            d_r_text_HB_localRecalculate[str(x)]=v
            v=[]

        else:
            for y in range(0, len(d_r_text_HB[x]) ):
                try:
                    d_r_text_HB_l0[str(y)]=d_r_text_HB[x][str(y)]
                except:
                    d_r_text_HB_l0[str(y)]=d_r_text_HB[x][int(y)]

            d_r_text_HB_localRecalculate[str(x)]=d_r_text_HB_l0
            d_r_text_HB_l0={}


    

    d_r_HB2_localRecalculate={}
    for x in d_r_HB2:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2[x]))]
        for y in range(0,  len(d_r_HB2[x]) ):
            try:
                if len(d_r_HB2[x][y][0]) > 1:
                    for w in d_r_HB2[x][y][0]:
                        matrix_output[y][0]=d_r_HB2[x][y][0].tolist()
                        matrix_output[y][1]=d_r_HB2[x][y][1].tolist()
                        matrix_output[y][2]=d_r_HB2[x][y][2].tolist()
            except:
                matrix_output[y][0]=d_r_HB2[x][y][0]
                matrix_output[y][1]=d_r_HB2[x][y][1]
                matrix_output[y][2]=d_r_HB2[x][y][2]

        d_r_HB2_localRecalculate[str(x)]=matrix_output





    
    d_r_d_result_HB_localRecalculate={}
    d_r_d_result_HB_l0={}
    d={}
    v=[]
    for x in d_r_d_result_HB:#falla para Continuous(añadido insistance despues del for y  )
        if isinstance(d_r_d_result_HB[x], list):
            matrix_output=[[None for c in range( len(d_r_d_result_HB[x])) ] for r in range(1)]
            for w in d_r_d_result_HB[x]:
                for w1 in w:
                    d[str(w1)]=w[w1]
                v.append(d)
                d={}
            d_r_d_result_HB_localRecalculate[str(x)]=v
            v=[]

        else:
            for y in range(0,  len(d_r_d_result_HB[x]) ):
                try:
                    d_r_d_result_HB_l0[str(y)]=d_r_d_result_HB[x][y]
                except:
                    d_r_d_result_HB_l0[str(y)]=d_r_d_result_HB[x][str(y)]
            d_r_d_result_HB_localRecalculate[str(x)]=d_r_d_result_HB_l0
            d_r_d_result_HB_l0={}





    d_r_SHR1_localRecalculate={}
    for x in d_r_SHR1:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1[x]))]
        for y in range(0,  len(d_r_SHR1[x]) ):
            try:
                if len(d_r_SHR1[x][y][0]) > 1:
                    for w in d_r_SHR1[x][y][0]:
                        matrix_output[y][0]=d_r_SHR1[x][y][0].tolist()
                        matrix_output[y][1]=d_r_SHR1[x][y][1].tolist()
            except:
                matrix_output[y][0]=d_r_SHR1[x][y][0]
                matrix_output[y][1]=d_r_SHR1[x][y][1]
        d_r_SHR1_localRecalculate[str(x)]=matrix_output


    d_r_text_SHR_localRecalculate={}
    d_r_text_SHR_l0={}
    d={}
    v=[]
    for x in d_r_text_SHR:# falla continous añadido str(y) despues de for y
        if isinstance(d_r_text_SHR[x], list):
            matrix_output=[[None for c in range( len(d_r_text_SHR[x])) ] for r in range(1)]
            for w in d_r_text_SHR[x]:
                v.append(w)
            d_r_text_SHR_localRecalculate[str(x)]=v
            v=[]

        else:
            for y in range(0,  len(d_r_text_SHR[x]) ):
                try:
                    d_r_text_SHR_l0[str(y)]=d_r_text_SHR[x][str(y)]
                except:
                    d_r_text_SHR_l0[str(y)]=d_r_text_SHR[x][int(y)]

            d_r_text_SHR_localRecalculate[str(x)]=d_r_text_SHR_l0
            d_r_text_SHR_l0={}
    


    d_r_SHR2_localRecalculate={}
    for x in d_r_SHR2:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2[x]))]
        for y in range(0,  len(d_r_SHR2[x]) ):
            try:
                if len(d_r_SHR2[x][y][0]) > 1:
                    for w in d_r_SHR2[x][y][0]:
                        matrix_output[y][0]=d_r_SHR2[x][y][0].tolist()
                        matrix_output[y][1]=d_r_SHR2[x][y][1].tolist()
            except:
                matrix_output[y][0]=d_r_SHR2[x][y][0]
                matrix_output[y][1]=d_r_SHR2[x][y][1]
        d_r_SHR2_localRecalculate[str(x)]=matrix_output


    d_r_d_result_SHR_localRecalculate={}
    d_r_d_result_SHR_l0={}
    d={}
    v=[]

    for x in d_r_d_result_SHR:
        if isinstance(d_r_d_result_SHR[x], list):
            matrix_output=[[None for c in range( len(d_r_d_result_SHR[x])) ] for r in range(1)]
            for w in d_r_d_result_SHR[x]:
                for w1 in w:
                    d[str(w1)]=w[w1]
                v.append(d)
                d={}
            d_r_d_result_SHR_localRecalculate[str(x)]=v
            v=[] 

        else:
            for y in d_r_d_result_SHR[x]:
                d_r_d_result_SHR_l0[str(y)]=d_r_d_result_SHR[x][y]
            d_r_d_result_SHR_localRecalculate[str(x)]=d_r_d_result_SHR_l0
            d_r_d_result_SHR_l0={}



    d_r_text_HB_pin_localRecalculate={}
    d_r_text_HB_pin_localRecalculate=d_r_text_HB_pin
    d_r_text_SHR_pin_localRecalculate={}
    d_r_text_SHR_pin_localRecalculate=d_r_text_SHR_pin



    d_r_HB1_pin_localRecalculate={}
    for x in d_r_HB1_pin:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_pin[x]))]
        for y in range(0,  len(d_r_HB1_pin[x]) ):
            matrix_output[y][0]=d_r_HB1_pin[x][y][0]
            matrix_output[y][1]=d_r_HB1_pin[x][y][1]
            matrix_output[y][2]=d_r_HB1_pin[x][y][2]
        d_r_HB1_pin_localRecalculate[str(x)]=matrix_output

    d_r_SHR1_pin_localRecalculate={}
    for x in d_r_SHR1_pin:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_pin[x]))]
        for y in range(0,  len(d_r_SHR1_pin[x]) ):
            matrix_output[y][0]=d_r_SHR1_pin[x][y][0]
            matrix_output[y][1]=d_r_SHR1_pin[x][y][1]
        d_r_SHR1_pin_localRecalculate[str(x)]=matrix_output 


    d_r_HB2_pin_localRecalculate={}
    for x in d_r_HB2_pin:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_pin[x]))]
        for y in range(0,  len(d_r_HB2_pin[x]) ):
            matrix_output[y][0]=d_r_HB2_pin[x][y][0]
            matrix_output[y][1]=d_r_HB2_pin[x][y][1]
            matrix_output[y][2]=d_r_HB2_pin[x][y][2]
        d_r_HB2_pin_localRecalculate[str(x)]=matrix_output


    d_r_SHR2_pin_localRecalculate={}
    for x in d_r_SHR2_pin:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_pin[x]))]
        for y in range(0,  len(d_r_SHR2_pin[x]) ):
            matrix_output[y][0]=d_r_SHR2_pin[x][y][0]
            matrix_output[y][1]=d_r_SHR2_pin[x][y][1]
        d_r_SHR2_pin_localRecalculate[str(x)]=matrix_output


    d_r_HB1_fix_localRecalculate={}
    for x in d_r_HB1_fix:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_fix[x]))]
        for y in range(0,  len(d_r_HB1_fix[x]) ):
            matrix_output[y][0]=d_r_HB1_fix[x][y][0]
            matrix_output[y][1]=d_r_HB1_fix[x][y][1]
            matrix_output[y][2]=d_r_HB1_fix[x][y][2]
        d_r_HB1_fix_localRecalculate[str(x)]=matrix_output


    d_r_SHR1_fix_localRecalculate={}
    for x in d_r_SHR1_fix:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_fix[x]))]
        for y in range(0,  len(d_r_SHR1_fix[x]) ):
            matrix_output[y][0]=d_r_SHR1_fix[x][y][0]
            matrix_output[y][1]=d_r_SHR1_fix[x][y][1]
        d_r_SHR1_fix_localRecalculate[str(x)]=matrix_output


    d_r_HB2_fix_localRecalculate={}
    for x in d_r_HB2_fix:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_fix[x]))]
        for y in range(0,  len(d_r_HB2_fix[x]) ):
            matrix_output[y][0]=d_r_HB2_fix[x][y][0]
            matrix_output[y][1]=d_r_HB2_fix[x][y][1]
            matrix_output[y][2]=d_r_HB2_fix[x][y][2]
        d_r_HB2_fix_localRecalculate[str(x)]=matrix_output



    d_r_SHR2_fix_localRecalculate={}
    for x in d_r_SHR2_fix:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_fix[x]))]
        for y in range(0,  len(d_r_SHR2_fix[x]) ):
            matrix_output[y][0]=d_r_SHR2_fix[x][y][0]
            matrix_output[y][1]=d_r_SHR2_fix[x][y][1]
        d_r_SHR2_fix_localRecalculate[str(x)]=matrix_output



    d_r_d_result_HB_fix_localRecalculate={}
    d_r_d_result_HB_fix_l0={}
    for x in d_r_d_result_HB_fix:
        for y in d_r_d_result_HB_fix[x]:
            d_r_d_result_HB_fix_l0[str(y)]=d_r_d_result_HB_fix[x][y]
        d_r_d_result_HB_fix_localRecalculate[str(x)]=d_r_d_result_HB_fix_l0
        d_r_d_result_HB_fix_l0={}



    d_r_d_result_SHR_fix_localRecalculate={}
    d_r_d_result_SHR_fix_l0={}
    for x in d_r_d_result_SHR_fix:
        for y in d_r_d_result_SHR_fix[x]:
            d_r_d_result_SHR_fix_l0[str(y)]=d_r_d_result_SHR_fix[x][y]
        d_r_d_result_SHR_fix_localRecalculate[str(x)]=d_r_d_result_SHR_fix_l0
        d_r_d_result_SHR_fix_l0={}



    d_r_d_result_HB_pin_localRecalculate={}
    d_r_d_result_HB_pin_l0={}
    for x in d_r_d_result_HB_pin:
        for y in d_r_d_result_HB_pin[x]:
            d_r_d_result_HB_pin_l0[str(y)]=d_r_d_result_HB_pin[x][y]
        d_r_d_result_HB_pin_localRecalculate[str(x)]=d_r_d_result_HB_pin_l0
        d_r_d_result_HB_pin_l0={}

   

    d_r_d_result_SHR_pin_localRecalculate={}
    d_r_d_result_SHR_pin_l0={}
    for x in d_r_d_result_SHR_pin:
        for y in d_r_d_result_SHR_pin[x]:
            d_r_d_result_SHR_pin_l0[str(y)]=d_r_d_result_SHR_pin[x][y]
        d_r_d_result_SHR_pin_localRecalculate[str(x)]=d_r_d_result_SHR_pin_l0
        d_r_d_result_SHR_pin_l0={}

    d_r_HB1_hjs_localRecalculate={}
    for x in d_r_HB1_hjs:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_hjs[x]))]
        for y in range(0,  len(d_r_HB1_hjs[x]) ):
            matrix_output[y][0]=d_r_HB1_hjs[x][y][0]
            matrix_output[y][1]=d_r_HB1_hjs[x][y][1]
            matrix_output[y][2]=d_r_HB1_hjs[x][y][2]
        d_r_HB1_hjs_localRecalculate[str(x)]=matrix_output


    d_r_SHR1_hjs_localRecalculate={}
    for x in d_r_SHR1_hjs:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_hjs[x]))]
        for y in range(0,  len(d_r_SHR1_hjs[x]) ):
            matrix_output[y][0]=d_r_SHR1_hjs[x][y][0]
            matrix_output[y][1]=d_r_SHR1_hjs[x][y][1]
        d_r_SHR1_hjs_localRecalculate[str(x)]=matrix_output


    d_r_HB2_hjs_localRecalculate={}
    for x in d_r_HB2_hjs:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_hjs[x]))]
        for y in range(0,  len(d_r_HB2_hjs[x]) ):
            matrix_output[y][0]=d_r_HB2_hjs[x][y][0]
            matrix_output[y][1]=d_r_HB2_hjs[x][y][1]
            matrix_output[y][2]=d_r_HB2_hjs[x][y][2]
        d_r_HB2_hjs_localRecalculate[str(x)]=matrix_output




    d_r_SHR2_hjs_localRecalculate={}
    for x in d_r_SHR2_hjs:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_hjs[x]))]
        for y in range(0,  len(d_r_SHR2_hjs[x]) ):
            matrix_output[y][0]=d_r_SHR2_hjs[x][y][0]
            matrix_output[y][1]=d_r_SHR2_hjs[x][y][1]
        d_r_SHR2_hjs_localRecalculate[str(x)]=matrix_output

    

    d_r_d_result_HB_hjs_localRecalculate={}
    d_r_d_result_HB_hjs_l0={}
    for x in d_r_d_result_HB_hjs:
        for y in d_r_d_result_HB_hjs[x]:
            d_r_d_result_HB_hjs_l0[str(y)]=d_r_d_result_HB_hjs[x][y]
        d_r_d_result_HB_hjs_localRecalculate[str(x)]=d_r_d_result_HB_hjs_l0
        d_r_d_result_HB_hjs_l0={}


    d_r_d_result_SHR_hjs_localRecalculate={}
    d_r_d_result_SHR_hjs_l0={}
    for x in d_r_d_result_SHR_hjs:
        for y in d_r_d_result_SHR_hjs[x]:
            d_r_d_result_SHR_hjs_l0[str(y)]=d_r_d_result_SHR_hjs[x][y]
        d_r_d_result_SHR_hjs_localRecalculate[str(x)]=d_r_d_result_SHR_hjs_l0
    d_r_d_result_SHR_hjs_l0={}


    d_extra_check_hj_localRecalculate={}
    for x in d_extra_check_hj:
        matrix_output=[[None for c in range(4)] for r in range(1)]
        for y in range(0,  len(d_extra_check_hj[x]) ):
            matrix_output[y][0]=d_extra_check_hj[x][y][0]
            matrix_output[y][1]=d_extra_check_hj[x][y][1]
            matrix_output[y][2]=d_extra_check_hj[x][y][2]
            matrix_output[y][3]=d_extra_check_hj[x][y][3]
        d_extra_check_hj_localRecalculate[str(x)]=matrix_output



    d_workssheetLB4coma2masI_f={}
    count=0
    v_workssheetLB4coma2masI_f=[]
    for x in d_workssheetLB4coma2masI:
        for y in d_workssheetLB4coma2masI[x]:
            if int(y)==0:
                count=count+1
            elif ( (int(y)!=0) and count<2):

                v_workssheetLB4coma2masI_f.append(y)
        count=0
        d_workssheetLB4coma2masI_f[x]=v_workssheetLB4coma2masI_f
        v_workssheetLB4coma2masI_f=[]
    
    
    d_r_text_HB_fix_localRecalculate={}
    d_r_text_HB_fix_localRecalculate=d_r_text_HB_fix
    d_r_text_SHR_fix_localRecalculate={}
    d_r_text_SHR_fix_localRecalculate=d_r_text_SHR_fix
    d_fallaContinouos_localRecalculate={}
    d_fallaContinouos_localRecalculate=d_fallaContinouos
    d_r_text_HB_hjs_localRecalculate={}
    d_r_text_HB_hjs_localRecalculate=d_r_text_HB_hjs
    d_r_text_SHR_hjs_localRecalculate={}
    d_r_text_SHR_hjs_localRecalculate=d_r_text_SHR_hjs
    d_current_status_hb_localRecalculate={}
    d_current_status_hb_localRecalculate=d_current_status_hb
    d_current_status_shr_localRecalculate={}
    d_current_status_shr_localRecalculate=d_current_status_shr
    d_sf_localRecalculate={}
    d_sf_localRecalculate=d_sf
    d_Span_SVRating_localRecalculate={}
    d_Span_SVRating_localRecalculate=d_Span_SVRating
    d_estructure_Type_convert_localRecalculate={}
    d_estructure_Type_convert_localRecalculate=d_estructure_Type_convert
    d_current_status_hb_hjs_localRecalculate={}
    d_current_status_hb_hjs_localRecalculate=d_current_status_hb_hjs
    d_current_status_shr_hjs_localRecalculate={}
    d_current_status_shr_hjs_localRecalculate=d_current_status_shr_hjs
    d_ldds_f_localRecalculate={}
    d_ldds_f_localRecalculate=d_ldds_f
    d_ldds_position_f_localRecalculate={}
    d_ldds_position_f_localRecalculate=d_ldds_position_f
    valid_data_localRecalculate={}
    valid_data_localRecalculate=valid_data
    d_all_Span_HBRating_localRecalculate={}
    d_all_Span_HBRating_localRecalculate=d_all_Span_HBRating
    d_comments_localRecalculate={}
    d_comments_localRecalculate=d_comments



    return render(request, 'result_engineer_mofier_save.html',{'structure':structure, 'd_StructureKey':d_StructureKey, 'd_current_status':d_current_status, \
    'd_HB_or_SV':d_HB_or_SV, 'd_HB_or_SV_value':d_HB_or_SV_value,'notice_reference':notice_reference,'d_r_St_type':d_r_St_type, 'd_r_HB1':d_r_HB1, 'd_r_text_HB':d_r_text_HB,\
    'd_r_HB2':d_r_HB2, 'd_r_d_result_HB':d_r_d_result_HB,'d_r_SHR1':d_r_SHR1 ,'d_r_text_SHR':d_r_text_SHR, 'd_r_SHR2':d_r_SHR2, 'd_r_d_result_SHR':d_r_d_result_SHR,\
    'vehicle_assessed':vehicle_assessed, 'd_r_text_HB_pin':d_r_text_HB_pin,'d_r_text_SHR_pin': d_r_text_SHR_pin, 'd_r_HB1_pin':d_r_HB1_pin,'d_r_SHR1_pin':d_r_SHR1_pin,\
    'd_r_HB2_pin':d_r_HB2_pin, 'd_r_SHR2_pin':d_r_SHR2_pin, 'd_r_d_result_HB_pin': d_r_d_result_HB_pin,'d_r_d_result_SHR_pin': d_r_d_result_SHR_pin,\
    'd_r_text_HB_fix':d_r_text_HB_fix,'d_r_text_SHR_fix': d_r_text_SHR_fix, 'd_r_HB1_fix':d_r_HB1_fix,'d_r_SHR1_fix':d_r_SHR1_fix, 'd_r_HB2_fix':d_r_HB2_fix,\
    'd_r_SHR2_fix':d_r_SHR2_fix, 'd_r_d_result_HB_fix': d_r_d_result_HB_fix, 'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix, 'd_fallaContinouos':d_fallaContinouos,\
    'd_r_HB1_hjs':d_r_HB1_hjs, 'd_r_SHR1_hjs':d_r_SHR1_hjs, 'd_r_HB2_hjs':d_r_HB2_hjs, 'd_r_SHR2_hjs':d_r_SHR2_hjs, 'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs,\
    'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs, 'd_r_text_HB_hjs': d_r_text_HB_hjs, 'd_r_text_SHR_hjs':d_r_text_SHR_hjs,\
    'd_current_status_hb':d_current_status_hb, 'd_current_status_shr':d_current_status_shr, 'd_sf':d_sf, 'd_Span_SVRating':d_Span_SVRating,\
    'd_estructure_Type_convert':d_estructure_Type_convert, 'd_current_status_hb_hjs': d_current_status_hb_hjs, 'd_current_status_shr_hjs':d_current_status_shr_hjs,\
    'd_ldds_f':d_ldds_f, 'd_ldds_position_f':d_ldds_position_f, 'valid_data':valid_data, 'd_extra_check_hj':d_extra_check_hj, 'd_calc_type':d_calc_type,\
    'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI_f, 'd_all_Span_HBRating':d_all_Span_HBRating, 'd_comments':d_comments, 'd_all_Span_SVRating':d_all_Span_SVRating,\
    'd_ESRN':d_ESRN,

    })

def home(request):

    if not threads:
        p = Process(target=start,args=('False',))
        threads.append(p)
        p.start()
    
    return redirect(home3)

def home3(request):

    current_user = request.user
    try:
        if current_user.userprofile.role!=None:
            return redirect(summary)
        else:
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def login_view(request):

    username = request.POST['username']
    password = request.POST['inputPassword']
    user = authenticate(request, username=username, password=password)

    count=0
    index=0
    
    if user is not None:
        login(request, user)

        mydoc = collection_summary.find()
        for x in mydoc:
            count=count+1

        matrix_output=np.zeros((count,2))
        matrix_output=[[None for c in range(2)] for r in range(count)]

        mydoc = collection_summary.find()
        for x in mydoc:
            matrix_output[index][0]=x["id"]
            y=x["variables"]
            matrix_output[index][1]=y[0]["global result"]
            index=index+1
        return redirect(summary)
    else:
        return render(request, 'login_error.html')

def logout_view(request):

    logout(request)
    return redirect('home')

@login_required
def summary(request):

    count=0
    index=0
    mydoc = collection_summary.find()
    for x in mydoc:
        count=count+1

    matrix_output=np.zeros((count,2))
    matrix_output=[[None for c in range(3)] for r in range(count)]

    mydoc = collection_summary.find()
    for x in mydoc:
        matrix_output[index][0]=x["id"]
        y=x["variables"]
        matrix_output[index][1]=y[0]["global result"]
        matrix_output[index][2]=y[0]["d_comments"]
        index=index+1

    
    return render(request, 'summary_JSONS.html',{"matrix_output":matrix_output})

def globalvariables():

    global OpeninFlag
    global L
    global sf
    global EIStrt
    global Lleft
    global KEI
    global EI
    global FEM
    global Vehicle
    global Loadin
    global FEM1
    global FEM2
    global Rv
    global MaxMoveMomHB
    global MaxMoveMomHB11
    global MaxMoveMomHB22
    global MaxMoveShrHB
    global MaxMoveShrHB11
    global MaxMoveShrHB22
    global workssheetLB6coma2masI
    global MaxMoveMom
    global MaxMoveShr
    global workssheetLB3coma2masI

    sf=0.95
    L=np.zeros(31)
    EIStrt=np.zeros(31)
    Lleft=np.zeros(31)
    EI=np.zeros(31)
    KEI=np.zeros((31,3))
    FEM=np.zeros((31,3))
    Vehicle=np.zeros((51,3))
    Loadin=np.zeros((6,101))
    FEM1=np.zeros((31,3))
    FEM2=np.zeros((31,3))
    Rv=np.zeros(32)
    MaxMoveMomHB=np.zeros((100,7))
    MaxMoveMomHB11=np.zeros((100,7))
    MaxMoveMomHB22=np.zeros((100,7))     
    MaxMoveShrHB=np.zeros((100,6))
    MaxMoveShrHB11=np.zeros((100,6))
    MaxMoveShrHB22=np.zeros((100,6))
    workssheetLB6coma2masI=np.zeros(31)
    MaxMoveMom=np.zeros((100,4))
    MaxMoveShr=np.zeros((100,3))        
    OpeninFlag=0
    workssheetLB3coma2masI=np.zeros(31)

def Load_Axles_AIL():

    global Factored
    global NoOF
    global NoDF
    global NoFact
    global AXles
    global workssheetLB10masIcoma22
    global workssheetLB10masIcoma24
    global incTee
    global MaxMoveMomHB
    global MaxMoveShrHB

    AXles = 0
    VehicleL = 0
    AxleCount = 1
    incTee = 0
    
    workssheetLB11coma26 = AXles
    

    for I in range(1, 30+1):
        if (workssheetLB10masIcoma22[I]!=0):
            AXles=AXles+1

    workssheetLB11coma25=AXles
    
     
    for I in range(1, AXles+1):
        if(Factored==1):
            OF = 1.1
            AxTon = workssheetLB10masIcoma22[I]/10
            DF = 1.7 / AxTon ** 0.15
            if DF<1.05:                
                DF=1.05
        if (NoOF==1):
            OF = 1
            AxTon = workssheetLB10masIcoma22[I]/10
            DF = 1.7 / AxTon ** 0.15
            if DF<1.05:                
                DF=1.05
        if (NoDF==1):
            OF = 1.1
            DF = 1
        if (NoFact==1):
            OF = 1
            DF = 1

        VehicleL = VehicleL + workssheetLB10masIcoma24[I]
        Colmn = int((I - 1) / 10)
        
        Vehicle[I, 1] = workssheetLB10masIcoma22[I]
        Vehicle[I, 2] = VehicleL
        
        Vehicle[I, 1] = Vehicle[I, 1] * OF * DF #'OVERLOAD & DINAMIC FACTOR
     

    workssheetLB12coma26 = VehicleL

    Load_Vehicle_AIL_Fact()
    
    return MaxMoveMomHB,MaxMoveShrHB

def Load_Vehicle_AIL_Fact():

    global MaxMoveMomHB
    global MaxMoveShrHB
    global MaxMoveMom
    global MaxMoveShr
    global LorryTimes
    global LorryTimesF
    
    #Dim GammaF As Single, Iimpct As Integer, VehRef As Integer, VehNef(1 To 22) As Integer, VehNcount As Integer, VehStrign As String, Inn As Integer, InnNo As Integer, RowVehNcount As Integer
    
    
    for I in range (1, (2 * (NoSpn * 2 + 1)) + 1):
        for J in range(1, 3 + 1):
            MaxMoveMomHB[I, J] = 0

    for I in range(1, (2 * NoSpn) + 1):
        for J in range(1, 2 + 1):
            MaxMoveShrHB[I, J] = 0

    #If Worksheets("Line Beam").OptionButtons("NoOF").Value = xlOn Or Worksheets("Line Beam").OptionButtons("Factored").Value = xlOn Then
    if (NoOF==1 or Factored==1):
        LorryTimes = AXles   #' Sets number of times the progress lorry crosses the deck
        LorryTimesF = 1
        ImpctFctr = 1.2 / 1.1

        for Iimpct in range(1, AXles+1):  # 'Apply 1.2 Overload factor to each wheel in turn
            if (Iimpct == 1):
                Vehicle[1, 1] = Vehicle[1, 1] * ImpctFctr
            else:
                Vehicle[Iimpct, 1] = Vehicle[Iimpct, 1] * ImpctFctr
                Vehicle[Iimpct - 1, 1] = Vehicle[Iimpct - 1, 1] / ImpctFctr

            if global_hj==1:
                MovinVehicle_HJ()
            else:
                MovinVehicle()

            for I in range(1, (2 * NoSpn + 1) + 1, 2):
                if (MaxMoveMom[I, 1] > MaxMoveMomHB[I, 1]):
                    MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1]   #'Moment                 Max hog
                    MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2]   #'Position of Max moment
                    MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3]   #'First wheel position
                    #'MaxMoveMomHB(I, 4) = inrAxle              'Vehicle configuration****************************************************************************
                    if (ImpctFctr > 1.01):
                        MaxMoveMomHB[I, 5] = Iimpct   #'Record which axle has overload factor
                        MaxMoveMomHB[I, 6] = Vehicle[Iimpct, 1]  #'Nominal Axle Load
                if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                    MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1]   #'Shear                 LHE
                    MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2]   #'First wheel position
                    #'MaxMoveShrHB(I, 3) = inrAxle               'Vehicle configuration
                    if (ImpctFctr > 1.01):
                        MaxMoveShrHB[I, 4] = Iimpct   #'Record which axle has overload factor
                        MaxMoveShrHB[I, 5] = Vehicle[Iimpct, 1] # 'Nominal Axle Load

            for I in range(2, (2 * NoSpn) + 1, 2):
                if (MaxMoveMom[I, 1] < MaxMoveMomHB[I, 1]):
                    MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1] #  'Moment                 Max sag
                    MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2] #  'Position of Max moment
                    MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3] #  'First wheel position
                    #'MaxMoveMomHB(I, 4) = inrAxle             'Vehicle configuration
                    if (ImpctFctr > 1.01):
                        MaxMoveMomHB[I, 5] = Iimpct   #'Record which axle has overload factor
                        MaxMoveMomHB[I, 6] = Vehicle[Iimpct, 1] #  'Nominal Axle Load
                if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                    MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1] #  'Shear                 RHE
                    MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2] #  'First wheel position
                    #'MaxMoveShrHB(I, 3) = inrAxle                 'Vehicle configuration
                    if (ImpctFctr > 1.01):
                        MaxMoveShrHB[I, 4] = Iimpct   #'Record which axle has overload factor
                        MaxMoveShrHB[I, 5] = Vehicle[Iimpct, 1] # 'Nominal Axle Load          

        Vehicle[AXles, 1] = Vehicle[AXles, 1] / ImpctFctr     #'reset last axle

    else:
        LorryTimes = AXles   #' Sets number of times the progress lorry crosses the deck
        LorryTimesF = 1

        if global_hj==1:
            MovinVehicle_HJ()
        else:
            MovinVehicle()

        for I in range(1, (2 * NoSpn + 1) + 1, 2):
            if (MaxMoveMom[I, 1] > MaxMoveMomHB[I, 1]):
                MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1]   #'Moment                 Max hog
                MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2]   #'Position of Max moment
                MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3]   #'First wheel position
                    #'MaxMoveMomHB(I, 4) = inrAxle              'Vehicle configuration****************************************************************************
            if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1]   #'Shear                 LHE
                MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2]   #'First wheel position
                    #'MaxMoveShrHB(I, 3) = inrAxle               'Vehicle configuration
                    
        for I in range(2, (2 * NoSpn) + 1, 2):
            if (MaxMoveMom[I, 1] < MaxMoveMomHB[I, 1]):
                MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1] #  'Moment                 Max sag
                MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2] #  'Position of Max moment
                MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3] #  'First wheel position
                    #'MaxMoveMomHB(I, 4) = inrAxle             'Vehicle configuration
            if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1] #  'Shear                 RHE
                MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2] #  'First wheel position
                    #'MaxMoveShrHB(I, 3) = inrAxle                 'Vehicle configuration
                  

    GammaF = 1.1
    for I in range(1, (2 * NoSpn + 1) + 1):
        MaxMoveMomHB[I, 1] = GammaF * MaxMoveMomHB[I, 1]
        MaxMoveShrHB[I, 1] = GammaF * MaxMoveShrHB[I, 1]
    
def Load_Vehicle_SV_Fact():

    global MaxMoveMomHB
    global MaxMoveShrHB
    global SV_Rating
    global Reserve_Factor
    global AXles
    global LorryTimes
    global LorryTimesF
    global incTee
    global global_hj

       
    if (SV_Rating == "SV80" or SV_Rating == "sv80"):
        for I in range(1, 6 + 1):
            Vehicle[I, 1] = 130 * 1.1 * 1.7 / 13 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        AXles = 6
        
    if (SV_Rating == "SV100" or SV_Rating == "sv100"):#   ' SV100
        for I in range(1, 6 + 1):
            Vehicle[I, 1] = 165 * 1.1 * 1.7 / 16.5 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        AXles = 6
        
    if (SV_Rating == "SV150" or SV_Rating == "sv150"):
        for I in range(1, 10 + 1):
            Vehicle[I, 1] = 146 * 1.1 * 1.7 / (14.6 ** 0.15) #'Apply impact factor and 1.1 Overload factor to each wheel
        AXles = 10
        
    if (SV_Rating == "SVTrain" or SV_Rating == "svtrain"):#                               ' SV-Train
        Vehicle[1, 1] = 100 * 1.1 * 1.7 / 10 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        Vehicle[2, 1] = 180 * 1.1 * 1.7 / 18 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        Vehicle[3, 1] = 180 * 1.1 * 1.7 / 18 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        for I in range(4, 13 + 1):
            Vehicle[I, 1] = 146 * 1.1 * 1.7 / 14.6 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        AXles = 13
    
        
    if (SV_Rating == "SVTT" or SV_Rating == "svtt"):#                            ' SV-TT
        Vehicle[1, 1] = 150 * 1.1 * 1.7 / 15 ** 0.15 # 'Apply impact factor and 1.1 Overload factor to each wheel
        Vehicle[2, 1] = 200 * 1.1 * 1.7 / 20 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        Vehicle[3, 1] = 200 * 1.1 * 1.7 / 20 ** 0.15 #'Apply impact factor and 1.1 Overload factor to each wheel
        Vehicle[4, 1] = 250 * 1.1 * 1.05
        Vehicle[5, 1] = 250 * 1.1 * 1.05
        AXles = 5
     
    InnNo = 3
    incTee = 0.001
    RowVehNcount = 1
     
    LorryTimes = InnNo * AXles #' Sets number of times the progress lorry crosses the deck
    LorryTimesF = 1.15

    for I in range(1, 100):
        for J in range(1, 6 + 1):
            MaxMoveMomHB[I, J] = 0
            
        for J in range(1, 5 + 1):
            MaxMoveShrHB[I, J] = 0
        

    for Inn in range(1, InnNo + 1):
        if (InnNo != 1):
            if (Inn == 1):
                inrAxle = 1.2
            elif (Inn == 2):
                inrAxle = 5
            elif (Inn == 3):
                inrAxle = 9

        if (SV_Rating == "SV80" or SV_Rating == "sv80"):#  ' SV80
            Vehicle[1, 2] = 0
            Vehicle[2, 2] = 1.2
            Vehicle[3, 2] = 2.4
            Vehicle[4, 2] = 2.4 + inrAxle
            Vehicle[5, 2] = 3.6 + inrAxle
            Vehicle[6, 2] = 4.8 + inrAxle
            VehicleL = Vehicle[6, 2]

        if (SV_Rating == "SV100" or SV_Rating == "sv100"): #Then      ' SV100
            Vehicle[1, 2] = 0
            Vehicle[2, 2] = 1.2
            Vehicle[3, 2] = 2.4
            Vehicle[4, 2] = 2.4 + inrAxle
            Vehicle[5, 2] = 3.6 + inrAxle
            Vehicle[6, 2] = 4.8 + inrAxle
            VehicleL = Vehicle[6, 2]

             
        if (SV_Rating == "SV150" or SV_Rating == "sv150"): #Then' SV150
            Vehicle[1, 2] = 0
            Vehicle[2, 2] = 1.2
            Vehicle[3, 2] = 2.4
            Vehicle[4, 2] = 3.6
            Vehicle[5, 2] = 4.8
            Vehicle[6, 2] = 4.8 + inrAxle
            Vehicle[7, 2] = 6   + inrAxle
            Vehicle[8, 2] = 7.2 + inrAxle
            Vehicle[9, 2] = 8.4 + inrAxle
            Vehicle[10, 2] = 9.6 + inrAxle
            VehicleL = Vehicle[10, 2]
             
        if (SV_Rating == "SVTrain" or SV_Rating == "svtrain"):# Then                            ' SV-Train
            Vehicle[1, 2] = 0
            Vehicle[2, 2] = 4.4
            Vehicle[3, 2] = 6
            Vehicle[4, 2] = 10
            Vehicle[5, 2] = 11.2
            Vehicle[6, 2] = 12.4
            Vehicle[7, 2] = 13.6
            Vehicle[8, 2] = 14.8
            Vehicle[9, 2] = 14.8 + inrAxle
            Vehicle[10, 2] = 16 + inrAxle
            Vehicle[11, 2] = 17.2 + inrAxle
            Vehicle[12, 2] = 18.4 + inrAxle
            Vehicle[13, 2] = 19.6 + inrAxle
            VehicleL = Vehicle[13, 2]
                
        if (SV_Rating == "SVTT" or SV_Rating == "svtt"):#Then      ' SV-TT
            Vehicle[1, 2] = 0
            Vehicle[2, 2] = 4
            Vehicle[3, 2] = 5.5
            Vehicle[4, 2] = 13.5
            Vehicle[5, 2] = 15
            VehicleL = Vehicle[5, 2]
            
                
        ImpctFctr = 1.2 / 1.1
        for Iimpct in range(1, AXles + 1):
            if (Iimpct == 1):
                Vehicle[1, 1] = Vehicle[1, 1] * ImpctFctr
            else:
                Vehicle[Iimpct, 1] = Vehicle[Iimpct, 1] * ImpctFctr
                Vehicle[Iimpct - 1, 1] = Vehicle[Iimpct - 1, 1] / ImpctFctr

                
            if global_hj==1:
                MovinVehicle_HJ()
            else:
                MovinVehicle()
             
            for I in range(1, (2 * NoSpn + 1) + 1, 2):
                if (MaxMoveMom[I, 1] > MaxMoveMomHB[I, 1]):# Then
                    MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1]# 'Moment                 Max hog
                    MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2]#   'Position of Max moment
                    MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3]#   'First wheel position
                    MaxMoveMomHB[I, 4] = inrAxle         #     'Vehicle configuration
                    if (ImpctFctr > 1.01):# Then
                        MaxMoveMomHB[I, 5] = Iimpct #  'Record which axle has overload factor
                        MaxMoveMomHB[I, 6] = Vehicle[Iimpct, 1] #  'Nominal Axle Load
                if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):# Then
                    MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1] # 'Shear                 LHE
                    MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2] #  'First wheel position
                    MaxMoveShrHB[I, 3] = inrAxle          #     'Vehicle configuration
                    if (ImpctFctr > 1.01):# Then
                        MaxMoveShrHB[I, 4] = Iimpct   #'Record which axle has overload factor
                        MaxMoveShrHB[I, 5] = Vehicle[Iimpct, 1] # 'Nominal Axle Load
            
            for I in range(2, (2 * NoSpn) + 1, 2):
                if (MaxMoveMom[I, 1] < MaxMoveMomHB[I, 1]):
                    MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1] # 'Moment                 Max sag
                    MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2] #  'Position of Max moment
                    MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3] #  'First wheel position
                    MaxMoveMomHB[I, 4] = inrAxle           #  'Vehicle configuration
                    if (ImpctFctr > 1.01):
                        MaxMoveMomHB[I, 5] = Iimpct  # 'Record which axle has overload factor
                        MaxMoveMomHB[I, 6] = Vehicle[Iimpct, 1] # 'Nominal Axle Load
                     
                if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                    MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1] #  'Shear                 RHE
                    MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2] #   'First wheel position
                    MaxMoveShrHB[I, 3] = inrAxle   #              'Vehicle configuration
                    if (ImpctFctr > 1.01):
                        MaxMoveShrHB[I, 4] = Iimpct   #'Record which axle has overload factor
                        MaxMoveShrHB[I, 5] = Vehicle[Iimpct, 1] #  'Nominal Axle Load
                    

        Vehicle[AXles, 1] = Vehicle[AXles, 1] / ImpctFctr   #  'reset last axle
        RowVehNcount = RowVehNcount + 1

    
    #'Apply Reserve Factor and Gamma F
    GammaF = 1.1
    for I in range(1, (2 * NoSpn + 1) + 1):
        MaxMoveMomHB[I, 1] = GammaF * Reserve_Factor * MaxMoveMomHB[I, 1]
        MaxMoveShrHB[I, 1] = GammaF * Reserve_Factor * MaxMoveShrHB[I, 1]


    return MaxMoveMomHB,MaxMoveShrHB

def Load_Vehicle_HB_Fact():

    global MaxMoveMomHB
    global MaxMoveShrHB
    global AXles
    global LorryTimes
    global LorryTimesF
    global incTee
    global HB_rating
    global global_hj


    incTee = 0.001
    GammaF = 1.3

    #'Define only 45HB vehicle, then a proportionate factr will be added
    for I in range(1, 4 + 1):
        Vehicle[I, 1] = float(HB_rating) * 10
     
    AXles = 4

    for I in range(1, 100):
        for J in range(1, 3 + 1):
            MaxMoveMomHB[I, J] = 0
            MaxMoveShrHB[I, J] = 0            
        MaxMoveMomHB[I, 4] = 1

    Vehicle[1, 2] = 0
    Vehicle[2, 2] = 1.8
          
    LorryTimes = 5   #' Sets number of times the progress lorry crosses the deck
    LorryTimesF = 1
          
    for Inn in range(1, 5 + 1):
        inrAxle = 6 + 5 * (Inn - 1)
        Vehicle[3, 2] = 1.8 + inrAxle
        Vehicle[4, 2] = 3.6 + inrAxle
        VehicleL = Vehicle[4, 2]

        if global_hj==1:
            MovinVehicle_HJ()
        else:
            MovinVehicle()
        for I in range(1, (2 * NoSpn + 1) + 1, 2):
            if (MaxMoveMom[I, 1] > MaxMoveMomHB[I, 1]):
                MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1]   #'Moment                 Max hog
                MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2]   #'Position of Max moment
                MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3]   #'First wheel position
                MaxMoveMomHB[I, 4] = Inn                #'HB configuration
            
            if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1]   #'Shear                 LHE
                MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2]   #'First wheel position
                MaxMoveShrHB[I, 3] = Inn                #'HB configuration
           
        for I in range(2, (2 * NoSpn) + 1, 2):
            if (MaxMoveMom[I, 1] < MaxMoveMomHB[I, 1]):
                MaxMoveMomHB[I, 1] = MaxMoveMom[I, 1]  # 'Moment                 Max sag
                MaxMoveMomHB[I, 2] = MaxMoveMom[I, 2]  # 'Position of Max moment
                MaxMoveMomHB[I, 3] = MaxMoveMom[I, 3]  # 'First wheel position
                MaxMoveMomHB[I, 4] = Inn               # 'HB configuration

            if (abs(MaxMoveShr[I, 1]) > abs(MaxMoveShrHB[I, 1])):
                MaxMoveShrHB[I, 1] = MaxMoveShr[I, 1] #   'Shear                 RHE
                MaxMoveShrHB[I, 2] = MaxMoveShr[I, 2] #  'First wheel position
                MaxMoveShrHB[I, 3] = Inn              #  'HB configuration
    
    #'Factorised results: Apply GammaF
    for I in range(1, (2 * NoSpn + 1) + 1):
        MaxMoveMomHB[I, 1] = GammaF * MaxMoveMomHB[I, 1]
        MaxMoveShrHB[I, 1] = GammaF * MaxMoveShrHB[I, 1]

    return MaxMoveMomHB,MaxMoveShrHB
    
def PREPARE_CALCS():

    global NoSpn
    global TotSpn
    global L
    global EIStrt
    global Lleft
    global NoSpnTot
    global workssheetLB6coma2masI
    global workssheetLB5coma2masI
    
    SecCount = 0

    if (OpeninFlag == 0):
        dinput()
    else:
        NospnNew = 0
        for I in range(1, 30+1):
            if(workssheetLB4coma2masI[I]!=0):
                NospnNew = NospnNew + 1
        if (NospnNew != NoSpn):    # 'Check to see if spans have been added or subtracted
            dinput()

    #'Input data for span length and EI and determine No of Spans
    TotSpn = 0
    NoSpn = 0
    for I in range(1, 30+1):
        L[I] = workssheetLB4coma2masI[I]
        TotSpn = TotSpn + L[I]        
        EIStrt[I] = workssheetLB5coma2masI[I]
        if (L[I] != 0):
            NoSpn = I
            workssheetLB3coma2masI[I] = I  
    
    if (NoSpn > 1):
        for I in range(1, NoSpn + 1):
            EI[I] = EIStrt[I]

        #'Reduce EI/L's to relative EI/L's
        smallEI = EI[1]
        for I in range(2, NoSpn+1):
            if (EI[I] < smallEI):
                smallEI = EI[I]
        for I in range(1, NoSpn + 1):
            EI[I] = EI[I] / smallEI / L[I]
            workssheetLB6coma2masI[I] = EI[I]

        #'Module2
        distribution()  #'Calculate distribution factors

        #'Calculate accumulative distance from left hand end
        for I in range(1, 30+1):
            Lleft[I] = 0
        Lleft[1] = L[1]
        if (NoSpn > 1):
            for I in range(2, NoSpn + 1):
                Lleft[I] = Lleft[I - 1] + L[I]

        
    if (NoSpn == 0):
        for I in range (1, 30+1):
            workssheetLB3coma2masI[I] = I  
            workssheetLB4coma2masI[I] = 0  
            workssheetLB5coma2masI[I] = 0  
            workssheetLB6coma2masI[I] = 0  
        
        
    NoSpnTot=NoSpn   

    return 0

def ShearAtSection():

    #'NoSpnLd = Number of the Span that the Section is being considered
    #'Calculate shears due to reactions
    global Shr
    Shr = 0
    for N in range(1, NoSpnLd + 1):
        Shr = Shr - Rv[N]

    #'Calculate shears due to loads
    for N in range(1, NoLoads + 1):
        if (Loadin[1, N] > NoSpnLd):
            pass
        elif(Loadin[2, N] == 1):
             LaShr = Sectn - (Lleft[int(Loadin[1, N])] - L[int(Loadin[1, N])] + Loadin[4, N])
             if (LaShr > 0):
                 Shr = Shr + Loadin[3, N]
        
def MomAtSection():
    global NoSpnLd
    global Sectn
    global Mom
    global FEM
    global Rv
    global Lleft
    global NoLoads
    global Loadin
    global L

    #'Calculate moment due to distributed moments(FEM) and reactions
    if(NoSpnLd == 1):
        Mom = FEM[1, 1] + Rv[1] * Sectn
    else:
        Mom = FEM[1, 1] + Rv[1] * Sectn
        for N in range(2, int(NoSpnLd)+1):
            Mom = Mom + Rv[N] * (Sectn - Lleft[N - 1])

    #'Calculate moments due to loads
    
    for N in range(1, NoLoads + 1):
        if (Loadin[2, N]==1 and Loadin[1, N] <= NoSpnLd):
            LaMom = Sectn - (Lleft[int(Loadin[1, N])] - L[int(Loadin[1, N])] + Loadin[4, N])
            if (LaMom > 0):
                Mom = Mom - Loadin[3, N] * LaMom

def MomAtSection_Adjust():
    global Mom
    global MSL
    global MSR
    global dSL
    global dSR
    global Sectn

    if (NoSpnLd == 1):# Then 'When load is in Span 1
        Mom=MSL*Sectn/L[1]
   
    if (NoSpnLd == 2): # Then `When load is in Span 2
        d=Sectn-L[1]
        m1=(MSR-MSL)/L[2]
        Mom=MSL+m1*d 
    
    if NoSpnLd==3:#          'When load is in Span 3
        d=Lleft[3]-Sectn
        Mom=MSR*d/L[3]

def Reactn():
    global TotLoad
    global NoSpn
    global Rv
    for N in range(1,NoSpn + 1 + 1):
        Rv[N] = 0
    

    #'calclate reacions
    Rv[NoSpn + 1] = TotLoad
    for N in range(1,NoSpn + 1):
        Rv[N] = -FEM[1, 1] - FEM[N, 2]

        for J in range(1, NoLoads + 1):
            Spannon = Loadin[1, J]
            if (Loadin[2, J] == 1):
                b = L[int(Spannon)] - Loadin[4, J]
                if (round(Lleft[int(Spannon)] - b, 5) < Lleft[N] - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + b) * Loadin[3, J]

            elif (Loadin[2, J] == 2):
                Caseb = L[int(Spannon)]
                if (Round(Lleft[int(Spannon)] - b, 5) < Lleft[N]  - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + b / 2) * Loadin[3, J] * b
            elif (Loadin[2, J] == 3):
                b = L[int(Spannon)] - Loadin[4, J]
                if (Round(Lleft[int(Spannon)] - b, 5) < Lleft[N]  - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + b - Loadin[5, J] / 2) * Loadin[3, J] * Loadin[5, J]
            elif (Loadin[2, J] == 4):
                b = L[int(Spannon)]
                if (Round(Lleft[int(Spannon)] - b, 5) < Lleft[N]  - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + b / 3) * Loadin[3, J] * b / 2
            elif (Loadin[2, J] == 5):
                b = L(int(Spannon))
                if (Round(Lleft(int(Spannon)) - b, 5) < Lleft[N]  - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + 2 * b / 3) * Loadin[3, J] * b / 2
            elif (Loadin[2, J] == 6):
                b = L(int(Spannon))
                if (Round(Lleft(int(Spannon)) - b, 5) < Lleft[N]  - 0.0000001):
                    Rv[N] = Rv[N] + (Lleft[N] - Lleft[int(Spannon)] + b / 2) * Loadin[3, J] * b / 2

        if (N > 1):
            for Ntmes in range(1, N - 1 + 1):
                if (Ntmes == 1):
                    La = Lleft[N]
                else:
                    La = Lleft[N] - Lleft[Ntmes - 1]
                Rv[N] = Rv[N] - Rv[Ntmes] * La

        Rv[N] = Rv[N] / L[N]
        Rv[NoSpn + 1] = Rv[NoSpn + 1] - Rv[N]

def Distribute():
    global FEM1
    global FEM2
    global FEM

    Icount = 0
    Accurcy = 1

    while (Accurcy>0.000000001 and Icount<100):
        FEM1[1, 1] = -KEI[1, 1] * FEM[1, 1]##KEI y FEM es la calculada en distribution.py??
        FEM1[1, 2] = -KEI[1, 2] * (FEM[1, 2] + FEM[2, 1])
        FEM1[NoSpn, 1] = -KEI[NoSpn, 1] * (FEM[NoSpn - 1, 2] + FEM[NoSpn, 1])
        FEM1[NoSpn, 2] = -KEI[NoSpn, 2] * FEM[NoSpn, 2]

        if (NoSpn > 2):
            for N in range(2,NoSpn - 1 + 1):
                FEM1[N, 1] = -KEI[N, 1] * (FEM[N - 1, 2] + FEM[N, 1])
                FEM1[N, 2] = -KEI[N, 2] * (FEM[N, 2] + FEM[N + 1, 1])

            #'Carry over
        for N in range(1,NoSpn+1):
            if (KEI[N, 1] != 1): 
                FEM2[N, 1] = 0.5 * FEM1[N, 2]
            if (KEI[N, 2] != 1): 
                FEM2[N, 2] = 0.5 * FEM1[N, 1]


            #'Sum moments at supports
        for N in range(1,NoSpn+1):
            FEM[N, 1] = FEM[N, 1] + FEM1[N, 1] + FEM2[N, 1]
            FEM[N, 2] = FEM[N, 2] + FEM1[N, 2] + FEM2[N, 2]

            #'Check accuracy of carry over

        for N in range(1,NoSpn+1):
            if (abs(FEM2[N, 1]) > 0.000000001):
                Accurcy = abs(FEM2[N, 1])
            if (abs(FEM2[N, 2]) > 0.000000001):
                Accurcy = abs(FEM2[N, 2])

        Icount = Icount + 1

def OneSpan():
    global KEI
    #'Check end conditions for pinned or fixed
    if (OPTlhfixed == 1):
        KEI[1, 1] = 0
    if (OPTlhpin == 1):
        KEI[1, 1] = 1

    if (OPTrhfixed == 1):
        KEI[NoSpn, 2] = 0
    if (OPTrhpin == 1):
        KEI[1, 2] = 1

    if (KEI[1, 1] == 0 and KEI[1, 2])== 1:
        FEM[1, 1] = FEM[1, 1] - FEM[1, 2] / 2
        FEM[1, 2] = 0

    if (KEI[1, 1] == 1 and KEI[1, 2] == 0):
        FEM[1, 2] = FEM[1, 2] - FEM[1, 1] / 2
        FEM[1, 1] = 0

    if (KEI[1, 1] == 1 and KEI[1, 2] == 1):
        FEM[1, 1] = 0
        FEM[1, 2] = 0

def FixdEndMomPoint():

    global Intensity
    global a
    global b
    global spnNo
    global FEML
    global FEMR
    global L

    FEML = (-Intensity * a * (b ** 2)) / (L[int(spnNo)] ** 2)
    FEMR = (Intensity * b * (a ** 2)) / L[int(spnNo)] ** 2

def Analyse():

    global NoLoads
    global Intensity
    global a 
    global b
    global spnNo
    global FEML
    global FEMR
    global TotLoad
    global NoSpn
   
    #'Module3
    TotLoad = 0
    for I in range(1, NoSpn+1):
        FEM[I, 1] = 0
        FEM[I, 2] = 0

    if (NoSpn > 1) :
        distribution()
    
    for I in range(1,NoLoads+1):
        spnNo = Loadin[1, I]
        Intensity = Loadin[3, I]

        if Loadin[2, I]==1:
            a = Loadin[4, I]
            b = L[int(spnNo)] - a
            TotLoad = TotLoad + Intensity
            FixdEndMomPoint()        
            
            FEM[int(spnNo), 1] = FEM[int(spnNo), 1] + FEML
            FEM[int(spnNo), 2] = FEM[int(spnNo), 2] + FEMR
   
    if (NoSpn > 1):
        Distribute()
    else:
        OneSpan()

    Reactn()

def SortVehLoad():

    global Xsection
    global NoloadsMove
    global Lleft
    global Loadin
    global AXles
    global NoSpn
    
    for I in range(1, AXles+1):
            Loadin[1, I] = 1
            for KLOAD in range(1, NoSpn+1):   #'Fill Loadin() with spans that have loads
                if I == 1:
                    if (Xsection > Lleft[KLOAD]):
                        Loadin[1, I] = KLOAD + 1
                else:
                    if (Xsection - Vehicle[I, 2] > Lleft[KLOAD]):
                        Loadin[1, I] = KLOAD + 1
                    if (Xsection - Vehicle[I, 2] < 0):
                        Loadin[1, I] = 0
            Loadin[2, I] = 1  #'All axles are point loads
            
            Loadin[3, I] = Vehicle[I, 1]   #  'Axle loads in Loadin(3,I)
            

            if (Loadin[1, I] <= NoSpn):
                if (I == 1):
                    Loadin[4, I] = Xsection - (Lleft[int(Loadin[1, I])] - L[int(Loadin[1, I])])
                else:
                    if (Loadin[1, I] > 0):
                        Loadin[4, I] = Xsection - Vehicle[I, 2] - (Lleft[ int(Loadin[1, I])] - L[int(Loadin[1, I])])
            if (Loadin[1, I] > NoSpn):
                Loadin[1, I] = 0
            if (Loadin[4, I] < 0):
                Loadin[1, I] = 0
            if (Loadin[1, I] != 0):
                NoloadsMove = NoloadsMove + 1
                Loadin[1, NoloadsMove] = Loadin[1, I]
                Loadin[2, NoloadsMove] = Loadin[2, I]
                Loadin[3, NoloadsMove] = Loadin[3, I]
                Loadin[4, NoloadsMove] = Loadin[4, I]

def MovinVehicle():

    global Xsection
    global NoloadsMove
    global NoLoads
    global NoSpnLd
    global Sectn
    global Mom
    global Shr
    global MaxMoveMom
    global MaxMoveShr
    global TotSpn
    global NoSpn
    global AXles
    global LorryTimes
    global LorryTimesF
    global incTee
    global Loadin


    for I in range(1, (2 * (NoSpn * 2 + 1)) + 1):
        for J in range(1,3+1):
            MaxMoveMom[I, J] = 0
    for I in range(1, (2 * NoSpn) + 1):
         for J in range(1, 2+1):
            MaxMoveShr[I, J] = 0

    if (NoSpn>6):
        diezOcien=10
    else:
        diezOcien=100

    AvInc = TotSpn / NoSpn / diezOcien

    LdInc = int(Vehicle[AXles, 2] / AvInc) + 1

    Xsection = 0


    LorryInc0 = (NoSpn * diezOcien + LdInc) / 20 / LorryTimes
    LorryInc = LorryInc0 * LorryTimes * LorryTimesF
    if LorryTimes > 66 :
        LorryIncFF = 1.15
        LorryInc1 = 30 / LorryTimes
    else:
        LorryInc1 = 24 / LorryTimes
        LorryIncFF = 1
    
    Movecount = 1
    for Jv in range(1,int((NoSpn * diezOcien + LdInc))+1-1): #( -1 porque el excel hace algo raro)

        if (LorryInc < Jv):
            Movecount = Movecount + 1
            LorryInc = LorryInc0 * Movecount * LorryTimes * LorryTimesF * LorryIncFF
        Xsection = Xsection + AvInc #       ' position of axle W1
        NoloadsMove = 0     #'Number of loads to move
        
        SortVehLoad()
        NoLoads = NoloadsMove
        Analyse()

        #'Calculate Moments
        if (-FEM[1, 1] > MaxMoveMom[1, 1]):
            MaxMoveMom[1, 1] = -FEM[1, 1] #  'Moment                 Max hog R1
            MaxMoveMom[1, 2] = 0      # 'Position of Max moment
            MaxMoveMom[1, 3] = Xsection  #     'First wheel position
     
        for J in range (1,NoSpn+1):
            if FEM[J, 2] > MaxMoveMom[3 + 2 * (J - 1), 1]:
                MaxMoveMom[3 + 2 * (J - 1), 1] = FEM[J, 2] #   'Moment                 Max hog @ Supports
                MaxMoveMom[3 + 2 * (J - 1), 3] = Xsection  #   'First wheel position


        for J in range (1,NoSpn+1):

            MaxMoveMom[3 + 2 * (J - 1), 2] = Lleft[J]   #    'Position of Max moment
        
        for Jx in range (1,NoloadsMove+1):
            NoSpnLd = Loadin[1, Jx]    #       'NoSpnLD = Span number that moments are to be calculted for
            Sectn = Loadin[4, Jx] + Lleft[int(NoSpnLd)] - L[int(NoSpnLd)]
            MomAtSection() #'Module7
            if (  -Mom < MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 1] ) :  #'In-span sag moments
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 1] = -Mom
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 2] = Sectn
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 3] = Xsection

    #'Calculate Shears
    
    for Jv  in range(1,AXles+1):
        NoloadsMove = 0     #'Number of loads to move
        Xsection = Vehicle[Jv, 2] + incTee + 0.00001 #' position of axle W1 span 1
        SortVehLoad()
        NoLoads = NoloadsMove
        Analyse()
        for Jx in range(1 ,NoSpn+1):
            Sectn = Lleft[Jx] - L[Jx] + incTee   #' distance from LH end of deck
            NoSpnLd = Jx
            ShearAtSection()    # 'module 7
            if (abs(Shr) > abs(MaxMoveShr[2 * Jx - 1, 1])):
                MaxMoveShr[2 * Jx - 1, 1] = Shr
                MaxMoveShr[2 * Jx - 1, 2] = Xsection
        for Js  in range(1,NoSpn+1):
            NoloadsMove = 0     #'Number of loads to move
            Xsection = Vehicle[Jv, 2] + Lleft[Js] + incTee + 0.00001 #' position of axle W1 in other spans
            SortVehLoad()
            NoLoads = NoloadsMove
            Analyse()
                
            for Jx in range(1,NoSpn+1):
                Sectn = Lleft[Jx] - L[Jx] + incTee  # ' distance from LH end of deck
                NoSpnLd = Jx
                ShearAtSection()    # 'module 7
                if (abs(Shr) > abs(MaxMoveShr[2 * Jx - 1, 1])):
                    MaxMoveShr[2 * Jx - 1, 1] = Shr
                    MaxMoveShr[2 * Jx - 1, 2] = Xsection
        
    for Jv in range(1, AXles+1):
        NoloadsMove = 0     #'Number of loads to move
        Xsection = L[1] + Vehicle[Jv, 2] - incTee - 0.00001 #' position of axle W1 span 1
        SortVehLoad()
        NoLoads = NoloadsMove
        Analyse()
        for Jx in range(1, NoSpn+1):
            Sectn = Lleft[Jx] - incTee   # ' distance from LH end of deck
            NoSpnLd = Jx
            ShearAtSection()    # 'module 7
            if (abs(Shr) > abs(MaxMoveShr[2 * Jx, 1])):
                MaxMoveShr[2 * Jx, 1] = Shr
                MaxMoveShr[2 * Jx, 2] = Xsection

        for Js in range(1, NoSpn+1):
            NoloadsMove = 0   #  'Number of loads to move
            Xsection = Lleft[Js] + Vehicle[Jv, 2] - incTee - 0.00001 #' position of axle W1 in other spans
            SortVehLoad()
            NoLoads = NoloadsMove
            Analyse()
                
            for Jx in range(1,NoSpn+1):
                Sectn = Lleft[Jx] - incTee  #  ' distance from LH end of deck
                NoSpnLd = Jx
                ShearAtSection() #   'module 7
                if (abs(Shr) > abs(MaxMoveShr[2 * Jx, 1])):
                    MaxMoveShr[2 * Jx, 1] = Shr
                    MaxMoveShr[2 * Jx, 2] = Xsection

def MovinVehicle_HJ():

    global NoloadsMove
    global Lcant
    global Mom
    global MSL
    global MSR
    global dSL
    global dSR
    global spnNo
    global a
    global b
    global Intensity
    global MaxMoveMom
    global MaxMoveShr
    global Xsection
    global NoLoads
    global NoSpnLd
    global Sectn
    global Shr
    global TotSpn
    global NoSpn
    global AXles
    global LorryTimes
    global LorryTimesF
    global incTee
    global Loadin
    global Lleft

    MSL=0
    MSR=0


    #'It is assumed that Span is always going to be 1
    for I in range(1, (2 * (NoSpn * 2 + 1))+1):
        for J in range( 1, 3+1):
            MaxMoveMom[I, J] = 0

    for I in range(1, (2 * NoSpn) +1 ):
        for J in range(1, 2+1):
            MaxMoveShr[I, J] = 0

  

    AvInc = TotSpn / NoSpn / 100
    LdInc = int(Vehicle[AXles, 2] / AvInc) + 1
    Xsection = 0

    LorryInc0 = (NoSpn * 100 + LdInc) / 20 / LorryTimes
    LorryInc = LorryInc0 * LorryTimes * LorryTimesF
    if LorryTimes > 66 :
        LorryIncFF = 1.15
        LorryInc1 = 30 / LorryTimes
    else:
        LorryInc1 = 24 / LorryTimes
        LorryIncFF = 1
    Movecount = 1


    for Jv in range(1, (NoSpn * 100 + LdInc) + 1 ):
        if LorryInc < Jv :
            Movecount = Movecount + 1
            LorryInc = LorryInc0 * Movecount * LorryTimes * LorryTimesF * LorryIncFF
        Xsection = Xsection + AvInc   #     ' position of axle W1
        NoloadsMove = 0     #'Number of loads to move
        
        SortVehLoad()        
        NoLoads = NoloadsMove
        Analyse()


        #'Calculate Moments        
        #'Moments at MidSPAN           
        for Jx in range(1, NoloadsMove + 1):
            
            #'Mom at First Half-Joint
            Sectn = L[1]+Lcant
            NoSpnLd=2
            MomAtSection()
            MomHJL = Mom
            #'Mom at Second Half Joint
            Sectn = Lleft[2]-Lcant
            MomAtSection()
            MomHJR = Mom
                
            m=(MomHJR-MomHJL)/Ldds
            
            MSL=-(MomHJL+m*(-Lcant)) #' Mom at Support 2
            MSR=-(MomHJL+m*(Ldds+Lcant)) #' Mom at Support 3


            NoSpnLd = Loadin[1, Jx]  #         'NoSpnLD = Span number that moments are to be calculted for
            Sectn = Loadin[4, Jx] + Lleft[int(NoSpnLd)] - L[int(NoSpnLd)]

            MomAtSection()# 'CONTINUOUS MODEL
                
            Mom1=Mom
            MomAtSection_Adjust()# 'Adjustment Model
            Mom2=Mom
            Mom=Mom1+Mom2

        
         
            if -Mom < MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 1]:# Then  'In-span sag moments
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 1] = -Mom
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 2] = Sectn
                MaxMoveMom[2 + 2 * (int(NoSpnLd) - 1), 3] = Xsection
        
     
        if (-FEM[1, 1] > MaxMoveMom[1, 1]):# Then
            MaxMoveMom[1, 1] = -FEM[1, 1]#   'Moment                 Max hog R1
            MaxMoveMom[1, 2] = 0       #'Position of Max moment
            MaxMoveMom[1, 3] = Xsection #      'First wheel position
     
        for J in range(1, NoSpn +1):        
            if J==1:# Then 
                FEM[J,2]=FEM[J,2]-MSL
            if J==2:# Then 
                FEM[J,2]=FEM[J,2]-MSR
        
            if FEM[J, 2] > MaxMoveMom[3 + 2 * (J - 1), 1]:# Then
                MaxMoveMom[3 + 2 * (J - 1), 1] = FEM[J, 2]#   'Moment                 Max hog @ Supports
                MaxMoveMom[3 + 2 * (J - 1), 3] = Xsection  #   'First wheel position
        for J in range(1, NoSpn + 1):
            MaxMoveMom[3 + 2 * (J - 1), 2] = Lleft[J]#       'Position of Max moment
        

    
    #'Calculate Shears
    
    for Jv in range(1, AXles+1):
        NoloadsMove = 0    # 'Number of loads to move
        Xsection = Vehicle[Jv, 2] + incTee + 0.00001 #' position of axle W1 span 1
        SortVehLoad()
        NoLoads = NoloadsMove
        Analyse()
        for Jx in range(1, NoSpn + 1):
            #'Mom at First Half-Joint
            Sectn = L[1]+Lcant
            NoSpnLd=2
            MomAtSection()
            MomHJL = Mom
            #'Mom at Second Half Joint
            Sectn = Lleft[2]-Lcant
            MomAtSection()
            MomHJR = Mom
                
            m=(MomHJR-MomHJL)/Ldds
            
            MSL=-(MomHJL+m*(-Lcant)) #' Mom at Support 2
            MSR=-(MomHJL+m*(Ldds+Lcant)) #' Mom at Support 3
                    
            RS1=MSL/L[1]
            RS2=(MSR-RS1*Lleft[2])/L[2]
            RS4=MSR/L[3]
            RS3=(MSL-RS4*(L[2]+L[3]))/L[2]
                    
            #'Check equilibrium
            SumRS=RS1+RS2+RS3*RS4

                                    
            Sectn = Lleft[Jx] - L[Jx] + incTee  #' distance from LH end of deck
            NoSpnLd = Jx
                    
                    
            ShearAtSection()# 'module 7
                    
            Shr1=Shr
            if Jx==1:
                Shr2=-RS1                        
            if Jx==2:# Tehn
                Shr2=-(RS1+RS2)
            if Jx==3:# Then
                Shr2=-(RS1+RS2+RS3)
                    
                    
            if abs(Shr1+Shr2) > abs(MaxMoveShr[2 * Jx - 1, 1]):# Then
                MaxMoveShr[2 * Jx - 1, 1] = Shr1+Shr2
                MaxMoveShr[2 * Jx - 1, 2] = Xsection              



        for Js in range(1, NoSpn + 1):
            NoloadsMove = 0  #   'Number of loads to move
            Xsection = Vehicle[Jv, 2] + Lleft[Js] + incTee + 0.00001 #' position of axle W1 in other spans
            SortVehLoad()
            NoLoads = NoloadsMove
            Analyse()
                
            for Jx in range (1, NoSpn+1):
                
                #'Mom at First Half-Joint
                Sectn = L[1]+Lcant
                NoSpnLd=2
                MomAtSection()
                MomHJL = Mom
                #    'Mom at Second Half Joint
                Sectn = Lleft[2]-Lcant
                MomAtSection()
                MomHJR = Mom
                
                m=(MomHJR-MomHJL)/Ldds
            
                MSL=-(MomHJL+m*(-Lcant)) #' Mom at Support 2
                MSR=-(MomHJL+m*(Ldds+Lcant)) #' Mom at Support 3
                    
                RS1=MSL/L[1]
                RS2=(MSR-RS1*Lleft[2])/L[2]
                RS4=MSR/L[3]
                RS3=(MSL-RS4*(L[2]+L[3]))/L[2]
                    
                #'Check equilibrium
                SumRS=RS1+RS2+RS3*RS4
                
                Sectn = Lleft[Jx] - L[Jx] + incTee  # ' distance from LH end of deck
                NoSpnLd = Jx
                ShearAtSection()    #'module 7
                    
                    
                Shr1=Shr
                if Jx==1:
                    Shr2=-RS1                        
                if Jx==2:# Tehn
                    Shr2=-(RS1+RS2)
                if Jx==3:# Then
                    Shr2=-(RS1+RS2+RS3)
                    
                if abs(Shr1+Shr2) > abs(MaxMoveShr[2 * Jx - 1, 1]): #Then
                    MaxMoveShr[2 * Jx - 1, 1] = Shr1+Shr2
                    MaxMoveShr[2 * Jx - 1, 2] = Xsection
       
    
    for Jv in range(1, AXles +1):
        NoloadsMove = 0    # 'Number of loads to move
        Xsection = L[1] + Vehicle[Jv, 2] - incTee - 0.00001 #' position of axle W1 span 1
        SortVehLoad()
        NoLoads = NoloadsMove
        Analyse()
        for Jx in range(1, NoSpn + 1):
                    
            #'Mom at First Half-Joint
            Sectn = L[1]+Lcant
            NoSpnLd=2
            MomAtSection()
            MomHJL = Mom
            #'Mom at Second Half Joint
            Sectn = Lleft[2]-Lcant
            MomAtSection()
            MomHJR = Mom
                
            m=(MomHJR-MomHJL)/Ldds
            
            MSL=-(MomHJL+m*(-Lcant)) #' Mom at Support 2
            MSR=-(MomHJL+m*(Ldds+Lcant)) #' Mom at Support 3
                    
            RS1=MSL/L[1]
            RS2=(MSR-RS1*Lleft[2])/L[2]
            RS4=MSR/L[3]
            RS3=(MSL-RS4*(L[2]+L[3]))/L[2]
                    
            #'Check equilibrium
            SumRS=RS1+RS2+RS3*RS4
                    
            Sectn = Lleft[Jx] - incTee #   ' distance from LH end of deck
            NoSpnLd = Jx
            ShearAtSection()  #   'module 7
                    
            Shr1=Shr
            if Jx==1:
                Shr2=-RS1                        
            if Jx==2:# Tehn
                Shr2=-(RS1+RS2)
            if Jx==3:# Then
                Shr2=-(RS1+RS2+RS3)
                    
                    
            if abs(Shr1+Shr2) > abs(MaxMoveShr[2 * Jx, 1]):# Then
                MaxMoveShr[2 * Jx, 1] = Shr1+Shr2
                MaxMoveShr[2 * Jx, 2] = Xsection

        for Js in range(1, NoSpn + 1):
            NoloadsMove = 0   #  'Number of loads to move
            Xsection = Lleft[Js] + Vehicle[Jv, 2] - incTee - 0.00001 #' position of axle W1 in other spans
            SortVehLoad()
            NoLoads = NoloadsMove
            Analyse()
                
            for Jx in range(1, NoSpn + 1):
                
                #'Mom at First Half-Joint
                Sectn = L[1]+Lcant
                NoSpnLd=2
                MomAtSection()
                MomHJL = Mom
                #'Mom at Second Half Joint
                Sectn = Lleft[2]-Lcant
                MomAtSection()
                MomHJR = Mom
                
                m=(MomHJR-MomHJL)/Ldds
            
                MSL=-(MomHJL+m*(-Lcant)) #' Mom at Support 2
                MSR=-(MomHJL+m*(Ldds+Lcant)) #' Mom at Support 3
                    
                RS1=MSL/L[1]
                RS2=(MSR-RS1*Lleft[2])/L[2]
                RS4=MSR/L[3]
                RS3=(MSL-RS4*(L[2]+L[3]))/L[2]
                    
                #'Check equilibrium
                SumRS=RS1+RS2+RS3*RS4
                    
                Sectn = Lleft[Jx] - incTee #   ' distance from LH end of deck
                NoSpnLd = Jx
                ShearAtSection() #    'module 7
                
                Shr1=Shr
                if Jx==1:
                    Shr2=-RS1                        
                if Jx==2:# Tehn
                    Shr2=-(RS1+RS2)
                if Jx==3:# Then
                    Shr2=-(RS1+RS2+RS3)
                    
                if abs(Shr1+Shr2) > abs(MaxMoveShr[2 * Jx, 1]):# Then
                    MaxMoveShr[2 * Jx, 1] = Shr1+Shr2
                    MaxMoveShr[2 * Jx, 2] = Xsection

def distribution():

    global OPTlhfixed
    global OPTlhpin
    global OPTrhfixed
    global OPTrhpin
        
    for I in range(1,31):
        for J in range(1,3):
            KEI[I, J] = 0
            FEM[I, J] = 0

    #'Refix EI reduced values
    for I in range(1, NoSpn+1):
        EI[I] = workssheetLB6coma2masI[I] #Worksheets("Line Beam").Cells(6, 2 + I).Value    

    #'Calculate distribution factors
    #'Check end conditions for pinned or fixed
    if (OPTlhfixed==1): #Worksheets("Line Beam").OptionButtons("OPTlhfixed").Value == xlOn:###si el botón fixed está activo
        KEI[1, 1] = 0
    if (OPTlhpin==1): #Worksheets("Line Beam").OptionButtons("OPTlhpin").Value == xlOn:## si el botón pinned está activo
        KEI[1, 1] = 1
        EI[1] = 0.75 * EI[1]
    
    if (OPTrhfixed==1): #Worksheets("Line Beam").OptionButtons("OPTrhfixed").Value == xlOn: ###si el botón fixed está activo
        KEI[NoSpn, 2] = 0
    if (OPTrhpin==1): #Worksheets("Line Beam").OptionButtons("OPTrhpin").Value == xlOn:## si el botón pinned está activo
        KEI[NoSpn, 2] = 1
        EI[NoSpn] = 0.75 * EI[NoSpn]

    ##############rellenar la matriz KEI##########
    KEI[1, 2] = EI[1] / (EI[1] + EI[2])
    KEI[NoSpn, 1] = EI[NoSpn] / (EI[NoSpn] + EI[NoSpn - 1])
    if (NoSpn > 2):
        for I in range(2,NoSpn):
            KEI[I, 1] = EI[I] / (EI[I - 1] + EI[I])
            KEI[I, 2] = EI[I] / (EI[I] + EI[I + 1])

def dinput():

    global OpeninFlag
    global NoSpn
    global workssheetLB6coma2masI
    global workssheetLB5coma2masI
    global Lleft
    global L
    global EIStrt

    OpeninFlag=OpeninFlag+1
    TotSpn = 0
    NoSpn = 0

    for I in range(1, 30 +1):
        L[I]= workssheetLB4coma2masI[I] # Worksheets("Line Beam").Cells(4, 2 + I).Value
        TotSpn = TotSpn + L[I]
        EIStrt[I]=workssheetLB5coma2masI[I]  # Worksheets("Line Beam").Cells(5, 2 + I).Value
        if L[I] != 0:
            NoSpn = I
            workssheetLB3coma2masI[I] = I #Worksheets("Line Beam").Cells(3, 2 + I) = I    

    if (NoSpn > 1):
        for I in range(1, NoSpn+1):
            EI[I] = EIStrt[I]       
        #'Reduce EI/L's to relative EI/L's
        smallEI = EI[1]
        for I in range(2,NoSpn+1):
            if EI[I] < smallEI:
                smallEI = EI[I]#Busca el valor más pequeño de EIStrt(I) = Worksheets("Line Beam").Cells(5, 2 + I).Value
        for I in range(1,NoSpn+1):
            EI[I] = EI[I] / smallEI / L[I] #cambia el valor de EI(I)=EIStrt(I) = Worksheets("Line Beam").Cells(5, 2 + I).Value  con la fórmula
            #Worksheets("Line Beam").Cells(6, 2 + I).NumberFormat = "0.000"
            workssheetLB6coma2masI[I] = EI[I] #Worksheets("Line Beam").Cells(6, 2 + I).Value = EI(I)##Guarda los valores de EI(I) en Worksheets("Line Beam").Cells(6, 2 + I).Value 
        #'Module2
        distribution()  #'Calculate distribution factors
    
       # 'Calculate accumulative distance from left hand end
    for I in range(1, NoSpn+1):
        Lleft[I] = 0 ##iniciliza la variable Lleft[10]=0
        
    Lleft[1] = L[1] #L(1) = Worksheets("Line Beam").Cells(4, 3).Value
    if (NoSpn > 1):
        for I in range(1,NoSpn+1):
            Lleft[I] = Lleft[I - 1] + L[I]###Lleft(2)=L[1]+L[2] || Lleft(3)=L[1]+L[2]+L[3] || Lleft(4)=L[1]+L[2]+L[3]+L[4] ....

def CALC_SS_HB_AIL():

    global NoSpn
    global sf
    global workssheetLB4coma2masI
    global workssheetLB5coma2masI
    global L
    global EIStrt
    global Lleft
    global EI
    global KEI
    global FEM
    global Vehicle
    global Loadin
    global FEM1
    global FEM2
    global Rv
    global MaxMoveMomHB      
    global MaxMoveShrHB
    global workssheetLB6coma2masI
    global MaxMoveMom
    global MaxMoveShr
    global OpeninFlag
    global HB_or_SV

    NoSpnTotf=[]

    v_HB1=[]
    v_SHR1=[]
    v_HB2=[]
    v_SHR2=[]
    v_d_result_HB=[] 
    v_d_result_SHR=[]


    Lcopy=np.zeros(31)
    MaxMoveMomHB11=np.zeros((100,7))
    MaxMoveMomHB22=np.zeros((100,7))
    MaxMoveShrHB11=np.zeros((100,6))
    MaxMoveShrHB22=np.zeros((100,6))
    

    NoSpnTot=NoSpn

    for I in range(0,31):
        Lcopy[I]=L[I]

    for J in range(1, NoSpnTot+1):   
        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(21)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0

        workssheetLB4coma2masI=[0,Lcopy[J],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        workssheetLB5coma2masI=[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        PREPARE_CALCS()


        if(HB_or_SV=="HB"):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

        for I in range(1, 100):
            for JJ in range(1, 7):
                MaxMoveMomHB11[I, JJ] = MaxMoveMomHB1[I, JJ]

        for I in range(1, 100):
            for JJ in range(1, 6):
                MaxMoveShrHB11[I, JJ] = MaxMoveShrHB1[I, JJ]


        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(21)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0
        
        workssheetLB3coma2masI=np.zeros(31)

        PREPARE_CALCS()
        MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()

        for I in range(1, 100):
            for JJ in range(1, 7):
                MaxMoveMomHB22[I, JJ] = MaxMoveMomHB2[I, JJ]

        for I in range(1, 100):
            for JJ in range(1, 6):
                MaxMoveShrHB22[I, JJ] = MaxMoveShrHB2[I, JJ]


        HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR=comparative(MaxMoveMomHB11,MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)


        v_HB1.append(HB1)
        v_SHR1.append(SHR1)
        v_HB2.append(HB2)
        v_SHR2.append(SHR2)
        v_d_result_HB.append(d_result_HB)
        v_d_result_SHR.append(d_result_SHR)

    return v_HB1, v_SHR1, v_HB2, v_SHR2, v_d_result_HB, v_d_result_SHR

def comparative(MaxMoveMomHB1, MaxMoveMomHB2,MaxMoveShrHB1,MaxMoveShrHB2):

    global sf  

    MaxMoveMomHB1_f=np.zeros(( (2*NoSpn)+1 , 3))
    MaxMoveShrHB1_f=np.zeros(( (2*NoSpn)   , 2))
    MaxMoveMomHB2_f=np.zeros(( (2*NoSpn)+1 , 3))
    MaxMoveShrHB2_f=np.zeros(( (2*NoSpn)   , 2))


    v_MaxMoveMomHB1=[]
    v_MaxMoveShrHB1=[]
    v_MaxMoveMomHB2=[]
    v_MaxMoveShrHB2=[]


    for x in range(1,(2*NoSpn)+1+1):
        MaxMoveMomHB1_f[x-1][0]=round(MaxMoveMomHB1[x][1],1)
        MaxMoveMomHB2_f[x-1][0]=round(MaxMoveMomHB2[x][1],1)
        MaxMoveMomHB1_f[x-1][1]=round(MaxMoveMomHB1[x][2],1)
        MaxMoveMomHB2_f[x-1][1]=round(MaxMoveMomHB2[x][2],1)
        MaxMoveMomHB1_f[x-1][2]=round(MaxMoveMomHB1[x][3],1)
        MaxMoveMomHB2_f[x-1][2]=round(MaxMoveMomHB2[x][3],1)

    for x in range(1,(2*NoSpn)+1):
        MaxMoveShrHB1_f[x-1][0]=round(MaxMoveShrHB1[x][1],1)
        MaxMoveShrHB2_f[x-1][0]=round(MaxMoveShrHB2[x][1],1)
        MaxMoveShrHB1_f[x-1][1]=round(MaxMoveShrHB1[x][2],1)
        MaxMoveShrHB2_f[x-1][1]=round(MaxMoveShrHB2[x][2],1)


    d_result_MaxMoveMomHB={}
    d_result_MaxMoveShrHB={}  

    for I in range(0, (2 * NoSpn + 1) ):
        if(abs(sf*MaxMoveMomHB1_f[I, 0]) < abs(MaxMoveMomHB2_f[I, 0])  and  abs(MaxMoveMomHB1_f[I, 0]) >= abs(MaxMoveMomHB2_f[I, 0])  ):
            d_result_MaxMoveMomHB[I]='CAUTION'
        elif (abs(sf*MaxMoveMomHB1_f[I, 0]) >= abs(MaxMoveMomHB2_f[I, 0])):
            d_result_MaxMoveMomHB[I]='OK'
        else:
            d_result_MaxMoveMomHB[I]='FAIL'

    for I in range(0, (2 * NoSpn )):
        if(abs(sf*MaxMoveShrHB1_f[I, 0]) < abs(MaxMoveShrHB2_f[I, 0])   and  abs(MaxMoveShrHB1_f[I, 0]) >= abs(MaxMoveShrHB2_f[I, 0]) ):
            d_result_MaxMoveShrHB[I]='CAUTION'

        elif( abs(sf*MaxMoveShrHB1_f[I, 0]) >= abs(MaxMoveShrHB2_f[I, 0]) ):
            d_result_MaxMoveShrHB[I]='OK'

        else:
            d_result_MaxMoveShrHB[I]='FAIL'
    
    return MaxMoveMomHB1_f,MaxMoveShrHB1_f,MaxMoveMomHB2_f,MaxMoveShrHB2_f,d_result_MaxMoveMomHB,d_result_MaxMoveShrHB

def HalfJointedSpan(HB_or_SV_hj):

    global Ldds_position
    global Ldds 
    global NoSpn
    global sf
    global workssheetLB4coma2masI
    global workssheetLB5coma2masI
    global L
    global EIStrt
    global Lleft
    global EI
    global KEI
    global FEM
    global Vehicle
    global Loadin
    global FEM1
    global FEM2
    global Rv
    global MaxMoveMomHB      
    global MaxMoveShrHB
    global workssheetLB6coma2masI
    global MaxMoveMom
    global MaxMoveShr
    global OpeninFlag
    global valid_data
    global global_hj
    global Lcant


    EIStrt=np.zeros(31)
    Lleft=np.zeros(31)
    EI=np.zeros(31)
    KEI=np.zeros((31,3))
    FEM=np.zeros((31,3))
    Vehicle=np.zeros((51,3))
    Loadin=np.zeros((6,101))
    FEM1=np.zeros((31,3))
    FEM2=np.zeros((31,3))
    Rv=np.zeros(32)
    MaxMoveMomHB=np.zeros((100,7))        
    MaxMoveShrHB=np.zeros((100,6))
    workssheetLB6coma2masI=np.zeros(31)
    MaxMoveMom=np.zeros((100,4))
    MaxMoveShr=np.zeros((100,3))
    OpeninFlag=0
    MaxMoveMomHB11=np.zeros((100,7))
    MaxMoveMomHB22=np.zeros((100,7))        
    MaxMoveShrHB11=np.zeros((100,6))
    MaxMoveShrHB22=np.zeros((100,6))

    workssheetLB4coma2masI_l=workssheetLB4coma2masI

    #'Comparar que Ldds_position <= NoSpn
    #'Comaparar que Ldds <= L(Ldds_position)
    if(Ldds_position<=NoSpn) and (Ldds<=L[Ldds_position]):
        valid_data=1
    else:
        valid_data=0


    if (valid_data==1):
        Lcant = (L[Ldds_position] - Ldds) / 2

        global_hj=1

        for x in range(0,31):
            if x==1:
                workssheetLB4coma2masI[x]=workssheetLB4coma2masI_l[Ldds_position-1]
                workssheetLB5coma2masI[x]=1
            elif x==2:
                workssheetLB4coma2masI[x]=workssheetLB4coma2masI_l[Ldds_position]
                workssheetLB5coma2masI[x]=1
            elif x==3:
                workssheetLB4coma2masI[x]=workssheetLB4coma2masI_l[Ldds_position+1]
                workssheetLB5coma2masI[x]=1
            else:
                workssheetLB4coma2masI[x]=0
                workssheetLB5coma2masI[x]=0

        PREPARE_CALCS()


        if(HB_or_SV_hj=='HB'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
        elif(HB_or_SV_hj=='SV'):
            MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()


        for I in range(1, 100):
            for JJ in range(1, 7):
                MaxMoveMomHB11[I, JJ] = MaxMoveMomHB1[I, JJ]

        for I in range(1, 100):
            for JJ in range(1, 6):
                MaxMoveShrHB11[I, JJ] = MaxMoveShrHB1[I, JJ]

        L=np.zeros(31)
        EIStrt=np.zeros(31)
        Lleft=np.zeros(31)
        EI=np.zeros(31)
        KEI=np.zeros((31,3))
        FEM=np.zeros((31,3))
        Vehicle=np.zeros((51,3))
        Loadin=np.zeros((6,101))
        FEM1=np.zeros((31,3))
        FEM2=np.zeros((31,3))
        Rv=np.zeros(32)
        MaxMoveMomHB=np.zeros((100,7))        
        MaxMoveShrHB=np.zeros((100,6))
        workssheetLB6coma2masI=np.zeros(31)
        MaxMoveMom=np.zeros((100,4))
        MaxMoveShr=np.zeros((100,3))
        OpeninFlag=0

        workssheetLB3coma2masI=np.zeros(31)

        PREPARE_CALCS()
        MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()


        for I in range(1, 100):
            for JJ in range(1, 7):
                MaxMoveMomHB22[I, JJ] = MaxMoveMomHB2[I, JJ]

        for I in range(1, 100):
            for JJ in range(1, 6):
                MaxMoveShrHB22[I, JJ] = MaxMoveShrHB2[I, JJ]

        #'CALL HERE COMPARATIVE COMMAND
        HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR=comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)


        #'Tehn Additional Cantilever Calcs
        Vcant1 = max(abs(MaxMoveShrHB11[1, 1]), abs(MaxMoveShrHB11[2, 1]))
        Mcant1 = Vcant1 * Lcant

        Vcant2 = max(abs(MaxMoveShrHB22[1, 1]), abs(MaxMoveShrHB22[2, 1]))       
        Mcant2 = Vcant2 * Lcant


        #'Now compare both Vcant and Mcant
        if (abs(sf * Vcant1) >= abs(Vcant2)) and (abs(sf * Mcant1) >= abs(Mcant2)):
            Result_HJ = "OK"
        else:
            Result_HJ = "FAIL"

        return HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR
    else:
        return 0, 0, 0, 0, 0, 0


def extract_element_from_json(obj, path):

    def extract(obj, path, ind, arr):
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                
                if key in obj.keys():                    
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

def get_Json_Data(jsontochoose):

    global workssheetLB10masIcoma22
    global workssheetLB10masIcoma24
    global workssheetLB4coma2masI
    global workssheetLB5coma2masI
    global d_workssheetLB4coma2masI
    global d_workssheetLB5coma2masI
    global d_HB_or_SV
    global d_HB_or_SV_value
    global total_structures
    global notice_reference
    global StructureKey
    global StructureType
    global vehicle_assessed
    global d_Span_SVRating
    global timestamp
    global ESRN
    global d_all_Span_HBRating
    global SignedWeightConstraints_variable
    global Span_SequencePosition_Duplicated
    global Span_SequencePosition_missing
    global d_length_missing
    global d_rating_missing
    global data
    global d_ESRN
    global d_Span_SVReserve
    global d_Span_SVRating_valid


    folder_url='/app/'+jsontochoose

    with open(folder_url) as json_file:
        data = json.load(json_file)        
        
        notice_reference=extract_element_from_json(data, ["properties", "movement_id"])
        StructureKey=extract_element_from_json(data, ["properties", "EsdalStructure", "StructureKey"])
        StructureType=extract_element_from_json(data, ["properties", "EsdalStructure", "StructureType"])
        timestamp=extract_element_from_json(data, ["properties", "timestamp"])
        ESRN=extract_element_from_json(data, ["properties", "EsdalStructure", "ESRN"])
        d_ESRN={}
        for i in range(0, len(ESRN)):
            d_ESRN[str(i+1)]=ESRN[i]
        vehicle_assessed=extract_element_from_json(data, ["properties", "Vehicles", "ConfigurationSummaryListPosition", "ConfigurationSummary"])

        #print("-------------------------------VEHICLE-----------------------------")
        d1=0
        workssheetLB10masIcoma22=np.zeros(31)
        workssheetLB10masIcoma24=np.zeros(31)
        workssheetLB4coma2masI=np.zeros(31)
        

        ###########Vector W y S##################
        number_Axles_longitude=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "Longitude"])

        number_Axles=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","NumberOfAxles"])

        number_Axles_Value_count=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","AxleWeightListPosition","AxleWeight","AxleCount"])

        number_Axles_Value_value=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","AxleWeightListPosition","AxleWeight","value"])


        for x in range(0,len(number_Axles_Value_value)):
            number_Axles_Value_value[x]=number_Axles_Value_value[x]/100

  

        ##########poner en orden correcto según longitud#####
        maxlongitud=np.amax(number_Axles_longitude)
        d = {}
        d1= {}
        d2= {}

        for i in range(1, maxlongitud+1):
            for x in range(0, len(number_Axles_longitude)):
                if (i==int(number_Axles_longitude[x])):
                    d[i]=number_Axles[x]
        ############
        startcount=0
        a=0
        b=0
        fin=0
        vector2=[]
        vector3=[]
        for i in range(0, len(number_Axles)):
            a=int(number_Axles[i])
            fin=0
            for x in range(startcount, len(number_Axles_Value_count)):
                if fin==0:
                    b=b+int(number_Axles_Value_count[x])
                    #d1[a].append(number_Axles_Value_count[x])
                    vector2.append(copy.deepcopy(number_Axles_Value_count[x])) 
                    vector3.append(copy.deepcopy(number_Axles_Value_value[x]))
                    if (b==a):
                        d1[str(a)+str("_")+str(i)]=vector2
                        d2[str(a)+str("_")+str(i)]=vector3
                        vector2=[]
                        vector3=[]
                        startcount=x+1
                        b=0
                        fin=1
                


        ####modificar los vectores anteriores pero ahora ordenados según longitud####
        number_Axles=[]
        number_Axles_Value_count=[]
        number_Axles_Value_value=[]
        for i in range(1, maxlongitud+1):
            number_Axles.append(d[i])
            for keyd1 in d1:
                keyd1split=keyd1.split("_")
                if(d[i]==int(keyd1split[0])):
                    for xx in d1[keyd1]:
                        number_Axles_Value_count.append(xx)
            for keyd2 in d2:
                keyd2split=keyd2.split("_")
                if(d[i]==int(keyd2split[0])):
                    for yy in d2[keyd2]:
                        number_Axles_Value_value.append(yy)



        ####Calculate final vectors####

        total_NA_values=0
        i=0
        total_Count=0
        contadorinicio=0
        fin_v1=1

        for N_A in number_Axles:
            v1=int(N_A)
            fin_v1=0
            for N_A_Count in range (contadorinicio, len(number_Axles_Value_count)):
                if fin_v1==0:
                    v2=int(number_Axles_Value_count[N_A_Count])  
                    v3=int(number_Axles_Value_value[N_A_Count]) 
                    for x in range(0,v2):
                        i=i+1
                        workssheetLB10masIcoma22[i]=v3

                    total_Count=total_Count+v2

                    if (total_Count>=v1):                       
                        contadorinicio=N_A_Count+1
                        total_Count=0
                        fin_v1=1
                        break               

        ###########################################DISTANCIA DE EJES#####################################################
        number_Axles2=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","NumberOfAxles"])

        number_Axles_Spacing_Count=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","AxleSpacingListPosition","AxleSpacing","AxleCount"])

        number_Axles_Spacing_Value=extract_element_from_json(data, ["properties", "Vehicles", "Configuration", "ComponentListPosition", "Component", "AxleConfiguration","AxleSpacingListPosition","AxleSpacing","value"])

        number_Axles_Spacing_toFollowing=extract_element_from_json(data, ["properties", "Vehicles", "Configuration","ComponentListPosition", "Component", "AxleConfiguration","AxleSpacingToFollowing"])
    

        ##########crear diccionarios para ordenarlos#####
        maxlongitud=np.amax(number_Axles_longitude)
        d_spacing_to_following = {}

        for i in range(1, maxlongitud+1):
            for x in range(0, len(number_Axles_longitude)):
                if (i==int(number_Axles_longitude[x])):
                    d_spacing_to_following[i]=number_Axles_Spacing_toFollowing[x]

        
        d1= {}
        d2= {}

        startcount=0
        a=0
        b=0
        fin=0
        vector2=[]
        vector3=[]
        for i in range(0, len(number_Axles2)):
            a=int(number_Axles2[i])
            fin=0
            for x in range(startcount, len(number_Axles_Spacing_Count)):
                if fin==0:
                    b=b+int(number_Axles_Spacing_Count[x])
                    #d1[a].append(number_Axles_Value_count[x])
                    vector2.append(number_Axles_Spacing_Count[x]) 
                    vector3.append(number_Axles_Spacing_Value[x])
                    if (b+1==a):
                        d1[a]=vector2
                        d2[a]=vector3
                        vector2=[]
                        vector3=[]
                        startcount=x+1
                        b=0
                        fin=1
                


        ####modificar los vectores anteriores pero ahora ordenados según longitud####
        number_Axles2=[]
        number_Axles_Spacing_Count=[]
        number_Axles_Spacing_Value=[]
        number_Axles_Spacing_toFollowing=[]
        for i in range(1, maxlongitud+1):
            number_Axles2.append(d[i])
            number_Axles_Spacing_toFollowing.append(d_spacing_to_following[i])
            for keyd1 in d1:
                if(d[i]==keyd1):
                    for xx in d1[keyd1]:
                        number_Axles_Spacing_Count.append(xx)
            for keyd2 in d2:
                if(d[i]==keyd2):
                    for yy in d2[keyd2]:
                        number_Axles_Spacing_Value.append(yy)


        for N_A in number_Axles2:
            v1=int(N_A)
            fin_v1=0
            for N_A_Count in range (contadorinicio, len(number_Axles_Spacing_Count)):
                if fin_v1==0:
                    v2=int(number_Axles_Spacing_Count[N_A_Count])  
                    v3=int(number_Axles_Spacing_Value[N_A_Count])   
                    for x in range(0,v2):
                        i=i+1
                        workssheetLB10masIcoma22[i]=v3
                    total_Count=total_Count+v2

                    if (total_Count>=v1):                       
                        contadorinicio=N_A_Count+1
                        total_Count=0
                        fin_v1=1
                        break           



        #####calculate final vectors#########
        total_NA_values=0
        i=0
        total_Count=0
        contadorinicio=0
        fin_v1=1
        i_spacing=0

        for N_A in number_Axles:
            v1=int(N_A)
            fin_v1=0
            for N_A_Count in range (contadorinicio, len(number_Axles_Spacing_Count)):
                if fin_v1==0:
                    v2=int(number_Axles_Spacing_Count[N_A_Count])  
                    v3=float(number_Axles_Spacing_Value[N_A_Count]) 
                    for x in range(0,v2):
                        i=i+1
                        workssheetLB10masIcoma24[i]=v3
                    total_Count=total_Count+v2

                    if (total_Count+1==v1):   
                        i=i+1   
                        if (str(number_Axles_Spacing_toFollowing[i_spacing])!='None'):
                            workssheetLB10masIcoma24[i]=(number_Axles_Spacing_toFollowing[i_spacing])
                        else:
                            workssheetLB10masIcoma24[i]=0

                        i_spacing=i_spacing+1
                        contadorinicio=N_A_Count+1
                        total_Count=0
                        fin_v1=1
                        break



        #################Estructura##############

        #print("-------------------------------STRUCTURE-----------------------------")

        #Span_SequencePosition=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "Span", "SpanPosition","SequencePosition"])
        Span_SequencePosition=[]
        Span_SequencePosition_vectorDuplicated=[]
        Span_SequencePosition_Duplicated=[None for c in range(100)]
        total_structures=0
        Span_SequencePosition_missing=[None for c in range(100)]
        d_estructure_spans={}
        v_estructure_spans=[]
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            total_structures=total_structures+1
            if (len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"]) == 0):
                Span_SequencePosition_missing[y+1]=1
                Span_SequencePosition.append(0)
                v_estructure_spans.append(0)
            else:                
                for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"])):
                    Span_SequencePosition_Duplicated[y+1]=0
                    for z in Span_SequencePosition_vectorDuplicated:
                        if z==data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"]:
                            Span_SequencePosition_Duplicated[y+1]=1
                            Span_SequencePosition.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"])
                            v_estructure_spans.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"])
                    if Span_SequencePosition_Duplicated[y+1]==0:
                        if (data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"] != ""):
                            Span_SequencePosition_vectorDuplicated.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"])
                            Span_SequencePosition.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"])
                            v_estructure_spans.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["SpanPosition"]["SequencePosition"])
                        else:
                            Span_SequencePosition_missing[y+1]=1
                            Span_SequencePosition.append(0)
                            v_estructure_spans.append(0)
            d_estructure_spans[y+1]=v_estructure_spans
            v_estructure_spans=[]
            Span_SequencePosition_vectorDuplicated=[]
            


        

        #Span_Lenght=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "Span", "Length"])
        d2_estructure_spans={}
        v2_estructure_spans=[]
        d_length_missing={}
        length_missing=0
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            length_missing=0
            for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"])):
                if data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["Length"]!="":
                    v2_estructure_spans.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["Length"])
                else:
                    length_missing=1
                    v2_estructure_spans.append(1)

            d2_estructure_spans[y+1]=v2_estructure_spans
            v2_estructure_spans=[]
            d_length_missing[y+1]=length_missing


        

        #Span_StructureType=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "Span", "StructureType"])
        d_estructure_Type={}
        v_estructure_Type=[]
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"])):
                v_estructure_Type.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["StructureType"])
            d_estructure_Type[y+1]=v_estructure_Type
            v_estructure_Type=[]

        



        #Span_Construction=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "Span", "Construction"])
        d_structure_Construction={}
        v_estructure_Construction=[]
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"])):
                v_estructure_Construction.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["Span"][x]["Construction"])
            d_structure_Construction[y+1]=v_estructure_Construction
            v_estructure_Construction=[]


        ###### restriction applayed ########
        SignedWeightConstraints=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","additionalProperties", "additionalProperties", "SignedWeightConstraints"])
        SignedWeightConstraints_variable=[None for c in range(100)]
        for x in range(0, len(SignedWeightConstraints)):
            if SignedWeightConstraints[x]=='AxleWeight':
                SignedWeightConstraints_variable[x+1]=1
            elif SignedWeightConstraints[x]=='GrossWeight':
                SignedWeightConstraints_variable[x+1]=1
            elif SignedWeightConstraints[x]=='DoubleAxleWeight':
                SignedWeightConstraints_variable[x+1]=1
            elif SignedWeightConstraints[x]=='TripleAxleWeight':
                SignedWeightConstraints_variable[x+1]=1
            else:
                SignedWeightConstraints_variable[x+1]=0
        


        all_Span_HBRating=[]
        d_all_Span_HBRating={}
        
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            try:
                if (len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"])>0):
                    for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"])):
                        all_Span_HBRating.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"][x]["HBRatingWithLoad"])
                else:
                    all_Span_HBRating.append(None)
            except:
                try:
                    all_Span_HBRating.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["HBRatingWithLoad"])
                except:
                    all_Span_HBRating.append(None)
            #Span_HBRating.append(min(all_Span_HBRating))
            d_all_Span_HBRating[y+1]=all_Span_HBRating
            all_Span_HBRating=[]





        

        #Ya no se usa#Span_SVRating_ignored=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "LoadRating", "SVRating"])
        
        #Span_SVReserve=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "LoadRating", "SVParameters", "SVReserveWithLoad"])
        #Span_SVRating_valid=extract_element_from_json(data, ["properties", "EsdalStructure", "UnderbridgeSections","UnderbridgeSection", "LoadRating", "SVParameters", "VehicleType"])
        
        d_Span_SVRating_valid={}
        Span_SVRating_valid=[]

        d_Span_SVReserve={}
        Span_SVReserve=[]
        for y in range(0, len(data["properties"]["EsdalStructure"])):
            try:
                for x in range(0, len(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["SVParameters"])):
                    Span_SVRating_valid.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["SVParameters"][x]["VehicleType"])
                    Span_SVReserve.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["SVParameters"][x]["SVReserveWithLoad"])
            except:
                try:
                    Span_SVRating_valid.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["SVParameters"]["VehicleType"])
                    Span_SVReserve.append(data["properties"]["EsdalStructure"][y]["UnderbridgeSections"]["UnderbridgeSection"]["LoadRating"]["SVParameters"]["SVReserveWithLoad"])
                except:
                    Span_SVRating_valid.append(None)
                    Span_SVReserve.append(None)
            d_Span_SVRating_valid[y+1]=Span_SVRating_valid
            Span_SVRating_valid=[]
            d_Span_SVReserve[y+1]=Span_SVReserve
            Span_SVReserve=[]
        




        repetido=[]
        cambio=0
        no_entra=0
        x=1
        
        for y in range(0, len(Span_SequencePosition)):
            span_seq_count=Span_SequencePosition[y]
            cambio=0
            for v in repetido:
                if span_seq_count==v:
                    cambio=1
            if cambio==0:
                repetido.append(span_seq_count)
            else:
                x=x+1
                repetido=[]
                repetido.append(span_seq_count)


        v1_f=[]
        d1_f={}
        v2_f=[]
        d2_f={}

        d_estructure_Type_f={}
        v_estructure_Type_f=[]
        d_structure_Construction_f={}
        v_estructure_Construction_f=[]

        for x in range(1,total_structures+1):
            maxspan=np.amax(d_estructure_spans[x])
            for y in range(1,maxspan+1):
                for v in range(0,len(d_estructure_spans[x])):
                    value=d_estructure_spans[x][v]
                    if y==value:
                        v1_f.append(value)
                        v2_f.append(d2_estructure_spans[x][v])
                        v_estructure_Type_f.append(d_estructure_Type[x][v])
                        v_estructure_Construction_f.append(d_structure_Construction[x][v])
            d1_f[x]=v1_f
            v1_f=[]
            d2_f[x]=v2_f
            v2_f=[]
            d_estructure_Type_f[x]=v_estructure_Type_f
            v_estructure_Type_f=[]
            d_structure_Construction_f[x]=v_estructure_Construction_f
            v_estructure_Construction_f=[]


        
        
        ###REGLAS ELEGIR HB o SV Y QUÉ SV COGER(REGLAS DE FRANCISCO):
        d_Span_SVRating={}
        d_HB_or_SV_value={}
        EntraRegla1=0
        haySVTT=0
        entraifmayorde1=0
        v_mayorde1=[]

        d_HB_or_SV={}

        for x in range(1,total_structures+1):
            EntraRegla1=0
            entraifmayorde1=0
            v_mayorde1=[]
            if( int(data["properties"]["Vehicles"]["ConfigurationSummaryListPosition"]["ConfigurationComponentsNo"])  > 1):
                for y in range(0, len(d_Span_SVRating_valid[x])):
                    if(d_Span_SVRating_valid[x][y]=='SVTrain' and d_Span_SVReserve[x][y]>1):
                        d_Span_SVRating[x]='SVTrain'
                        d_HB_or_SV_value[x]=d_Span_SVReserve[x][y]
                        d_HB_or_SV[x]='SV'
                        EntraRegla1=1
            if EntraRegla1==0:
                for y in range(0, len(d_Span_SVReserve[x])):
                    try:#si hay algún sv
                        if (d_Span_SVReserve[x][y]>1 and d_Span_SVRating_valid[x][y]!='SVTT'):
                            v_mayorde1.append(d_Span_SVReserve[x][y])
                            entraifmayorde1=1

                    except:#si no hay sv buscamos el hb
                        if( d_all_Span_HBRating[x]!=None):## si hay b
                            d_HB_or_SV[x]='HB'
                            try:
                                d_HB_or_SV_value[x]=min(d_all_Span_HBRating[x])
                                d_Span_SVRating[x]=None
                            except:
                                d_HB_or_SV_value[x]=0
                                d_Span_SVRating[x]=None
                if (entraifmayorde1==0 and d_all_Span_HBRating[x][0]!=None) :# si no entra en esa condificion cogemos el hb si tiene, si no tiene cogemos el svtt si es que tiene
                    d_HB_or_SV[x]='HB'
                    d_HB_or_SV_value[x]=min(d_all_Span_HBRating[x])
                    d_Span_SVRating[x]=None

                elif (entraifmayorde1==0 and d_all_Span_HBRating[x][0]==None):
                    for y in range(0, len(d_Span_SVReserve[x])):
                        try:#si hay algún svtt
                            if (d_Span_SVReserve[x][y]>1 and d_Span_SVRating_valid[x][y]=='SVTT'):
                                d_Span_SVRating[x]="SVTT"
                                d_HB_or_SV_value[x]=d_Span_SVReserve[x][y]
                                d_HB_or_SV[x]='SV'
                        except:
                            pass

                if(len(v_mayorde1)>0):#si hay algún sv
                    minmayorde1=min(v_mayorde1)
                    for y in range(0,len(d_Span_SVReserve[x])):
                        if (d_Span_SVReserve[x][y]==minmayorde1):
                            d_Span_SVRating[x]=d_Span_SVRating_valid[x][y]
                            d_HB_or_SV_value[x]=minmayorde1
                            d_HB_or_SV[x]='SV'


        d_workssheetLB4coma2masI={}
        v_workssheetLB4coma2masI=np.zeros(31)

        d_workssheetLB5coma2masI={}
        v_workssheetLB5coma2masI=np.zeros(31)

        
        for i in range(1,total_structures+1):
            for x in range(0,len(d2_f[i])): 
                v_workssheetLB4coma2masI[x+1]=d2_f[i][x]
                v_workssheetLB5coma2masI[x+1]=1
            
            d_workssheetLB4coma2masI[i]=v_workssheetLB4coma2masI
            v_workssheetLB4coma2masI=np.zeros(31)

            d_workssheetLB5coma2masI[i]=v_workssheetLB5coma2masI
            v_workssheetLB5coma2masI=np.zeros(31)


    
        # for i in range(1,total_structures+1):  
        #     if( str(d_Span_SVReserve[i])!='' and str(d_Span_SVReserve[i])!='None' ):
        #         d_HB_or_SV[i]='SV'
        #         d_HB_or_SV_value[i]=d_Span_SVReserve[i]
        #     elif( str(d_Span_HBRating[i])!='None' and str(d_Span_HBRating[i])!='' ):
        #         d_HB_or_SV[i]='HB'
        #         d_HB_or_SV_value[i]=d_Span_HBRating[i]
        #     else:
        #         d_HB_or_SV[i]=""
        #         d_HB_or_SV_value[i]=""

        d_rating_missing={}

        for i in range(1,total_structures+1):
            try:
                if d_HB_or_SV[i]=="" or d_HB_or_SV[i]==None or d_HB_or_SV_value[i]=='' or d_HB_or_SV_value[i]==None:
                    d_rating_missing[i]=1
                else:
                    d_rating_missing[i]=0
            except:
                d_HB_or_SV[i]='HB'
                d_HB_or_SV_value[i]=0
                d_rating_missing[i]=1



def writejson():
    global timestamp
    global d_ESRN
    global global_status
    global unable_to_assess_one_or_more_structures
    global data

    data_json={}
    dateTimeObj = datetime.now()

    esdalstructureresults={}
    esdalstructureresultsVector=[]
    for i in range(1,total_structures+1):
        str_current_status= d_current_status[i]
        if(d_comments[i] != "Lorem ipsum dolor"):

            if(d_comments[i] == "Unable to perform assessment - Structure not assessed due to data issue"):
                string_d_comments='E101'
            if(d_comments[i] == "Unable to perform assessment - Structure type not supported by Alsat"):
                string_d_comments='E102'
            if(d_comments[i] == "Unable to perform assessment - Weight restriction applayed"):
                string_d_comments='E201'
            if(d_comments[i] == "Unable to perform assessment - Data issue span sequence position duplicated"):
                string_d_comments='E302'
            if(d_comments[i] == "Unable to perform assessment - Data issue span sequence position missing"):
                string_d_comments='E303'
            if(d_comments[i] == "Unable to perform assessment - Data issue span length missing"):
                string_d_comments='E301'
            if(d_comments[i] == "Unable to perform assessment - Data issue structure rating missing"):
                string_d_comments='E202'
        else:
            string_d_comments=""
        esdalstructureresultsValues = {}
        esdalstructureresultsValues["ESRN"]=d_ESRN[str(i)]
        esdalstructureresultsValues["StructureKey"]=StructureKey[i-1]
        esdalstructureresultsValues["StructureCalculationType"]=d_estructure_Type_convert[i]
        esdalstructureresultsValues["result_structure"]=str_current_status 
        esdalstructureresultsValues["sf"]=sf
        esdalstructureresultsValues["comments_for_haulier"]=""
        esdalstructureresultsValues["assessment_comments"]=string_d_comments

        esdalstructureresultsVector.append(esdalstructureresultsValues)
    
    esdalstructureresults['EsdalStructure']=esdalstructureresultsVector 




    if unable_to_assess_one_or_more_structures==1:
        strig_unable_to_assess_one_or_more_structures="Unable to assess one or more structures"
    else:
        strig_unable_to_assess_one_or_more_structures=""


    data_json['$id']=data['$id']
    data_json['title']=data['title']
    data_json['type']=data['type']
    data_json['definitions']=data['definitions']
    data_json['schema']=data['schema']

    data_json['properties'] = []
    data_json['properties'].append({   
        "sequence_number":data['properties']['sequence_number'],
        "timestamp": timestamp[0],
        "timestamp_finish":str(dateTimeObj),
        "movement_id":notice_reference,
        "global_result": global_status,
        "global_comments":strig_unable_to_assess_one_or_more_structures,
    })

    data_json['properties'].append(esdalstructureresults)

    v=notice_reference.split("/")
    string_notice_reference=""
    for x in range(0,len(v)):
        if x<len(v)-1:
            string_notice_reference=string_notice_reference+v[x]+"-"
        else:
            string_notice_reference=string_notice_reference+v[x]
    datatext=string_notice_reference+'.json'
    

    with open(str(datatext), 'w+') as outfile:
        json.dump(data_json, outfile , indent=4)

    

    return datatext

#@login_required
def command_json(request):  

    json=request.GET['json']

    myquery = { "id": json }
    mydoc = collection_summary.find_one(myquery)

    matrix_output=mydoc["variables"][0]["matrix_output"]
    global_status=mydoc["variables"][0]["global result"]

    return render(request, 'summary.html',{'matrix_output':matrix_output,'global_status':global_status, 'json':json})

#@login_required
def command(request):

    structureVSjson=request.GET['structure']
    structureVSjson=structureVSjson.split("&&")
    structure=structureVSjson[0]
    json=(structureVSjson[1])


    myquery = { "id": json }
    mydoc = collection_results.find_one(myquery)


    d_StructureKey=mydoc["variables"][0]["d_StructureKey"]
    d_current_status=mydoc["variables"][0]["d_current_status"]
    d_HB_or_SV=mydoc["variables"][0]["d_HB_or_SV"]
    d_HB_or_SV_value=mydoc["variables"][0]["d_HB_or_SV_value"]
    notice_reference=mydoc["variables"][0]["notice_reference"]
    d_r_St_type=mydoc["variables"][0]["d_r_St_type"]
    d_r_HB1=mydoc["variables"][0]["d_r_HB1"]
    d_r_HB2=mydoc["variables"][0]["d_r_HB2"]
    d_r_d_result_HB=mydoc["variables"][0]["d_r_d_result_HB"]
    d_r_SHR1=mydoc["variables"][0]["d_r_SHR1"]
    d_r_text_SHR=mydoc["variables"][0]["d_r_text_SHR"]
    d_r_SHR2=mydoc["variables"][0]["d_r_SHR2"]
    d_r_d_result_SHR=mydoc["variables"][0]["d_r_d_result_SHR"]
    d_r_text_HB=mydoc["variables"][0]["d_r_text_HB"]
    d_r_text_HB=mydoc["variables"][0]["d_r_text_HB"]
    vehicle_assessed=mydoc["variables"][0]["vehicle_assessed"]
    d_r_text_HB_pin=mydoc["variables"][0]["d_r_text_HB_pin"]
    d_r_text_SHR_pin=mydoc["variables"][0]["d_r_text_SHR_pin"]
    d_r_HB1_pin=mydoc["variables"][0]["d_r_HB1_pin"]
    d_r_SHR1_pin=mydoc["variables"][0]["d_r_SHR1_pin"]
    d_r_HB2_pin=mydoc["variables"][0]["d_r_HB2_pin"]
    d_r_SHR2_pin=mydoc["variables"][0]["d_r_SHR2_pin"]
    d_r_d_result_HB_pin=mydoc["variables"][0]["d_r_d_result_HB_pin"]
    d_r_d_result_SHR_pin=mydoc["variables"][0]["d_r_d_result_SHR_pin"]
    d_r_text_HB_fix=mydoc["variables"][0]["d_r_text_HB_fix"]
    d_r_text_SHR_fix=mydoc["variables"][0]["d_r_text_SHR_fix"]
    d_r_HB1_fix=mydoc["variables"][0]["d_r_HB1_fix"]
    d_r_SHR1_fix=mydoc["variables"][0]["d_r_SHR1_fix"]
    d_r_HB2_fix=mydoc["variables"][0]["d_r_HB2_fix"]
    d_r_SHR2_fix=mydoc["variables"][0]["d_r_SHR2_fix"]
    d_r_d_result_HB_fix=mydoc["variables"][0]["d_r_d_result_HB_fix"]
    d_r_d_result_SHR_fix=mydoc["variables"][0]["d_r_d_result_SHR_fix"]
    d_fallaContinouos=mydoc["variables"][0]["d_fallaContinouos"]
    d_r_HB1_hjs=mydoc["variables"][0]["d_r_HB1_hjs"]
    d_r_SHR1_hjs=mydoc["variables"][0]["d_r_SHR1_hjs"]
    d_r_HB2_hjs=mydoc["variables"][0]["d_r_HB2_hjs"]
    d_r_SHR2_hjs=mydoc["variables"][0]["d_r_SHR2_hjs"]
    d_r_d_result_HB_hjs=mydoc["variables"][0]["d_r_d_result_HB_hjs"]
    d_r_d_result_SHR_hjs=mydoc["variables"][0]["d_r_d_result_SHR_hjs"]
    d_r_text_HB_hjs=mydoc["variables"][0]["d_r_text_HB_hjs"]
    d_r_text_SHR_hjs=mydoc["variables"][0]["d_r_text_SHR_hjs"]
    d_current_status_hb=mydoc["variables"][0]["d_current_status_hb"]
    d_current_status_shr=mydoc["variables"][0]["d_current_status_shr"]
    d_sf=mydoc["variables"][0]["d_sf"]
    d_Span_SVRating=mydoc["variables"][0]["d_Span_SVRating"]
    d_estructure_Type_convert=mydoc["variables"][0]["d_estructure_Type_convert"]
    d_current_status_hb_hjs=mydoc["variables"][0]["d_current_status_hb_hjs"]
    d_current_status_shr_hjs=mydoc["variables"][0]["d_current_status_shr_hjs"]
    d_ldds_f=mydoc["variables"][0]["d_ldds_f"]
    d_ldds_position_f=mydoc["variables"][0]["d_ldds_position_f"]
    valid_data=mydoc["variables"][0]["valid_data"]
    d_extra_check_hj=mydoc["variables"][0]["d_extra_check_hj"]
    d_workssheetLB4coma2masI=mydoc["variables"][0]["d_workssheetLB4coma2masI"]
    d_comments=mydoc["variables"][0]["d_comments"]
    d_ESRN=mydoc["variables"][0]["d_ESRN"]
        

  
    d_workssheetLB4coma2masI_f={}
    count=0
    v_workssheetLB4coma2masI_f=[]
    for x in d_workssheetLB4coma2masI:
        for y in d_workssheetLB4coma2masI[x]:
            if int(y)==0:
                count=count+1
            elif ( (int(y)!=0) and count<2):

                v_workssheetLB4coma2masI_f.append(y)
        count=0
        d_workssheetLB4coma2masI_f[x]=v_workssheetLB4coma2masI_f
        v_workssheetLB4coma2masI_f=[]


    current_user = request.user
    
    if(current_user.userprofile.role=='engineer'):
        return render(request, 'result_engineer.html',{'structure':structure, 'd_StructureKey':d_StructureKey, 'd_current_status':d_current_status ,'d_HB_or_SV':d_HB_or_SV,\
        'd_HB_or_SV_value':d_HB_or_SV_value,  'notice_reference':notice_reference,'d_r_St_type':d_r_St_type, 'd_r_HB1':d_r_HB1, 'd_r_text_HB':d_r_text_HB,\
        'd_r_HB2':d_r_HB2, 'd_r_d_result_HB':d_r_d_result_HB,'d_r_SHR1':d_r_SHR1 ,'d_r_text_SHR':d_r_text_SHR, 'd_r_SHR2':d_r_SHR2, 'd_r_d_result_SHR':d_r_d_result_SHR,\
        'vehicle_assessed':vehicle_assessed, 'd_r_text_HB_pin':d_r_text_HB_pin,'d_r_text_SHR_pin': d_r_text_SHR_pin, 'd_r_HB1_pin':d_r_HB1_pin,'d_r_SHR1_pin':d_r_SHR1_pin,\
        'd_r_HB2_pin':d_r_HB2_pin, 'd_r_SHR2_pin':d_r_SHR2_pin, 'd_r_d_result_HB_pin': d_r_d_result_HB_pin,'d_r_d_result_SHR_pin': d_r_d_result_SHR_pin,\
        'd_r_text_HB_fix':d_r_text_HB_fix,'d_r_text_SHR_fix': d_r_text_SHR_fix, 'd_r_HB1_fix':d_r_HB1_fix,'d_r_SHR1_fix':d_r_SHR1_fix, 'd_r_HB2_fix':d_r_HB2_fix,\
        'd_r_SHR2_fix':d_r_SHR2_fix, 'd_r_d_result_HB_fix': d_r_d_result_HB_fix, 'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix, 'd_fallaContinouos':d_fallaContinouos,\
        'd_r_HB1_hjs':d_r_HB1_hjs, 'd_r_SHR1_hjs':d_r_SHR1_hjs, 'd_r_HB2_hjs':d_r_HB2_hjs, 'd_r_SHR2_hjs':d_r_SHR2_hjs, 'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs,\
        'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs, 'd_r_text_HB_hjs': d_r_text_HB_hjs, 'd_r_text_SHR_hjs':d_r_text_SHR_hjs,\
        'd_current_status_hb':d_current_status_hb, 'd_current_status_shr':d_current_status_shr, 'd_sf':d_sf, 'd_Span_SVRating':d_Span_SVRating,\
        'd_estructure_Type_convert':d_estructure_Type_convert, 'd_current_status_hb_hjs': d_current_status_hb_hjs, 'd_current_status_shr_hjs':d_current_status_shr_hjs,\
        'd_ldds_f':d_ldds_f, 'd_ldds_position_f':d_ldds_position_f, 'valid_data':valid_data, 'd_extra_check_hj':d_extra_check_hj, 'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI_f,\
        'd_comments':d_comments, 'd_ESRN':d_ESRN})
    else:
        return render(request, 'result.html',{'structure':structure, 'd_StructureKey':d_StructureKey, 'd_current_status':d_current_status ,'d_HB_or_SV':d_HB_or_SV,\
        'd_HB_or_SV_value':d_HB_or_SV_value,  'notice_reference':notice_reference,'d_r_St_type':d_r_St_type, 'd_r_HB1':d_r_HB1, 'd_r_text_HB':d_r_text_HB,\
        'd_r_HB2':d_r_HB2, 'd_r_d_result_HB':d_r_d_result_HB,'d_r_SHR1':d_r_SHR1 ,'d_r_text_SHR':d_r_text_SHR, 'd_r_SHR2':d_r_SHR2, 'd_r_d_result_SHR':d_r_d_result_SHR,\
        'vehicle_assessed':vehicle_assessed, 'd_r_text_HB_pin':d_r_text_HB_pin,'d_r_text_SHR_pin': d_r_text_SHR_pin, 'd_r_HB1_pin':d_r_HB1_pin,'d_r_SHR1_pin':d_r_SHR1_pin,\
        'd_r_HB2_pin':d_r_HB2_pin, 'd_r_SHR2_pin':d_r_SHR2_pin, 'd_r_d_result_HB_pin': d_r_d_result_HB_pin,'d_r_d_result_SHR_pin': d_r_d_result_SHR_pin,\
        'd_r_text_HB_fix':d_r_text_HB_fix,'d_r_text_SHR_fix': d_r_text_SHR_fix, 'd_r_HB1_fix':d_r_HB1_fix,'d_r_SHR1_fix':d_r_SHR1_fix, 'd_r_HB2_fix':d_r_HB2_fix,\
        'd_r_SHR2_fix':d_r_SHR2_fix, 'd_r_d_result_HB_fix': d_r_d_result_HB_fix, 'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix, 'd_fallaContinouos':d_fallaContinouos,\
        'd_r_HB1_hjs':d_r_HB1_hjs, 'd_r_SHR1_hjs':d_r_SHR1_hjs, 'd_r_HB2_hjs':d_r_HB2_hjs, 'd_r_SHR2_hjs':d_r_SHR2_hjs, 'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs,\
        'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs, 'd_r_text_HB_hjs': d_r_text_HB_hjs, 'd_r_text_SHR_hjs':d_r_text_SHR_hjs,\
        'd_current_status_hb':d_current_status_hb, 'd_current_status_shr':d_current_status_shr, 'd_sf':d_sf, 'd_Span_SVRating':d_Span_SVRating,\
        'd_estructure_Type_convert':d_estructure_Type_convert, 'd_current_status_hb_hjs': d_current_status_hb_hjs, 'd_current_status_shr_hjs':d_current_status_shr_hjs,\
        'd_ldds_f':d_ldds_f, 'd_ldds_position_f':d_ldds_position_f, 'valid_data':valid_data, 'd_extra_check_hj':d_extra_check_hj, 'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI_f,\
        'd_comments':d_comments, 'd_ESRN':d_ESRN})

def jsonDatabase_Summaryvariables():
    global matrix_output
    global d_comments
    
    string_comments="Lorem ipsum dolor"
    for key in d_comments:
        if d_comments[key]=="Unable to perform assessment - Structure not assessed due to data issue":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Structure type not supported by Alsat":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Weight restriction applayed":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Data issue span sequence position duplicated":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Data issue span sequence position missing":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Data issue span length missing":
            string_comments="Unable to assess one or more structures"
        elif d_comments[key]=="Unable to perform assessment - Data issue structure rating missing":
            string_comments="Unable to assess one or more structures"

    data={}      
    data['variables'] = []
    data['variables'].append({

    "global result": global_status,
    "matrix_output":matrix_output,
    "d_comments":string_comments})

    data["id"]=notice_reference
    collection_summary.insert_one(data)

def jsonDatabase_ResultAllvariables():

    global d_current_status
    global d_HB_or_SV
    global d_HB_or_SV_value
    global d_r_St_type
    global d_r_HB1
    global d_r_text_HB
    global d_r_HB2
    global d_r_d_result_HB
    global d_r_SHR1
    global d_r_text_SHR
    global d_r_SHR2
    global d_r_d_result_SHR
    global d_r_text_HB_pin
    global d_r_text_SHR_pin
    global d_r_HB1_pin
    global d_r_SHR1_pin
    global d_r_HB2_pin
    global d_r_SHR2_pin
    global d_r_d_result_HB_pin
    global d_r_d_result_SHR_pin
    global d_r_text_HB_fix
    global d_r_text_SHR_fix
    global d_r_HB1_fix
    global d_r_SHR1_fix
    global d_r_HB2_fix
    global d_r_SHR2_fix
    global d_r_d_result_HB_fix
    global d_r_d_result_SHR_fix
    global d_fallaContinouos
    global d_r_HB1_hjs
    global d_r_SHR1_hjs
    global d_r_HB2_hjs
    global d_r_SHR2_hjs
    global d_r_d_result_HB_hjs
    global d_r_d_result_SHR_hjs
    global d_r_text_HB_hjs
    global d_r_text_SHR_hjs
    global d_current_status_hb
    global d_current_status_shr
    global d_sf
    global d_Span_SVRating
    global d_estructure_Type_convert
    global d_current_status_hb_hjs
    global d_current_status_shr_hjs
    global d_ldds_f
    global d_ldds_position_f
    global d_extra_check_hj
    global d_calc_type
    global d_comments
    global d_all_Span_HBRating
    global data
    global d_ESRN
    global d_Span_SVRating_valid
    global d_Span_SVReserve

    
    
    workssheetLB10masIcoma22_l=[None for c in range(31)]
    for y in range(0,  31 ):
        workssheetLB10masIcoma22_l[y]=workssheetLB10masIcoma22[y]

    workssheetLB10masIcoma24_l=[None for c in range(31)]
    for y in range(0,  31 ):
        workssheetLB10masIcoma24_l[y]=workssheetLB10masIcoma24[y]
    

    d_workssheetLB4coma2masI_l={}
    for x in d_workssheetLB4coma2masI:
        matrix_output=[None for c in range(31)]
        for y in range(0,  31 ):
            matrix_output[y]=d_workssheetLB4coma2masI[x][y]
        d_workssheetLB4coma2masI_l[str(x)]=matrix_output


    d_workssheetLB5coma2masI_l={}
    for x in d_workssheetLB5coma2masI:
        matrix_output=[None for c in range(31)]
        for y in range(0,  31 ):
            matrix_output[y]=d_workssheetLB5coma2masI[x][y]
        d_workssheetLB5coma2masI_l[str(x)]=matrix_output
    


    matrix_output=[[None for c in range(3)] for r in range(total_structures)]
    i=-1
    for key in d_StructureKey:
        i=i+1
        matrix_output[i][0]=key
        matrix_output[i][1]=d_StructureKey[key]

    
    d_r_HB1_l={}
    for x in d_r_HB1:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1[x]))]
        for y in range(0,  len(d_r_HB1[x]) ):
            try:
                if len(d_r_HB1[x][y][0]) > 1:
                    for w in d_r_HB1[x][y][0]:
                        matrix_output[y][0]=d_r_HB1[x][y][0].tolist()
                        matrix_output[y][1]=d_r_HB1[x][y][1].tolist()
                        matrix_output[y][2]=d_r_HB1[x][y][2].tolist()

            except:
                matrix_output[y][0]=d_r_HB1[x][y][0]
                matrix_output[y][1]=d_r_HB1[x][y][1]
                matrix_output[y][2]=d_r_HB1[x][y][2]
        d_r_HB1_l[str(x)]=matrix_output
    

    d_r_HB2_l={}
    for x in d_r_HB2:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2[x]))]
        for y in range(0,  len(d_r_HB2[x]) ):
            try:
                if len(d_r_HB2[x][y][0]) > 1:
                    for w in d_r_HB2[x][y][0]:
                        matrix_output[y][0]=d_r_HB2[x][y][0].tolist()
                        matrix_output[y][1]=d_r_HB2[x][y][1].tolist()
                        matrix_output[y][2]=d_r_HB2[x][y][2].tolist()
            except:
                matrix_output[y][0]=d_r_HB2[x][y][0]
                matrix_output[y][1]=d_r_HB2[x][y][1]
                matrix_output[y][2]=d_r_HB2[x][y][2]

        d_r_HB2_l[str(x)]=matrix_output

    d_r_SHR1_l={}
    for x in d_r_SHR1:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1[x]))]
        for y in range(0,  len(d_r_SHR1[x]) ):
            try:
                if len(d_r_SHR1[x][y][0]) > 1:
                    for w in d_r_SHR1[x][y][0]:
                        matrix_output[y][0]=d_r_SHR1[x][y][0].tolist()
                        matrix_output[y][1]=d_r_SHR1[x][y][1].tolist()
            except:
                matrix_output[y][0]=d_r_SHR1[x][y][0]
                matrix_output[y][1]=d_r_SHR1[x][y][1]
        d_r_SHR1_l[str(x)]=matrix_output

    d_r_SHR2_l={}
    for x in d_r_SHR2:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2[x]))]
        for y in range(0,  len(d_r_SHR2[x]) ):
            try:
                if len(d_r_SHR2[x][y][0]) > 1:
                    for w in d_r_SHR2[x][y][0]:
                        matrix_output[y][0]=d_r_SHR2[x][y][0].tolist()
                        matrix_output[y][1]=d_r_SHR2[x][y][1].tolist()
            except:
                matrix_output[y][0]=d_r_SHR2[x][y][0]
                matrix_output[y][1]=d_r_SHR2[x][y][1]
        d_r_SHR2_l[str(x)]=matrix_output

        
    d_r_HB1_pin_l={}
    for x in d_r_HB1_pin:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_pin[x]))]
        for y in range(0,  len(d_r_HB1_pin[x]) ):
            matrix_output[y][0]=d_r_HB1_pin[x][y][0]
            matrix_output[y][1]=d_r_HB1_pin[x][y][1]
            matrix_output[y][2]=d_r_HB1_pin[x][y][2]
        d_r_HB1_pin_l[str(x)]=matrix_output



    d_r_SHR1_pin_l={}
    for x in d_r_SHR1_pin:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_pin[x]))]
        for y in range(0,  len(d_r_SHR1_pin[x]) ):
            matrix_output[y][0]=d_r_SHR1_pin[x][y][0]
            matrix_output[y][1]=d_r_SHR1_pin[x][y][1]
        d_r_SHR1_pin_l[str(x)]=matrix_output    
    

    d_r_HB2_pin_l={}
    for x in d_r_HB2_pin:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_pin[x]))]
        for y in range(0,  len(d_r_HB2_pin[x]) ):
            matrix_output[y][0]=d_r_HB2_pin[x][y][0]
            matrix_output[y][1]=d_r_HB2_pin[x][y][1]
            matrix_output[y][2]=d_r_HB2_pin[x][y][2]
        d_r_HB2_pin_l[str(x)]=matrix_output


    d_r_SHR2_pin_l={}
    for x in d_r_SHR2_pin:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_pin[x]))]
        for y in range(0,  len(d_r_SHR2_pin[x]) ):
            matrix_output[y][0]=d_r_SHR2_pin[x][y][0]
            matrix_output[y][1]=d_r_SHR2_pin[x][y][1]
        d_r_SHR2_pin_l[str(x)]=matrix_output




    d_r_HB1_fix_l={}
    for x in d_r_HB1_fix:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_fix[x]))]
        for y in range(0,  len(d_r_HB1_fix[x]) ):
            matrix_output[y][0]=d_r_HB1_fix[x][y][0]
            matrix_output[y][1]=d_r_HB1_fix[x][y][1]
            matrix_output[y][2]=d_r_HB1_fix[x][y][2]
        d_r_HB1_fix_l[str(x)]=matrix_output

    d_r_SHR1_fix_l={}
    for x in d_r_SHR1_fix:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_fix[x]))]
        for y in range(0,  len(d_r_SHR1_fix[x]) ):
            matrix_output[y][0]=d_r_SHR1_fix[x][y][0]
            matrix_output[y][1]=d_r_SHR1_fix[x][y][1]
        d_r_SHR1_fix_l[str(x)]=matrix_output

    d_r_HB2_fix_l={}
    for x in d_r_HB2_fix:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_fix[x]))]
        for y in range(0,  len(d_r_HB2_fix[x]) ):
            matrix_output[y][0]=d_r_HB2_fix[x][y][0]
            matrix_output[y][1]=d_r_HB2_fix[x][y][1]
            matrix_output[y][2]=d_r_HB2_fix[x][y][2]
        d_r_HB2_fix_l[str(x)]=matrix_output

    d_r_SHR2_fix_l={}
    for x in d_r_SHR2_fix:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_fix[x]))]
        for y in range(0,  len(d_r_SHR2_fix[x]) ):
            matrix_output[y][0]=d_r_SHR2_fix[x][y][0]
            matrix_output[y][1]=d_r_SHR2_fix[x][y][1]
        d_r_SHR2_fix_l[str(x)]=matrix_output


    d_r_HB1_hjs_l={}
    for x in d_r_HB1_hjs:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB1_hjs[x]))]
        for y in range(0,  len(d_r_HB1_hjs[x]) ):
            matrix_output[y][0]=d_r_HB1_hjs[x][y][0]
            matrix_output[y][1]=d_r_HB1_hjs[x][y][1]
            matrix_output[y][2]=d_r_HB1_hjs[x][y][2]
        d_r_HB1_hjs_l[str(x)]=matrix_output


    d_r_SHR1_hjs_l={}
    for x in d_r_SHR1_hjs:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR1_hjs[x]))]
        for y in range(0,  len(d_r_SHR1_hjs[x]) ):
            matrix_output[y][0]=d_r_SHR1_hjs[x][y][0]
            matrix_output[y][1]=d_r_SHR1_hjs[x][y][1]
        d_r_SHR1_hjs_l[str(x)]=matrix_output


    d_r_HB2_hjs_l={}
    for x in d_r_HB2_hjs:
        matrix_output=[[None for c in range(3)] for r in range(len(d_r_HB2_hjs[x]))]
        for y in range(0,  len(d_r_HB2_hjs[x]) ):
            matrix_output[y][0]=d_r_HB2_hjs[x][y][0]
            matrix_output[y][1]=d_r_HB2_hjs[x][y][1]
            matrix_output[y][2]=d_r_HB2_hjs[x][y][2]
        d_r_HB2_hjs_l[str(x)]=matrix_output


    d_r_SHR2_hjs_l={}
    for x in d_r_SHR2_hjs:
        matrix_output=[[None for c in range(2)] for r in range(len(d_r_SHR2_hjs[x]))]
        for y in range(0,  len(d_r_SHR2_hjs[x]) ):
            matrix_output[y][0]=d_r_SHR2_hjs[x][y][0]
            matrix_output[y][1]=d_r_SHR2_hjs[x][y][1]
        d_r_SHR2_hjs_l[str(x)]=matrix_output



    d_r_d_result_HB_l={}
    d_r_d_result_HB_l0={}
    d={}
    v=[]
    
    for x in d_r_d_result_HB:   
        try:
            if isinstance(d_r_d_result_HB[x], list):
                matrix_output=[[None for c in range( len(d_r_d_result_HB[x])) ] for r in range(1)]
                for w in d_r_d_result_HB[x]:
                    for w1 in w:
                        d[str(w1)]=w[w1]
                    v.append(d)
                    d={}
                d_r_d_result_HB_l[str(x)]=v
                v=[]

            else:
                for y in range(0,  len(d_r_d_result_HB[x]) ):
                    d_r_d_result_HB_l0[str(y)]=d_r_d_result_HB[x][y]
                d_r_d_result_HB_l[str(x)]=d_r_d_result_HB_l0
                d_r_d_result_HB_l0={}
        except:
            pass
    


    


    d_r_d_result_SHR_l={}
    d_r_d_result_SHR_l0={}
    d={}
    v=[]
    for x in d_r_d_result_SHR:
        try:
            if isinstance(d_r_d_result_SHR[x], list):
                matrix_output=[[None for c in range( len(d_r_d_result_SHR[x])) ] for r in range(1)]
                for w in d_r_d_result_SHR[x]:
                    for w1 in w:
                        d[str(w1)]=w[w1]
                    v.append(d)
                    d={}
                d_r_d_result_SHR_l[str(x)]=v
                v=[] 


            else:
                for y in range(0,  len(d_r_d_result_SHR[x]) ):
                    d_r_d_result_SHR_l0[str(y)]=d_r_d_result_SHR[x][y]
                d_r_d_result_SHR_l[str(x)]=d_r_d_result_SHR_l0
                d_r_d_result_SHR_l0={}
        except:
            pass


    d_r_d_result_HB_pin_l={}
    d_r_d_result_HB_pin_l0={}
    for x in d_r_d_result_HB_pin:
        for y in d_r_d_result_HB_pin[x]:
            d_r_d_result_HB_pin_l0[str(y)]=d_r_d_result_HB_pin[x][y]
        d_r_d_result_HB_pin_l[str(x)]=d_r_d_result_HB_pin_l0
        d_r_d_result_HB_pin_l0={}

   

    d_r_d_result_SHR_pin_l={}
    d_r_d_result_SHR_pin_l0={}
    for x in d_r_d_result_SHR_pin:
        for y in d_r_d_result_SHR_pin[x]:
            d_r_d_result_SHR_pin_l0[str(y)]=d_r_d_result_SHR_pin[x][y]
        d_r_d_result_SHR_pin_l[str(x)]=d_r_d_result_SHR_pin_l0
        d_r_d_result_SHR_pin_l0={}


    d_r_d_result_HB_fix_l={}
    d_r_d_result_HB_fix_l0={}
    for x in d_r_d_result_HB_fix:
        for y in d_r_d_result_HB_fix[x]:
            d_r_d_result_HB_fix_l0[str(y)]=d_r_d_result_HB_fix[x][y]
        d_r_d_result_HB_fix_l[str(x)]=d_r_d_result_HB_fix_l0
        d_r_d_result_HB_fix_l0={}

    d_r_d_result_SHR_fix_l={}
    d_r_d_result_SHR_fix_l0={}
    for x in d_r_d_result_SHR_fix:
        for y in d_r_d_result_SHR_fix[x]:
            d_r_d_result_SHR_fix_l0[str(y)]=d_r_d_result_SHR_fix[x][y]
        d_r_d_result_SHR_fix_l[str(x)]=d_r_d_result_SHR_fix_l0
        d_r_d_result_SHR_fix_l0={}

    d_r_d_result_HB_hjs_l={}
    d_r_d_result_HB_hjs_l0={}
    for x in d_r_d_result_HB_hjs:
        for y in d_r_d_result_HB_hjs[x]:
            d_r_d_result_HB_hjs_l0[str(y)]=d_r_d_result_HB_hjs[x][y]
        d_r_d_result_HB_hjs_l[str(x)]=d_r_d_result_HB_hjs_l0
        d_r_d_result_HB_hjs_l0={}



    d_r_d_result_SHR_hjs_l={}
    d_r_d_result_SHR_hjs_l0={}
    for x in d_r_d_result_SHR_hjs:
        for y in d_r_d_result_SHR_hjs[x]:
            d_r_d_result_SHR_hjs_l0[str(y)]=d_r_d_result_SHR_hjs[x][y]
        d_r_d_result_SHR_hjs_l[str(x)]=d_r_d_result_SHR_hjs_l0
        d_r_d_result_SHR_hjs_l0={}



    d_extra_check_hj_l={}
    for x in d_extra_check_hj:
        matrix_output=[[None for c in range(4)] for r in range(1)]
        for y in range(0,  len(d_extra_check_hj[x]) ):
            matrix_output[y][0]=d_extra_check_hj[x][y][0]
            matrix_output[y][1]=d_extra_check_hj[x][y][1]
            matrix_output[y][2]=d_extra_check_hj[x][y][2]
            matrix_output[y][3]=d_extra_check_hj[x][y][3]
        d_extra_check_hj_l[str(x)]=matrix_output
    


    ### All values SV:

    

    d_all_Span_SVRating_l={}
    for x in range(1, len(d_Span_SVRating_valid)+1):
        matrix_output=[[None for c in range(2)] for r in range(len(d_Span_SVRating_valid[x]))]
        for y in range(0,  len(d_Span_SVRating_valid[x]) ):
            try:
                matrix_output[y][0]=d_Span_SVRating_valid[x][y]
                matrix_output[y][1]=d_Span_SVReserve[x][y]
            except:
                pass
        d_all_Span_SVRating_l[str(x)]=matrix_output



    d_r_text_HB_pin_l = dict((str(k),v) for k,v in d_r_text_HB_pin.items())
    d_r_text_SHR_pin_l = dict((str(k),v) for k,v in d_r_text_SHR_pin.items())
    d_r_text_HB_l = dict((str(k),v) for k,v in d_r_text_HB.items())
    d_r_text_SHR_l = dict((str(k),v) for k,v in d_r_text_SHR.items())
    d_current_status_l = dict((str(k),v) for k,v in d_current_status.items())    
    d_HB_or_SV_l = dict((str(k),v) for k,v in d_HB_or_SV.items())    
    d_HB_or_SV_value_l = dict((str(k),v) for k,v in d_HB_or_SV_value.items())    
    d_r_St_type_l = dict((str(k),v) for k,v in d_r_St_type.items())     
    d_r_text_HB_fix_l = dict((str(k),v) for k,v in d_r_text_HB_fix.items())
    d_r_text_SHR_fix_l = dict((str(k),v) for k,v in d_r_text_SHR_fix.items())
    d_fallaContinouos_l = dict((str(k),v) for k,v in d_fallaContinouos.items())
    d_r_text_HB_hjs_l = dict((str(k),v) for k,v in d_r_text_HB_hjs.items())
    d_r_text_SHR_hjs_l = dict((str(k),v) for k,v in d_r_text_SHR_hjs.items())
    d_current_status_hb_l = dict((str(k),v) for k,v in d_current_status_hb.items())
    d_current_status_shr_l = dict((str(k),v) for k,v in d_current_status_shr.items())
    d_sf_l = dict((str(k),v) for k,v in d_sf.items())
    d_Span_SVRating_l = dict((str(k),v) for k,v in d_Span_SVRating.items())
    d_estructure_Type_convert_l = dict((str(k),v) for k,v in d_estructure_Type_convert.items())
    d_current_status_hb_hjs_l = dict((str(k),v) for k,v in d_current_status_hb_hjs.items())
    d_current_status_shr_hjs_l = dict((str(k),v) for k,v in d_current_status_shr_hjs.items())
    d_ldds_f_l = dict((str(k),v) for k,v in d_ldds_f.items())
    d_ldds_position_f_l = dict((str(k),v) for k,v in d_ldds_position_f.items())
    d_calc_type = dict((str(k),v) for k,v in d_calc_type.items())
    d_comments_l = dict((str(k),v) for k,v in d_comments.items())
    d_all_Span_HBRating_l=dict((str(k),v) for k,v in d_all_Span_HBRating.items())





    data_json={}  

    

    
    data_json['variables'] = []
    data_json['variables'].append({

    'd_StructureKey':d_StructureKey,
    'd_current_status':d_current_status_l,
    'd_HB_or_SV':d_HB_or_SV_l,
    'd_HB_or_SV_value':d_HB_or_SV_value_l,
    'notice_reference':notice_reference,
    'd_r_St_type':d_r_St_type_l,
    'd_r_HB1':d_r_HB1_l,
    'd_r_text_HB':d_r_text_HB_l,
    'd_r_HB2':d_r_HB2_l,
    'd_r_d_result_HB':d_r_d_result_HB_l,
    'd_r_SHR1':d_r_SHR1_l,
    'd_r_text_SHR':d_r_text_SHR_l,
    'd_r_SHR2':d_r_SHR2_l,
    'd_r_d_result_SHR':d_r_d_result_SHR_l,
    'vehicle_assessed':vehicle_assessed,
    'd_r_text_HB_pin':d_r_text_HB_pin_l,
    'd_r_text_SHR_pin': d_r_text_SHR_pin_l,
    'd_r_HB1_pin':d_r_HB1_pin_l,
    'd_r_SHR1_pin':d_r_SHR1_pin_l,
    'd_r_HB2_pin':d_r_HB2_pin_l,
    'd_r_SHR2_pin':d_r_SHR2_pin_l,
    'd_r_d_result_HB_pin': d_r_d_result_HB_pin_l,
    'd_r_d_result_SHR_pin': d_r_d_result_SHR_pin_l,
    'd_r_text_HB_fix':d_r_text_HB_fix_l,
    'd_r_text_SHR_fix': d_r_text_SHR_fix_l,
    'd_r_HB1_fix':d_r_HB1_fix_l,
    'd_r_SHR1_fix':d_r_SHR1_fix_l,
    'd_r_HB2_fix':d_r_HB2_fix_l,
    'd_r_SHR2_fix':d_r_SHR2_fix_l,
    'd_r_d_result_HB_fix': d_r_d_result_HB_fix_l,
    'd_r_d_result_SHR_fix': d_r_d_result_SHR_fix_l,
    'd_fallaContinouos':d_fallaContinouos_l,
    'd_r_HB1_hjs':d_r_HB1_hjs_l,
    'd_r_SHR1_hjs':d_r_SHR1_hjs_l,
    'd_r_HB2_hjs':d_r_HB2_hjs_l,
    'd_r_SHR2_hjs':d_r_SHR2_hjs_l,
    'd_r_d_result_HB_hjs':d_r_d_result_HB_hjs_l,
    'd_r_d_result_SHR_hjs':d_r_d_result_SHR_hjs_l,
    'd_r_text_HB_hjs': d_r_text_HB_hjs_l,
    'd_r_text_SHR_hjs':d_r_text_SHR_hjs_l,
    'd_current_status_hb':d_current_status_hb_l,
    'd_current_status_shr':d_current_status_shr_l,
    'd_sf':d_sf_l,
    'd_Span_SVRating':d_Span_SVRating_l,    
    'd_estructure_Type_convert':d_estructure_Type_convert_l,
    'd_current_status_hb_hjs': d_current_status_hb_hjs_l,
    'd_current_status_shr_hjs':d_current_status_shr_hjs_l,
    'd_ldds_f':d_ldds_f_l,
    'd_ldds_position_f':d_ldds_position_f_l,
    'valid_data':valid_data,
    'd_extra_check_hj':d_extra_check_hj_l,
    'd_workssheetLB4coma2masI':d_workssheetLB4coma2masI_l,
    'd_workssheetLB5coma2masI':d_workssheetLB5coma2masI_l,
    'workssheetLB10masIcoma22':workssheetLB10masIcoma22_l,
    'workssheetLB10masIcoma24':workssheetLB10masIcoma24_l,
    'd_calc_type':d_calc_type,
    'd_comments':d_comments_l,
    'd_all_Span_HBRating':d_all_Span_HBRating_l,
    'd_ESRN':d_ESRN,
    'd_all_Span_SVRating':d_all_Span_SVRating_l,
    })

    data_json["id"]=notice_reference


    data_json["dolar_id"]=data['$id']
    data_json["title"]=data['title']
    data_json["type"]=data['type']
    data_json["definitions"]=data['definitions']
    data_json["schema"]=data['schema']
    data_json["timestamp"]=data['properties']['timestamp']
    data_json["sequence_number"]=data['properties']['sequence_number']

    collection_results.insert_one(data_json)

def calculate(jsontoload):

    global matrix_output
    global MaxMoveMomHB11
    global MaxMoveShrHB11
    global MaxMoveMomHB22
    global MaxMoveShrHB22
    global OpeninFlag
    global workssheetLB4coma2masI
    global workssheetLB5coma2masI
    global HB_rating
    global Reserve_Factor
    global HB_or_SV
    global notice_reference
    global StructureKey
    global d_ESRN
    global StructureType
    global vehicle_assessed
    global sf
    global Ldds
    global Ldds_position
    global OPTlhfixed
    global OPTlhpin
    global OPTrhfixed
    global OPTrhpin
    global SV_Rating
    global d_StructureKey
    global d_current_status 
    global d_HB_or_SV
    global d_HB_or_SV_value
    global d_r_St_type
    global d_r_HB1 
    global d_r_text_HB
    global d_r_HB2
    global d_r_d_result_HB
    global d_r_SHR1
    global d_r_text_SHR
    global d_r_SHR2
    global d_r_d_result_SHR
    global vehicle_assessed
    global d_r_text_HB_pin
    global d_r_text_SHR_pin
    global d_r_HB1_pin
    global d_r_SHR1_pin
    global d_r_HB2_pin
    global d_r_SHR2_pin
    global d_r_d_result_HB_pin
    global d_r_d_result_SHR_pin
    global d_r_text_HB_fix
    global d_r_text_SHR_fix
    global d_r_HB1_fix
    global d_r_SHR1_fix
    global d_r_HB2_fix
    global d_r_SHR2_fix
    global d_r_d_result_HB_fix
    global d_r_d_result_SHR_fix
    global d_fallaContinouos
    global d_r_HB1_hjs
    global d_r_SHR1_hjs
    global d_r_HB2_hjs
    global d_r_SHR2_hjs
    global d_r_d_result_HB_hjs
    global d_r_d_result_SHR_hjs
    global d_r_text_HB_hjs
    global d_r_text_SHR_hjs
    global d_current_status_hb
    global d_current_status_shr
    global d_sf
    global d_Span_SVRating
    global d_estructure_Type_convert
    global d_current_status_hb_hjs
    global d_current_status_shr_hjs
    global valid_data
    global global_status
    global d_extra_check_hj
    global d_ldds_f
    global d_ldds_position_f  
    global Factored
    global NoOF
    global NoDF
    global NoFact
    global d_calc_type
    global global_hj
    global d_comments
    global SignedWeightConstraints_variable    
    global Span_SequencePosition_Duplicated    
    global Span_SequencePosition_missing
    global d_length_missing
    global d_rating_missing
    global unable_to_assess_one_or_more_structures
    global data
    global timestamp


    valid_data=1

    ####################GET JSON DATA#########################################

    try:    
        get_Json_Data(jsontoload)
        
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("Whole structures:")
        print(StructureKey)

        d_r_HB1={}
        d_r_SHR1={}
        d_r_HB2={} 
        d_r_SHR2={} 
        d_r_d_result_HB={} 
        d_r_d_result_SHR={}
        d_r_HB1_pin={} 
        d_r_SHR1_pin={} 
        d_r_HB2_pin={} 
        d_r_SHR2_pin={} 
        d_r_d_result_HB_pin={} 
        d_r_d_result_SHR_pin={}
        d_r_HB1_fix={}
        d_r_SHR1_fix={} 
        d_r_HB2_fix={} 
        d_r_SHR2_fix={} 
        d_r_d_result_HB_fix={} 
        d_r_d_result_SHR_fix={}
        d_r_HB1_hjs={} 
        d_r_SHR1_hjs={} 
        d_r_HB2_hjs={} 
        d_r_SHR2_hjs={} 
        d_r_d_result_HB_hjs={} 
        d_r_d_result_SHR_hjs={}
        d_r_fallaContinouos={}
        d_r_St_type={}

        ####return variables#####
        d_r_text_HB={}
        d_r_text_m_HB={}
        d_r_text_SHR={}
        d_r_text_m_SHR={}
        d_current_status={}
        d_StructureKey={}
        d_r_text_HB_pin={}
        d_r_text_SHR_pin={}
        d_current_status_pin={}
        d_r_text_HB_fix={}
        d_r_text_SHR_fix={}
        d_current_status_fix={}
        d_fallaContinouos={}
        d_r_text_HB_hjs={}
        d_r_text_SHR_hjs={}
        d_current_status_hb={}
        d_current_status_shr={}
        d_sf={}
        d_estructure_Type_convert={}
        d_current_status_hb_hjs={}
        d_current_status_shr_hjs={}
        d_extra_check_hj={}
        d_ldds_f={}
        d_ldds_position_f={}
        d_calc_type={}
        d_comments={}


        unable_to_assess_one_or_more_structures=0

        for T_E in range (1, total_structures+1):
            St_type=0
            global_hj=0
            d_StructureKey[str(T_E)]=StructureKey[T_E-1]
            print("structure:" + str(StructureKey[T_E-1]))
            globalvariables()   

            #workssheetLB4coma2masI=d_workssheetLB4coma2masI[T_E]
            v_all=[]
            for x in d_workssheetLB4coma2masI:
                if x==T_E:
                    for y in d_workssheetLB4coma2masI[x]:
                        v_all.append(y)
                    workssheetLB4coma2masI=v_all
                    v_all=[]

            #workssheetLB5coma2masI=d_workssheetLB5coma2masI[T_E]
            v_all=[]
            for x in d_workssheetLB5coma2masI:
                if x==T_E:
                    for y in d_workssheetLB5coma2masI[x]:
                        v_all.append(y)
                    workssheetLB5coma2masI=v_all
                    v_all=[]

            HB_or_SV=d_HB_or_SV[T_E]
            print("HB_or_SV: " + HB_or_SV)
            if(HB_or_SV=='HB'):
                HB_rating=d_HB_or_SV_value[T_E]
                print("HB_rating: " + str(HB_rating))
            elif(HB_or_SV=='SV'):
                Reserve_Factor=d_HB_or_SV_value[T_E]
                SV_Rating=d_Span_SVRating[T_E]
                print("SV_Rating: " + str(SV_Rating))


            if StructureType[T_E-1]=="box culvert":
                St_type="2"
            elif StructureType[T_E-1]=="Framed Span - Bridges":
                St_type="2"
            elif StructureType[T_E-1]=="cable stayed bridge":
                St_type="1"
            elif StructureType[T_E-1]=="multi span bridge":
                St_type="1"
            elif StructureType[T_E-1]=="continuous span bridge" or StructureType[T_E-1]=="continuous span bridges":
                St_type="1"
            elif StructureType[T_E-1]=="integral structure":
                St_type="2"
            elif StructureType[T_E-1]=="portal frame":
                St_type="2"
            elif ( StructureType[T_E-1]=="simply supported span" or StructureType[T_E-1]=="Simply Supported Span"):
                St_type="3"
            elif StructureType[T_E-1]=="suspension bridge":
                St_type="-1"
            elif StructureType[T_E-1]=="lift":
                St_type="-1"
            elif StructureType[T_E-1]=="swing":
                St_type="-1"
            elif StructureType[T_E-1]=="pipe":
                St_type="3"

            elif StructureType[T_E-1]=="Open Arch":
                St_type="-1"
            elif StructureType[T_E-1]=="cantilever":
                St_type="1"
            elif StructureType[T_E-1]=="Arched":
                St_type="-1"
            elif StructureType[T_E-1]=="Uniform Box or Tubular Culvert":
                St_type="2"
            elif StructureType[T_E-1]=="Continuous":
                St_type="1"
            elif StructureType[T_E-1]=="masonry arch":
                St_type="-1"
            elif StructureType[T_E-1]=="Orthotropic Plate":
                St_type="-1"
            elif StructureType[T_E-1]=="continuous span":
                St_type="1"
            elif StructureType[T_E-1]=="integral structure":
                St_type="2"
            elif StructureType[T_E-1]=="propped cantilever":
                St_type="-1"
            # elif StructureType[T_E-1]=="Cantilever And Suspended Span":
            #     St_type="4"
            elif StructureType[T_E-1]=="Slab Flat":
                St_type="-1"
            elif StructureType[T_E-1]=="Slab Haunched":
                St_type="-1"
            elif StructureType[T_E-1]=="Composite Section Culvert":
                St_type="2"
            elif StructureType[T_E-1]=="Simply Supported":
                St_type="3"
            elif StructureType[T_E-1]=="Tied/Anchored":
                St_type="-1"
            elif StructureType[T_E-1]=="Arch":
                St_type="-1"
            elif StructureType[T_E-1]=="Filled Arch":
                St_type="-1"

            
            ## Half Joint Database##
            database = 'BBDD_SQL'
            halfjoint_table = 'halfjoint'
            cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
            #########check if it is Half-Joint#######
            cursor = cnxn.cursor()
            try:
                halfjoint_search = 'SELECT * FROM BBDD_SQL.dbo.' + halfjoint_table
                cursor.execute(halfjoint_search)
                ishalfjoint=0
                for row in cursor:
                    if(StructureKey[T_E-1]==row[0]):
                        St_type="4"
                        ishalfjoint=1
                        Ldds=row[1]
                        Ldds_position=row[2]
                        d_ldds_f[T_E]=Ldds
                        d_ldds_position_f[T_E]=Ldds_position

                if ishalfjoint==0:
                    Ldds=0
                    Ldds_position=0
            except:
                pass
            cnxn.close()
            ###########################################


            ######### structure type ########
            # print("Structure type:")
            # print("1. Continuous")
            # print("2. Box/Frame")
            # print("3. Simply-Supported")
            # print("4. Half-Joint")
            print("Structure analysis type: " + str(St_type))


            ######### comments
            if St_type==0:
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Structure not assessed due to data issue"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            elif St_type=="-1":
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Structure type not supported by Alsat"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            else:
                d_comments[T_E]="Lorem ipsum dolor"

            if SignedWeightConstraints_variable[T_E]==1:
                St_type=0
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Weight restriction applayed"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1

            if Span_SequencePosition_Duplicated[T_E]==1:
                St_type=0
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Data issue span sequence position duplicated"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            elif Span_SequencePosition_missing[T_E]==1:
                St_type=0
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Data issue span sequence position missing"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            elif d_length_missing[T_E]==1:
                St_type=0
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Data issue span length missing"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            if d_rating_missing[T_E]==1:
                St_type=0
                d_current_status[T_E]="FAIL"
                d_estructure_Type_convert[T_E]="Not Defined"
                d_comments[T_E]="Unable to perform assessment - Data issue structure rating missing"
                d_calc_type[T_E]="Not Defined"
                unable_to_assess_one_or_more_structures=1
            ###############################################################

            d_r_St_type[T_E]=St_type
            d_sf[T_E]=sf

            
            if(St_type=="1"):      
                d_estructure_Type_convert[T_E]='Continuous'     
                #####botones#####3
                OPTlhfixed=0
                OPTlhpin=1
                OPTrhfixed=0
                OPTrhpin=1   
                Factored=1
                NoOF=0
                NoDF=0
                NoFact=0       

                PREPARE_CALCS()

                if(HB_or_SV=="HB"):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
                elif(HB_or_SV=='SV'):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]

                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(32)
                MaxMoveMomHB=np.zeros((100,7))        
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))
                OpeninFlag=0
                
                workssheetLB3coma2masI=np.zeros(31)

                PREPARE_CALCS()
                MaxMoveMomHB2, MaxMoveShrHB2=Load_Axles_AIL()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]

                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]


                HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR =comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)

                d_r_HB1[T_E]=HB1
                d_r_SHR1[T_E]=SHR1
                d_r_HB2[T_E]=HB2
                d_r_SHR2[T_E]=SHR2
                d_r_d_result_HB[T_E]=d_result_HB
                d_r_d_result_SHR[T_E]=d_result_SHR

                ##################################### RETURN VALUES ########################            
                ######## HB1 ########
                v_text_m_HB=[]
                i=1           
                nciclos=int(len(d_r_HB1[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Mom at sup " + str(i)
                    b="Mom at span " + str(i)
                    v_text_m_HB.append(a)
                    v_text_m_HB.append(b)
                c="Mom at sup " + str(i+1)
                v_text_m_HB.append(c)
                d_r_text_HB[T_E]=v_text_m_HB

                ###### SHR1 #####
                v_text_m_SHR=[]
                i=1
                nciclos=int(len(d_r_SHR1[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Span " + str(i) + " left end"
                    b="Span " + str(i) + " right end"
                    v_text_m_SHR.append(a)
                    v_text_m_SHR.append(b)

                d_r_text_SHR[T_E]=v_text_m_SHR

                fail_hb=0
                fail_shr=0
                fail=0
                caution=0
                caution_hb=0
                caution_shr=0

                for x in d_r_d_result_HB[T_E]:
                    if (d_r_d_result_HB[T_E][x]=='FAIL'):
                        fail=1
                        fail_hb=1
                    elif (d_r_d_result_HB[T_E][x]=='CAUTION'):
                        caution=1
                        caution_hb=1

                if fail_hb==1:
                    d_current_status_hb[T_E]="FAIL"
                elif caution_hb==1:
                    d_current_status_hb[T_E]="CAUTION"
                else:
                    d_current_status_hb[T_E]="OK"

                for x in d_r_d_result_SHR[T_E]:
                    if (d_r_d_result_SHR[T_E][x]=='FAIL'):
                        fail=1
                        fail_shr=1
                    elif (d_r_d_result_SHR[T_E][x]=='CAUTION'):
                        caution=1
                        caution_shr=1

                if fail_shr==1:
                    d_current_status_shr[T_E]="FAIL"
                elif caution_shr==1:
                    d_current_status_shr[T_E]="CAUTION"
                else:
                    d_current_status_shr[T_E]="OK"

                if fail==1:
                    d_current_status[T_E]="FAIL"
                elif caution==1:
                    d_current_status[T_E]="CAUTION"
                else:
                    d_current_status[T_E]="OK"

                if (Factored==1):
                    d_calc_type[T_E]='Factored'
                elif (NoOF==1):
                    d_calc_type[T_E]='NoOF'
                elif (NoDF==1):
                    d_calc_type[T_E]='NoDF'
                elif (NoFact==1):
                    d_calc_type[T_E]='NoFact'
                        
            if(St_type=="2"):  
                d_estructure_Type_convert[T_E]='Box/Frame'   
                
                #####botones#####
                OPTlhfixed=0
                OPTlhpin=1
                OPTrhfixed=0
                OPTrhpin=1        
                Factored=1
                NoOF=0
                NoDF=0
                NoFact=0

                PREPARE_CALCS()
                if(HB_or_SV=="HB"):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
                elif(HB_or_SV=='SV'):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]
                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(32)
                MaxMoveMomHB=np.zeros((100,7))
                MaxMoveMomHB22=np.zeros((100,7))
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))        
                OpeninFlag=0########?????               
                workssheetLB3coma2masI=np.zeros(31)       

                PREPARE_CALCS()
                MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]
                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]
            
                HB1_pin, SHR1_pin, HB2_pin, SHR2_pin, d_result_HB_pin, d_result_SHR_pin = comparative(MaxMoveMomHB11, MaxMoveMomHB22, MaxMoveShrHB11, MaxMoveShrHB22)

                d_r_HB1_pin[T_E]=HB1_pin
                d_r_SHR1_pin[T_E]=SHR1_pin
                d_r_HB2_pin[T_E]=HB2_pin
                d_r_SHR2_pin[T_E]=SHR2_pin
                d_r_d_result_HB_pin[T_E]=d_result_HB_pin
                d_r_d_result_SHR_pin[T_E]=d_result_SHR_pin

                ##################################### RETURN VALUES ########################            
                ######## HB1 ########
                v_text_m_HB=[]
                i=1           
                nciclos=int(len(d_r_HB1_pin[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Mom at sup " + str(i)
                    b="Mom at span " + str(i)
                    v_text_m_HB.append(a)
                    v_text_m_HB.append(b)
                c="Mom at sup " + str(i+1)
                v_text_m_HB.append(c)
                d_r_text_HB_pin[T_E]=v_text_m_HB

                ###### SHR1 #####
                v_text_m_SHR=[]
                i=1
                nciclos=int(len(d_r_SHR1_pin[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Span " + str(i) + " left end"
                    b="Span " + str(i) + " right end"
                    v_text_m_SHR.append(a)
                    v_text_m_SHR.append(b)

                d_r_text_SHR_pin[T_E]=v_text_m_SHR


                fail=0
                caution=0
                for x in d_r_d_result_HB_pin[T_E]:
                    if (d_r_d_result_HB_pin[T_E][x]=='FAIL'):
                        fail=1
                    elif (d_r_d_result_HB_pin[T_E][x]=='CAUTION'):
                        caution=1
                for x in d_r_d_result_SHR_pin[T_E]:
                    if (d_r_d_result_SHR_pin[T_E][x]=='FAIL'):
                        fail=1
                    elif (d_r_d_result_SHR_pin[T_E][x]=='CAUTION'):
                        caution=1
                if fail==1:
                    d_current_status_pin[T_E]="FAIL"
                elif caution==1:
                    d_current_status_pin[T_E]="CAUTION"
                else:
                    d_current_status_pin[T_E]="OK"


                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(12)
                MaxMoveMomHB=np.zeros((100,7))
                MaxMoveMomHB11=np.zeros((100,7))
                MaxMoveMomHB22=np.zeros((100,7))        
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))
                OpeninFlag=0

                #####botones#####3
                OPTlhfixed=1
                OPTlhpin=0
                OPTrhfixed=1
                OPTrhpin=0
                
                workssheetLB3coma2masI=np.zeros(31)

                PREPARE_CALCS()

                if(HB_or_SV=="HB"):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
                elif(HB_or_SV=='SV'):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]
                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(32)
                MaxMoveMomHB=np.zeros((100,7))
                MaxMoveMomHB22=np.zeros((100,7))        
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))
                OpeninFlag=0            
                workssheetLB3coma2masI=np.zeros(31)

                PREPARE_CALCS()
                MaxMoveMomHB2,MaxMoveShrHB2=Load_Axles_AIL()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]
                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]
            
                HB1_fix, SHR1_fix, HB2_fix, SHR2_fix, d_result_HB_fix, d_result_SHR_fix=comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11, MaxMoveShrHB22)

                d_r_HB1_fix[T_E]=HB1_fix
                d_r_SHR1_fix[T_E]=SHR1_fix
                d_r_HB2_fix[T_E]=HB2_fix
                d_r_SHR2_fix[T_E]=SHR2_fix
                d_r_d_result_HB_fix[T_E]=d_result_HB_fix
                d_r_d_result_SHR_fix[T_E]=d_result_SHR_fix

                ##################################### RETURN VALUES ########################            
                ######## HB1 ########
                v_text_m_HB=[]
                i=1           
                nciclos=int(len(d_r_HB1_fix[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Mom at sup " + str(i)
                    b="Mom at span " + str(i)
                    v_text_m_HB.append(a)
                    v_text_m_HB.append(b)
                c="Mom at sup " + str(i+1)
                v_text_m_HB.append(c)
                d_r_text_HB_fix[T_E]=v_text_m_HB


                ###### SHR1 #####
                v_text_m_SHR=[]
                i=1
                nciclos=int(len(d_r_SHR1_pin[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Span " + str(i) + " left end"
                    b="Span " + str(i) + " right end"
                    v_text_m_SHR.append(a)
                    v_text_m_SHR.append(b)

                d_r_text_SHR_fix[T_E]=v_text_m_SHR


                fail=0
                caution=0
                for x in d_r_d_result_HB_fix[T_E]:
                    if (d_r_d_result_HB_fix[T_E][x]=='FAIL'):
                        fail=1
                    elif (d_r_d_result_HB_fix[T_E][x]=='CAUTION'):
                        caution=1

                for x in d_r_d_result_SHR_fix[T_E]:
                    if (d_r_d_result_SHR_fix[T_E][x]=='FAIL'):
                        fail=1
                    elif (d_r_d_result_SHR_fix[T_E][x]=='CAUTION'):
                        caution=1
                if fail==1:
                    d_current_status_fix[T_E]="FAIL"
                elif caution==1:
                    d_current_status_fix[T_E]="CAUTION"
                else:
                    d_current_status_fix[T_E]="OK"


                fail_hb=0
                fail_shr=0
                fail=0
                caution_hb=0
                caution_shr=0
                caution=0
                for x in d_r_d_result_HB_pin[T_E]:
                    if (d_r_d_result_HB_pin[T_E][x]=='FAIL'):
                        fail=1
                        fail_hb=1
                    elif (d_r_d_result_HB_pin[T_E][x]=='CAUTION'):
                        caution=1
                        caution_hb=1

                for x in d_r_d_result_HB_fix[T_E]:
                    if (d_r_d_result_HB_fix[T_E][x]=='FAIL'):
                        fail=1
                        fail_hb=1
                    elif (d_r_d_result_HB_fix[T_E][x]=='CAUTION'):
                        caution=1
                        caution_hb=1

                if fail_hb==1:
                    d_current_status_hb[T_E]="FAIL"
                elif caution_hb==1:
                    d_current_status_hb[T_E]="CAUTION"
                else:
                    d_current_status_hb[T_E]="OK"


                for x in d_r_d_result_SHR_pin[T_E]:
                    if (d_r_d_result_SHR_pin[T_E][x]=='FAIL'):
                        fail=1
                        fail_shr=1
                    elif (d_r_d_result_SHR_pin[T_E][x]=='CAUTION'):
                        caution=1
                        caution_shr=1
                for x in d_r_d_result_SHR_fix[T_E]:
                    if (d_r_d_result_SHR_fix[T_E][x]=='FAIL'):
                        fail=1
                        fail_shr=1
                    elif (d_r_d_result_SHR_fix[T_E][x]=='CAUTION'):
                        caution=1
                        caution_shr=1
                if fail_shr==1:
                    d_current_status_shr[T_E]="FAIL"
                elif caution_shr==1:
                    d_current_status_shr[T_E]="CAUTION"
                else:
                    d_current_status_shr[T_E]="OK"

                if (fail_hb==1 or fail_shr==1):
                    d_current_status[T_E]='FAIL'
                elif (caution_hb==1 or caution_shr==1):
                    d_current_status[T_E]='CAUTION'
                else:
                    d_current_status[T_E]='OK'


                if (Factored==1):
                    d_calc_type[T_E]='Factored'
                elif (NoOF==1):
                    d_calc_type[T_E]='NoOF'
                elif (NoDF==1):
                    d_calc_type[T_E]='NoDF'
                elif (NoFact==1):
                    d_calc_type[T_E]='NoFact'


            if(St_type=="3"):     
                d_estructure_Type_convert[T_E]='Simply-Supported'
                Simply_Supported=1
                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(32)
                MaxMoveMomHB=np.zeros((100,7))
                MaxMoveMomHB11=np.zeros((100,7))
                MaxMoveMomHB22=np.zeros((100,7))        
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))
                OpeninFlag=0
                #####botones#####
                OPTlhfixed=0
                OPTlhpin=1
                OPTrhfixed=0
                OPTrhpin=1
                Factored=1
                NoOF=0
                NoDF=0
                NoFact=0
                #################        
                workssheetLB3coma2masI=np.zeros(31)

                PREPARE_CALCS()
                v_HB1, v_SHR1, v_HB2, v_SHR2, v_d_result_HB, v_d_result_SHR=CALC_SS_HB_AIL() 

                d_r_HB1[T_E]=v_HB1
                d_r_SHR1[T_E]=v_SHR1
                d_r_HB2[T_E]=v_HB2
                d_r_SHR2[T_E]=v_SHR2
                d_r_d_result_HB[T_E]=v_d_result_HB
                d_r_d_result_SHR[T_E]=v_d_result_SHR   
                fail=0
                fail_hb=0
                fail_shr=0

                caution=0
                caution_hb=0
                caution_shr=0
                for x in range(0,len(d_r_d_result_HB[T_E])):
                    for xx in range(0,len(d_r_d_result_HB[T_E][x])):
                        if (d_r_d_result_HB[T_E][x][xx]=='FAIL'):
                            fail=1
                            fail_hb=1
                        elif (d_r_d_result_HB[T_E][x][xx]=='CAUTION'):
                            caution=1
                            caution_hb=1

                if fail_hb==1:
                    d_current_status_hb[T_E]="FAIL"
                elif caution_hb==1:
                    d_current_status_hb[T_E]="CAUTION"
                else:
                    d_current_status_hb[T_E]="OK"


                for x in range(0,len(d_r_d_result_SHR[T_E])):
                    for xx in range(0,len(d_r_d_result_SHR[T_E][x])):
                        if (d_r_d_result_SHR[T_E][x][xx]=='FAIL'):
                            fail=1
                            fail_shr=1
                        elif (d_r_d_result_SHR[T_E][x][xx]=='CAUTION'):
                            caution=1
                            caution_shr=1

                if fail_shr==1:
                    d_current_status_shr[T_E]="FAIL"
                elif caution_shr==1:
                    d_current_status_shr[T_E]="CAUTION"
                else:
                    d_current_status_shr[T_E]="OK"


                if fail==1:
                    d_current_status[T_E]="FAIL"
                elif caution==1:
                    d_current_status[T_E]="CAUTION"
                else:
                    d_current_status[T_E]="OK"


                #################################  RETURN  VALUES  ########################
                ###### HB1 #####
                v_text_m_HB=[]
                i=1

                for y in range(0,len(d_r_HB1[T_E])):  
                    nciclos=int(len(d_r_HB1[T_E][y])/2)
                    for i in range(1,nciclos+1):
                        a="Mom at sup " + str(y+1)
                        b="Mom at span " + str(y+1)
                        v_text_m_HB.append(a)
                        v_text_m_HB.append(b)
                    c="Mom at sup " + str(y+1+1)
                    v_text_m_HB.append(c)
                    d_r_text_m_HB[str(y)]=v_text_m_HB
                    v_text_m_HB=[]

                d_r_text_HB[T_E]=d_r_text_m_HB
                d_r_text_m_HB={}

                ###### SHR1 #####
                v_text_m_SHR=[]
                i=1
                for y in range(0,len(d_r_SHR1[T_E])):             
                    nciclos=int(len(d_r_SHR1[T_E][y])/2)
                    for i in range(1,nciclos+1):
                        a="Span " + str(y+1) + " left end"
                        b="Span " + str(y+1) + " right end"
                        v_text_m_SHR.append(a)
                        v_text_m_SHR.append(b)
                    d_r_text_m_SHR[str(y)]=v_text_m_SHR
                    v_text_m_SHR=[]

                d_r_text_SHR[T_E]=d_r_text_m_SHR
                d_r_text_m_SHR={}


                if (Factored==1):
                    d_calc_type[T_E]='Factored'
                elif (NoOF==1):
                    d_calc_type[T_E]='NoOF'
                elif (NoDF==1):
                    d_calc_type[T_E]='NoDF'
                elif (NoFact==1):
                    d_calc_type[T_E]='NoFact'

            if(St_type=="4"):
                d_estructure_Type_convert[T_E]='Half-Joint'
                OPTlhfixed=0
                OPTlhpin=1
                OPTrhfixed=0
                OPTrhpin=1 
                Factored=1
                NoOF=0
                NoDF=0
                NoFact=0

                PREPARE_CALCS()
                if(HB_or_SV=="HB"):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_HB_Fact()
                elif(HB_or_SV=='SV'):
                    MaxMoveMomHB1,MaxMoveShrHB1=Load_Vehicle_SV_Fact()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB11[I, J] = MaxMoveMomHB1[I, J]

                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB11[I, J] = MaxMoveShrHB1[I, J]

                L=np.zeros(31)
                EIStrt=np.zeros(31)
                Lleft=np.zeros(31)
                EI=np.zeros(31)
                KEI=np.zeros((31,3))
                FEM=np.zeros((31,3))
                Vehicle=np.zeros((51,3))
                Loadin=np.zeros((6,101))
                FEM1=np.zeros((31,3))
                FEM2=np.zeros((31,3))
                Rv=np.zeros(32)
                MaxMoveMomHB=np.zeros((100,7))
                MaxMoveShrHB=np.zeros((100,6))
                workssheetLB6coma2masI=np.zeros(31)
                MaxMoveMom=np.zeros((100,4))
                MaxMoveShr=np.zeros((100,3))
                OpeninFlag=0########?????        
                workssheetLB3coma2masI=np.zeros(31)

                PREPARE_CALCS()
                MaxMoveMomHB2, MaxMoveShrHB2=Load_Axles_AIL()

                for I in range(1, 100):
                    for J in range(1, 7):
                        MaxMoveMomHB22[I, J] = MaxMoveMomHB2[I, J]

                for I in range(1, 100):
                    for J in range(1, 6):
                        MaxMoveShrHB22[I, J] = MaxMoveShrHB2[I, J]


                HB1, SHR1, HB2, SHR2, d_result_HB, d_result_SHR = comparative(MaxMoveMomHB11, MaxMoveMomHB22,MaxMoveShrHB11,MaxMoveShrHB22)

                d_r_HB1[T_E]=HB1
                d_r_SHR1[T_E]=SHR1
                d_r_HB2[T_E]=HB2
                d_r_SHR2[T_E]=SHR2
                d_r_d_result_HB[T_E]=d_result_HB
                d_r_d_result_SHR[T_E]=d_result_SHR

                ##################################### RETURN VALUES ########################            
                ######## HB1 ########
                v_text_m_HB=[]
                i=1           
                nciclos=int(len(d_r_HB1[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Mom at sup " + str(i)
                    b="Mom at span " + str(i)
                    v_text_m_HB.append(a)
                    v_text_m_HB.append(b)
                c="Mom at sup " + str(i+1)
                v_text_m_HB.append(c)
                d_r_text_HB[T_E]=v_text_m_HB

                ###### SHR1 #####
                v_text_m_SHR=[]
                i=1
                nciclos=int(len(d_r_SHR1[T_E])/2)
                for i in range(1,nciclos+1):
                    a="Span " + str(i) + " left end"
                    b="Span " + str(i) + " right end"
                    v_text_m_SHR.append(a)
                    v_text_m_SHR.append(b)

                d_r_text_SHR[T_E]=v_text_m_SHR
                ##################################### END RETURN VALUES ######################## 
                ##IF COUNTINOUS WORKS##    DO JUST ONE SIMPLY SUPPORTED

                fail=0
                fail_hb=0
                fail_shr=0
                fallaContinouos=0
                caution=0
                caution_hb=0
                caution_shr=0
                for x in d_r_d_result_HB[T_E]:
                    if (d_r_d_result_HB[T_E][x]=='FAIL'):
                        fail=1
                        fail_hb=1
                    elif (d_r_d_result_HB[T_E][x]=='CAUTION'):
                        caution=1
                        caution_hb=1
                for x in d_r_d_result_SHR[T_E]:
                    if (d_r_d_result_SHR[T_E][x]=='FAIL'):
                        fail=1
                        fail_shr=1
                    elif (d_r_d_result_SHR[T_E][x]=='CAUTION'):
                        caution=1
                        caution_shr=1


                if fail_hb==1:
                    d_current_status_hb[T_E]='FAIL'
                elif caution_hb==1:
                    d_current_status_hb[T_E]='CAUTION'
                else:
                    d_current_status_hb[T_E]='OK'

                if fail_shr==1:
                    d_current_status_shr[T_E]='FAIL'
                elif caution_shr==1:
                    d_current_status_shr[T_E]='CAUTION'
                else:
                    d_current_status_shr[T_E]='OK'


                if (fail==0):
                    d_fallaContinouos[T_E]='OK'
                    HB1_hjs, SHR1_hjs, HB2_hjs, SHR2_hjs, d_result_HB_hjs, d_result_SHR_hjs=HalfJointedSpan(HB_or_SV)
                else:
                    fallaContinouos=1
                    d_fallaContinouos[T_E]='FAIL'

        
                if (fail==0 and valid_data==1):
                    d_r_HB1_hjs[T_E]=HB1_hjs
                    d_r_SHR1_hjs[T_E]=SHR1_hjs 
                    d_r_HB2_hjs[T_E]=HB2_hjs
                    d_r_SHR2_hjs[T_E]=SHR2_hjs
                    d_r_d_result_HB_hjs[T_E]=d_result_HB_hjs
                    d_r_d_result_SHR_hjs[T_E]=d_result_SHR_hjs

                    ##################################### RETURN VALUES ########################            
                    ######## HB1 ########
                    v_text_m_HB=[]
                    i=Ldds_position-1       
                    nciclos=int(len(d_r_HB1_hjs[T_E])/2)
                    for i in range(Ldds_position-1, Ldds_position-1 + nciclos):
                        a="Mom at sup " + str(i)
                        b="Mom at span " + str(i)
                        v_text_m_HB.append(a)
                        v_text_m_HB.append(b)
                    c="Mom at sup " + str(i+1)
                    v_text_m_HB.append(c)

                    d_r_text_HB_hjs[T_E]=v_text_m_HB


                    ###### SHR1 #####
                    v_text_m_SHR=[]
                    i=Ldds_position-1
                    nciclos=int(len(d_r_SHR1_hjs[T_E])/2)
                    for i in range(Ldds_position-1, Ldds_position-1 + nciclos):
                        a="Span " + str(i) + " left end"
                        b="Span " + str(i) + " right end"
                        v_text_m_SHR.append(a)
                        v_text_m_SHR.append(b)

                    d_r_text_SHR_hjs[T_E]=v_text_m_SHR
                    

                    #### if ok, fail o caution
                    fail_hjs=0
                    fail_hb_hjs=0
                    fail_shr_hjs=0

                    caution_hjs=0
                    caution_hb_hjs=0
                    caution_shr_hjs=0
                    for x in d_r_d_result_HB_hjs[T_E]:
                        if (d_r_d_result_HB_hjs[T_E][x]=='FAIL'):
                            fail_hjs=1
                            fail_hb_hjs=1
                        elif (d_r_d_result_HB_hjs[T_E][x]=='CAUTION'):
                            caution_hjs=1
                            caution_hb_hjs=1

                    for x in d_r_d_result_SHR_hjs[T_E]:
                        if (d_r_d_result_SHR_hjs[T_E][x]=='FAIL'):
                            fail_hjs=1
                            fail_shr_hjs=1
                        elif (d_r_d_result_SHR_hjs[T_E][x]=='CAUTION'):
                            caution_hjs=1
                            caution_shr_hjs=1

                    if fail_hjs==1:
                        d_current_status[T_E]="FAIL"
                    elif caution_hjs==1 or caution==1:
                        d_current_status[T_E]="CAUTION"
                    else:
                        d_current_status[T_E]="OK"


                    if fail_hb_hjs==1:
                        d_current_status_hb_hjs[T_E]='FAIL'
                    elif caution_hb_hjs==1:
                        d_current_status_hb_hjs[T_E]="CAUTION"
                    else:
                        d_current_status_hb_hjs[T_E]="OK"


                    if fail_shr_hjs==1 :
                        d_current_status_shr_hjs[T_E]='FAIL'
                    elif caution_shr_hjs==1:
                        d_current_status_shr_hjs[T_E]="CAUTION"
                    else:
                        d_current_status_shr_hjs[T_E]="OK"              

                else:
                    d_current_status[T_E]="FAIL"



                if (Factored==1):
                    d_calc_type[T_E]='Factored'
                elif (NoOF==1):
                    d_calc_type[T_E]='NoOF'
                elif (NoDF==1):
                    d_calc_type[T_E]='NoDF'
                elif (NoFact==1):
                    d_calc_type[T_E]='NoFact'

            
        notice_reference=notice_reference[0]
        vehicle_assessed=vehicle_assessed[0]
        
        global_fail=0
        global_caution=0

        for x in range(1,total_structures+1):
            if (d_current_status[x]=='FAIL'):
                global_fail=1
            elif (d_current_status[x]=='CAUTION'):
                global_caution=1
        if global_fail==1:
            global_status='FAIL'
        elif global_caution==1:
            global_status='CAUTION'
        else:
            global_status='OK'


        namejson=writejson()

        matrix_output=[[None for c in range(5)] for r in range(total_structures)]
        i=-1
        for key in d_StructureKey:
            i=i+1
            matrix_output[i][0]=key
            matrix_output[i][1]=d_StructureKey[key]

        i=-1
        for key in d_current_status:
            i=i+1
            matrix_output[i][2]=d_current_status[key]
        i=-1
        for key in d_comments:
            i=i+1
            matrix_output[i][3]=d_comments[key]
        i=-1
        for key in d_ESRN:
            i=i+1
            matrix_output[i][4]=d_ESRN[key]



        jsonDatabase_Summaryvariables()
        jsonDatabase_ResultAllvariables()

        ### Database for errors #########
        data_json={}
        esdalstructureresults={}

        if unable_to_assess_one_or_more_structures==1:
            for i in range(1,total_structures+1):
                str_current_status= d_current_status[i]   
                if(d_comments[i] != "Lorem ipsum dolor"):
                    string_d_comments=d_comments[i]
                    esdalstructureresults['EsdalStructure ' + str(i)] = []
                    esdalstructureresults['EsdalStructure ' + str(i)].append({        
                    "StructureKey":StructureKey[i-1],
                    "assessment comments":string_d_comments,
                })

            
            strig_unable_to_assess_one_or_more_structures="Unable to assess one or more structures"
            
            data_json['properties'] = []
            data_json['properties'].append({
            "movement_id":notice_reference,
            #"global result": global_status,
            "global comments":strig_unable_to_assess_one_or_more_structures,
            })

            data_json["id"]=notice_reference

            data_json['properties'].append(esdalstructureresults)
            collection_errors.insert_one(data_json)

        return namejson

    except:
        print("INPUT JSON FAIL")
        matrix_output=[[None for c in range(4)] for r in range(1)]
        global_status='FAIL'

        ### Database for errors #########
        data_json={}
        data_json['properties'] = []
        data_json['properties'].append({
        "global comments":"Unable to perform assessment - Invalid json schema",
        })       

        collection_errors.insert_one(data_json)

        data_json={}
        dateTimeObj = datetime.now()

        string_d_comments='E001'

        data_json['properties'] = []
        data_json['properties'].append({   
            #"timestamp": timestamp[0],
            "timestamp_finish":str(dateTimeObj),
            "global_result": 'FAIL',
            "global_comments":string_d_comments,
        })

    
        with open('jsonError.json', 'w') as outfile:
            json.dump(data_json, outfile , indent=4)

        return 1

    
        return render(request, 'summary.html',{'matrix_output':matrix_output,'global_status':global_status})

def start(manual_input):
    global threads2
    global threads
    pid = os.getpid()

    if manual_input=='False':
        sequence_number_count=0
        while(True):
            
            sequence_number= 'sequence_number='+str(sequence_number_count)
            # print("############ SECUENCE NUMBER #################")
            # print(sequence_number)
            # print("############################################")
            request_url = '/api/assessment/v1/?'+sequence_number

            try:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile=certificate_file, keyfile=certificate_secret)
                connection = http.client.HTTPSConnection(host, port=443, context=context)
                connection.request(method="GET", url=request_url)
                response = connection.getresponse()
                if (response.status==200 and response.reason=='OK'):
                    data=bytes.decode(response.read(), 'utf-8')
                    rrr=json.loads(data)

                    sequence_number_count=sequence_number_count+1
                    with open('inputjson.json', 'w') as outfile:
                        json.dump(rrr, outfile)
                    
                    datatext=calculate('inputjson.json') #datatext=write json name if ok   #datatext=1 if error
                    
                    if datatext!=1:    
                        data='/app/' + datatext
                        with open(data) as outfile:
                            data = json.load(outfile)
                            json_data = json.dumps(data)
                            headers_req={'Content-Type': 'application/json'}
                            try: 
                                request_url_upload='/uploader'
                                connection = http.client.HTTPSConnection(host, port=443, context=context)
                                connection.request('PUT', request_url_upload, json_data, headers_req)
                                response2=connection.getresponse()
                                print("_______response________")
                                print(response2.read().decode())
                            except ConnectionError:
                                print("NO CONNECTION")
                    else:
                        data='/app/jsonError.json'
                        with open(data) as outfile:
                            data = json.load(outfile)
                            json_data = json.dumps(data)
                            try: 
                                request_url_upload='/uploader'
                                connection = http.client.HTTPSConnection(host, port=443, context=context)
                                connection.request('PUT', request_url_upload, json_data)
                                response2=connection.getresponse()
                                print("_______response2________")
                                print(response2.read().decode())
                            except ConnectionError:
                                print("NO CONNECTION")
                    
                    sequence_number_count=sequence_number_count+1
                else:
                    print("NO CONNECTION")
                    time.sleep(10)
            except:
                print("NO CONNECTION")
                time.sleep(10)
    elif manual_input == 'True':
        datatext=calculate('outputampliacion.json') #datatext=write json name if ok   #datatext=1 if error
        os.kill(pid, 9)
    
    return 0



def gotocreatejsonmodule(request):
    return render(request, 'ManualInput.html')

def create_dict_json(movement_id, ConfigurationSummary, v_de_v_AxleWeight, v_de_v_Axlespacing, Distance_following, structures):
    dateTimeObj = datetime.now()
    data={}
    

    data['$id']="https://esdalurl/schemas/assessment.json"
    data['title']="assessment"
    data['type']="object"
    data['definitions']={}
    data['schema']="http://json-schema.org/draft-07/schema#"
    
    data_properties={}
    data_properties['movement_id']=movement_id
    data_properties['timestamp']=str(dateTimeObj)
    data_properties['sequence_number']=0

    ################ VEHICLES ###################

    data_vehicles={}

    #   ------ConfigurationSummaryListPosition------
    data_vehicles_ConfigurationSummaryListPosition={}
    data_vehicles_ConfigurationSummaryListPosition['ConfigurationSummary']=ConfigurationSummary
    data_vehicles_ConfigurationSummaryListPosition['ConfigurationComponentsNo']=len(v_de_v_AxleWeight)

    #  -------Configuration------
    data_vehicles_Configuration={}
    data_vehicles_ComponentListPosition = {}
    data_vehicles_Component_vector = []

    d_AxleWeight={}
    v_AxleWeight=[]
    d_AxleWeightListPosition = {}


    v_AxleSpacing = []
    d_AxleSpacingListPosition = {}

    #       ---------AxleConfiguration-----------
    vector_allVehicledata = []
    
    for vectorposition in range(len(v_de_v_AxleWeight)):
        data_vehicles_Component_dict = {}
        
        data_vehicles_Component_dict['Longitude'] = vectorposition+1

        data_vehicles_Component_AxleConfiguration = {}
        count_Axles = 0
        for x in v_de_v_AxleWeight[vectorposition]:
            count_Axles += int(x['AxleCount'])
        data_vehicles_Component_AxleConfiguration['NumberOfAxles'] = count_Axles

            #   Weight
        v_AxleWeight = v_de_v_AxleWeight[vectorposition]
        d_AxleWeightListPosition['AxleWeight'] = v_AxleWeight
        
        data_vehicles_Component_AxleConfiguration['AxleWeightListPosition'] = d_AxleWeightListPosition
               
            #   Spacing
        v_AxleSpacing = v_de_v_Axlespacing[vectorposition]
        d_AxleSpacingListPosition['AxleSpacing'] = v_AxleSpacing
        data_vehicles_Component_AxleConfiguration['AxleSpacingListPosition'] = d_AxleSpacingListPosition    
            #   Distance to following       
        try:
            data_vehicles_Component_AxleConfiguration['AxleSpacingToFollowing'] = float(Distance_following[vectorposition])
        except:
            data_vehicles_Component_AxleConfiguration['AxleSpacingToFollowing'] = 0
                

        data_vehicles_Component_dict['AxleConfiguration']=data_vehicles_Component_AxleConfiguration


        data_vehicles_Component_vector.append(copy.deepcopy(data_vehicles_Component_dict))


    

    #------------------------------------------------------------------------------------
                
    data_vehicles_ComponentListPosition_Components = {}
    data_vehicles_ComponentListPosition_Components['Component'] = data_vehicles_Component_vector
    data_vehicles_ComponentListPosition['ComponentListPosition'] = data_vehicles_ComponentListPosition_Components
    
    data_vehicles_Configuration['ConfigurationSummaryListPosition']=data_vehicles_ConfigurationSummaryListPosition

    data_vehicles_Configuration['Configuration'] = data_vehicles_ComponentListPosition

    data_properties['Vehicles'] = data_vehicles_Configuration




    v_EsdalStructure=[]
    for struct in structures:
        json_OneSingleStructure=get_data_structure(struct)
        if (json_OneSingleStructure!=None):
            v_EsdalStructure.append(json_OneSingleStructure)
    data_properties['EsdalStructure'] = v_EsdalStructure


    data['properties']=data_properties  

    datatext='/app/outputampliacion.json'
    with open(datatext, 'w') as outfile:
        json.dump(data, outfile, indent=4)



    return 0


def dict_json_vehicle_weight(v_AxleWeight):

    data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_vector=[]
    data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_dict={}
    for count, value in v_AxleWeight:
        if count != 0:
            data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_dict['AxleCount'] = count
            data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_dict['value'] = value
            data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_vector.append(data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_dict)
            data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_dict = {}
        else:
            break
    return data_vehicles_Component_AxleConfiguration_AxleWeightListPosition_AxleWeight_vector

def dict_json_vehicle_spacing(v_Axlespacing):

    data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_vector = []
    data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_dict = {}
    for count, value in v_Axlespacing:
        if count != 0:
            data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_dict['AxleCount'] = count
            data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_dict['value'] = value
            data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_vector.append(data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_dict)
            data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_dict = {}
        else:
            break
    return data_vehicles_Component_AxleConfiguration_AxleSpacingListPosition_AxleSpacing_vector

def get_vehicleData_vectors_ordenados(v_noordenados):
    
    element_old = -1
    count_element_repetidos = 0
    v_element=np.zeros((10,2))
    v_AxleWeight_index = 0
    count_element = 0



    for element in v_noordenados:
        element_actual=element
        if element_actual==element_old:
            count_element_repetidos += 1
        elif element_actual!=element_old and count_element>0:
            v_element[v_AxleWeight_index, 0] = count_element_repetidos+1
            v_element[v_AxleWeight_index, 1] = element_old
            v_AxleWeight_index += 1
            count_element_repetidos = 0
            element_old = element_actual
            
        element_old=element_actual
        count_element+=1


    try:
        v_element[v_AxleWeight_index, 0] = count_element_repetidos+1
        v_element[v_AxleWeight_index, 1] = element_actual

    except:
        pass
        

    
    return v_element

def get_vehicleData_vectors_noordenados(vehicle_data):
    
    v_weight_noordenados=[]
    v_spacing_noordenados=[]

    for line in vehicle_data.splitlines():
        try:
            int(line.strip()[0])
            new_line_split=line.split("\t")
            if int(new_line_split[0])==1 and int(new_line_split[1])==2 and int(new_line_split[2])==3:
                pass
            else:
                linessplitbyspace=line.strip().split("\t")
                v_weight_noordenados.append(int(linessplitbyspace[2]))

                try:
                    v_spacing_noordenados.append(float(linessplitbyspace[3]))
                except:
                    Axle_spacing=0
        except:
            pass

    return v_weight_noordenados, v_spacing_noordenados


def create_json_estructures(ESRN, StructureKey, StructureType, skew_angle, AxleWeight, GrossWeight, DoubleAxleWeight, TripleAxleWeight, HB_RATING_WITH_LOAD, HB_RATING_WITHOUT_LOAD, VEHICLE_TYPE, SV_RES_WITH_LOAD, SV_RES_MINUS_LOAD, SEQ_NO, SEQ_POS, LEN, STRUCT_TYPE1, STRUCT_TYPE2, STRUCT_TYPE3, CONSTRUCTION_TYPE1, CONSTRUCTION_TYPE2, CONSTRUCTION_TYPE3 ):
    
    v_spans=[]
    d_spans={}
    d_SpanPosition={}
    d_LoadRating={}
    d_UnderbridgeSection={}
    v_SVParameters=[]
    d_SVParameters={}
    d_UnderbridgeSections={}
    d_EsdalStructure={}

    #print("-------------- ESTRUCTURES ---------------")

    for pos in range(len(SEQ_POS)):
        ## spans ###
        try:
            d_spans['SpanNumber']=int(SEQ_POS[pos])
        except:
            d_spans['SpanNumber']=int(0)
        try:
            d_spans['Length']=float(LEN[pos])
        except:
            d_spans['Length']=float(0)
        if STRUCT_TYPE1[pos] != None:
            d_spans['StructureType']=STRUCT_TYPE1[pos]
        else:
            if STRUCT_TYPE2[pos] != None:
                d_spans['StructureType']=STRUCT_TYPE2[pos]
            else:
                if STRUCT_TYPE3[pos] != None:
                    d_spans['StructureType']=STRUCT_TYPE3[pos]
                else:
                    d_spans['StructureType']="unknown value"

        if CONSTRUCTION_TYPE1[pos] != None:   
            d_spans['Construction']=CONSTRUCTION_TYPE1[pos]
        else:
            if CONSTRUCTION_TYPE2[pos] != None:
                d_spans['Construction']=CONSTRUCTION_TYPE2[pos]
            else:
                if CONSTRUCTION_TYPE3[pos] != None:
                    d_spans['Construction']=CONSTRUCTION_TYPE3[pos]
                else:
                    d_spans['Construction']="unknown value"
        try:
            d_SpanPosition['SequencePosition']=int(SEQ_POS[pos])
        except:
            d_SpanPosition['SequencePosition']=""
        try:
            d_spans['SpanPosition']=d_SpanPosition
        except:
            d_spans['SpanPosition']=""
        d_SpanPosition={}
        v_spans.append(d_spans)
        d_spans={}

    
    ## load rating ##
    if HB_RATING_WITH_LOAD != None:
        d_LoadRating['HBRatingWithLoad']=HB_RATING_WITH_LOAD
        if HB_RATING_WITHOUT_LOAD != None:
            d_LoadRating['HBRatingWithoutLoad']=HB_RATING_WITH_LOAD
        else:
            d_LoadRating['HBRatingWithoutLoad']="unknown value"
    
    # SV PARAMETERS #
    if len(VEHICLE_TYPE)!=0:
        for pos in range(len(VEHICLE_TYPE)):
            d_SVParameters['VehicleType']=VEHICLE_TYPE[pos]
            try:
                d_SVParameters['SVReserveWithLoad']=float(SV_RES_WITH_LOAD[pos])
            except:
                d_SVParameters['SVReserveWithLoad']=float(0)
            try:
                d_SVParameters['SVReserveWithoutLoad']=float(SV_RES_MINUS_LOAD[pos])
            except:
                d_SVParameters['SVReserveWithoutLoad']=float(0)
            v_SVParameters.append(d_SVParameters)
            d_SVParameters={}

        d_LoadRating['SVParameters']=v_SVParameters

    ## SignedWeightConstraints
    
    if AxleWeight != None or GrossWeight != None or DoubleAxleWeight != None or TripleAxleWeight != None:
        d_SignedWeightConstraints={}
        if AxleWeight != None:
            d_SignedWeightConstraints['AxleWeight'] = AxleWeight
        if GrossWeight != None:
            d_SignedWeightConstraints['GrossWeight'] = GrossWeight
        if DoubleAxleWeight != None:
            d_SignedWeightConstraints['DoubleAxleWeight'] = DoubleAxleWeight
        if TripleAxleWeight != None:
            d_SignedWeightConstraints['TripleAxleWeight'] = TripleAxleWeight


    ## UnderbridgeSection ##
    if skew_angle == None:
        d_UnderbridgeSection['SkewAngle']=0
    else:
        d_UnderbridgeSection['SkewAngle']=float(skew_angle)

    try:
        d_UnderbridgeSection['SignedWeightConstraints']=d_SignedWeightConstraints
    except:
        pass
    d_UnderbridgeSection['LoadRating']=d_LoadRating
    d_UnderbridgeSection['Span']=v_spans
    d_LoadRating={}

    ## UnderbridgeSectionSSSSSS ##
    d_UnderbridgeSections['UnderbridgeSection']=d_UnderbridgeSection

    ## EsdalStructurev##
    d_EsdalStructure['ESRN']=ESRN
    d_EsdalStructure['StructureKey']=StructureKey
    d_EsdalStructure['StructureType']=StructureType
    d_EsdalStructure['UnderbridgeSections']=d_UnderbridgeSections

    #print(d_EsdalStructure)

    return d_EsdalStructure

def get_data_structure(struct):
    ##buscar StructureKey
    ESRN=struct


    try:
        select= "SELECT STRUCTURE_ID FROM dbo.STRUCT_DETAILS WHERE STRUCTURE_CODE = '" + ESRN + "'"
        cursor_structure.execute(select)

        StructureKey=""
        for row in cursor_structure:
            for colum in row:
                StructureKey=colum
    except:
        StructureKey=""

    ##buscar STRUCTURE_TYPE
    try:
        select= "SELECT STRUCTURE_TYPE, STRUCTURE_TYPE1, STRUCTURE_TYPE2 FROM dbo.STRUCT_DETAILS WHERE STRUCTURE_ID = " + str(StructureKey) 
        cursor_structure.execute(select)

        for row in cursor_structure:
            for colum in row:
                if colum != None:
                    StructureType=colum
                    break
    except:
        StructureType=""


    ##buscar SKEW_ANGLE
    try:
        select= "SELECT SECTION_ID FROM dbo.STRUCTURE_SPANS WHERE STRUCTURE_ID = " + str(StructureKey) 
        cursor_structure.execute(select)

        cursor_structure1=cursor_structure
        for row in cursor_structure1:
            for colum in row:
                skew_angle_sectionId=colum

        select= "SELECT SKEW_ANGLE FROM dbo.STRUCTURE_SECTIONS WHERE STRUCTURE_ID = " + str(StructureKey) + "AND SECTION_ID = " + str(skew_angle_sectionId)
        cursor_structure.execute(select)
        for row_table2 in cursor_structure:
            for colum in row_table2:
                skew_angle=colum
    except:
        skew_angle=0

    ### SignedWeightConstraints
    AxleWeight=None
    GrossWeight=None
    DoubleAxleWeight=None
    TripleAxleWeight=None
    try:
        select= "SELECT SIGN_SINGLE_AXLE_WEIGHT, SIGN_GROSS_WEIGHT, SIGN_DOUBLE_AXLE_WEIGHT, SIGN_TRIPLE_AXLE_WEIGHT FROM dbo.STRUCTURE_SECTIONS WHERE STRUCTURE_ID = " + str(StructureKey)
        cursor_structure.execute(select)
        for row in cursor_structure:
            try:
                AxleWeight = float(row[0])
            except:
                AxleWeight = None
            try:
                GrossWeight = float(row[1])
            except:
                GrossWeight = None
            try:
                DoubleAxleWeight = float(row[2])
            except:
                DoubleAxleWeight = None
            try:
                TripleAxleWeight = float(row[3])
            except:
                TripleAxleWeight = None
    except:
        pass

    ### HBRatingWithLoad
    try:
        select= "SELECT HB_RATING_WITH_LOAD FROM dbo.STRUCTURE_SECTIONS WHERE STRUCTURE_ID = " + str(StructureKey) + "AND SECTION_ID = " + str(skew_angle_sectionId)
        cursor_structure.execute(select)
        for row_table2 in cursor_structure:
            for colum in row_table2:
                HB_RATING_WITH_LOAD=int(colum)
    except:
        HB_RATING_WITH_LOAD=None

    ##HB_RATING_WITHOUT_LOAD
    try:
        select= "SELECT HB_RATING_WITHOUT_LOAD FROM dbo.STRUCTURE_SECTIONS WHERE STRUCTURE_ID = " + str(StructureKey) + "AND SECTION_ID = " + str(skew_angle_sectionId)
        cursor_structure.execute(select)
        for row_table2 in cursor_structure:
            for colum in row_table2:
                HB_RATING_WITHOUT_LOAD=int(colum)
    except:
        HB_RATING_WITHOUT_LOAD=None


    ##SV_RATING
    try:
        VEHICLE_TYPE=[]
        SV_RES_WITH_LOAD=[]
        SV_RES_MINUS_LOAD=[]
        select= "SELECT VEHICLE_TYPE, SV_RES_WITH_LOAD, SV_RES_MINUS_LOAD FROM dbo.STRUCTURE_SECTION_SV_PARAMS WHERE STRUCTURE_ID = " + str(StructureKey) + "AND SECTION_ID = " + str(skew_angle_sectionId)
        cursor_structure.execute(select)
        for row in cursor_structure:
            VEHICLE_TYPE.append(row[0])
            SV_RES_WITH_LOAD.append(row[1])
            SV_RES_MINUS_LOAD.append(row[2])
    except:
        VEHICLE_TYPE.append("")
        SV_RES_WITH_LOAD.append("")
        SV_RES_MINUS_LOAD.append("")



    #Span
    try:
        SEQ_NO=[]
        SEQ_POS=[]
        LEN=[]
        STRUCT_TYPE1=[]
        STRUCT_TYPE2=[]
        STRUCT_TYPE3=[]
        CONSTRUCTION_TYPE1=[]
        CONSTRUCTION_TYPE2=[]
        CONSTRUCTION_TYPE3=[]
        select= "SELECT SEQ_NO, SEQ_POS, LEN, STRUCT_TYPE1, STRUCT_TYPE2, STRUCT_TYPE3, CONSTRUCTION_TYPE1, CONSTRUCTION_TYPE2, CONSTRUCTION_TYPE3 FROM dbo.STRUCTURE_SPANS WHERE STRUCTURE_ID = " + str(StructureKey) + "AND SECTION_ID = " + str(skew_angle_sectionId)
        cursor_structure.execute(select)
        for row in cursor_structure:
            SEQ_NO.append(row[0])
            SEQ_POS.append(row[1])
            LEN.append(row[2])
            STRUCT_TYPE1.append(row[3])
            STRUCT_TYPE2.append(row[4])
            STRUCT_TYPE3.append(row[5])
            CONSTRUCTION_TYPE1.append(row[6])
            CONSTRUCTION_TYPE2.append(row[7])
            CONSTRUCTION_TYPE3.append(row[8])
    except:
        SEQ_NO.append("")
        SEQ_POS.append("")
        LEN.append("")
        STRUCT_TYPE1.append("")
        STRUCT_TYPE2.append("")
        STRUCT_TYPE3.append("")
        CONSTRUCTION_TYPE1.append("")
        CONSTRUCTION_TYPE2.append("")
        CONSTRUCTION_TYPE3.append("")

    

    try:


        json_OneSingleStructure = create_json_estructures(ESRN, StructureKey, StructureType, skew_angle, AxleWeight, GrossWeight, DoubleAxleWeight,\
                                TripleAxleWeight, HB_RATING_WITH_LOAD, HB_RATING_WITHOUT_LOAD, VEHICLE_TYPE, SV_RES_WITH_LOAD, SV_RES_MINUS_LOAD,\
                                SEQ_NO, SEQ_POS, LEN, STRUCT_TYPE1, STRUCT_TYPE2, STRUCT_TYPE3, CONSTRUCTION_TYPE1, CONSTRUCTION_TYPE2,\
                                CONSTRUCTION_TYPE3)

    except:
        json_OneSingleStructure=None

    



    return json_OneSingleStructure

def createjsonmodule_email(request):
    global threads2
    
    movement_id = request.POST['movement_id_email']
    ConfigurationSummary = request.POST['ConfigurationSummary']
    Axle_Weight = request.POST.getlist('Axle_Weight[]')
    Axle_Spacing = request.POST.getlist('Axle_Spacing[]')
    Distance_following = request.POST.getlist('Distance_following[]')
    Structures = request.POST.getlist('structures[]')



    #######    Weight  #############
    try:
        count=0
        v_split_data=np.zeros((len(Axle_Weight),20))
        v_final_split=[]
        for vehicle_weight in Axle_Weight:
            vehicle_weight_split=vehicle_weight.split(' kg x')
            for new_split in vehicle_weight_split:
                vehicle_weight_split=new_split.split(' , ')
                for final_split in vehicle_weight_split:
                    v_final_split.append(final_split)       
            count2=0    
            for x in v_final_split:
                v_split_data[count][count2]=int(x)
                count2 += 1
            v_final_split=[]
            count += 1

        
        v_de_v_weight=[]
        for vector_number in v_split_data:
            vector_ordenados=np.zeros((10,2))
            count=0
            count_par=0
            for vector_number_element in vector_number:
                if count_par==0:
                    vector_ordenados[count][1]=vector_number_element
                    count_par += 1
                else:
                    vector_ordenados[count][0]=vector_number_element
                    count_par=0
                    count += 1      
            dict_vehicle_weight = dict_json_vehicle_weight(vector_ordenados)
            v_de_v_weight.append(dict_vehicle_weight)
    except:
        v_de_v_weight=[]

    

    #######    SPACING  #############
    try:
        count=0
        v_split_data=np.zeros((len(Axle_Spacing),20))
        v_final_split=[]
        for vehicle_spacing in Axle_Spacing:
            vehicle_spacing_split=vehicle_spacing.split(' m x')
            for new_split in vehicle_spacing_split:
                vehicle_spacing_split=new_split.split(' , ')
                for final_split in vehicle_spacing_split:
                    v_final_split.append(final_split)       
            count2=0    
            for x in v_final_split:
                v_split_data[count][count2]=float(x)
                count2 += 1
            v_final_split=[]
            count += 1

        
        v_de_v_spacing=[]
        for vector_number in v_split_data:
            vector_ordenados=np.zeros((10,2))
            count=0
            count_par=0
            for vector_number_element in vector_number:
                if count_par==0:
                    vector_ordenados[count][1]=vector_number_element
                    count_par += 1
                else:
                    vector_ordenados[count][0]=vector_number_element
                    count_par=0
                    count += 1      
            dict_vehicle_spacing = dict_json_vehicle_spacing(vector_ordenados)
            v_de_v_spacing.append(dict_vehicle_spacing)
    except:
        v_de_v_spacing=[]


    create_dict_json(movement_id, ConfigurationSummary, v_de_v_weight, v_de_v_spacing, Distance_following, Structures)

    
    
    p2 = Process(target=start, args=('True',))
    threads2.append(p2)
    p2.start()

    return render(request, 'ManualInput.html')

def createjsonmodule_esdal(request):
    global threads2

    movement_id = request.POST['movement_id_esdal']
    ConfigurationSummary = request.POST['ConfigurationSummary']
    vehicle_data1 = request.POST.getlist('vehicle_data1[]')
    Distance_following = request.POST.getlist('Distance_following[]')
    Structures = request.POST['structures']


    v_de_v_weight=[]
    v_de_v_spacing=[]

    for vehicle in vehicle_data1:
        v_AxleWeight_noordenados, v_Axlespacing_noordenados = get_vehicleData_vectors_noordenados(vehicle)
        

        v_AxleWeight  = get_vehicleData_vectors_ordenados(v_AxleWeight_noordenados)
        v_Axlespacing  = get_vehicleData_vectors_ordenados(v_Axlespacing_noordenados)



        dict_vehicle_weight = dict_json_vehicle_weight(v_AxleWeight)
        v_de_v_weight.append(dict_vehicle_weight)

        dict_vehicle_spacing = dict_json_vehicle_spacing(v_Axlespacing)
        v_de_v_spacing.append(dict_vehicle_spacing)



    # La estructura es del tipo: "over S-TQ039956-1- Berry Lane Viaduct, over S-SU039956-1- London Lane Viaduct". Separar solo las estructuras de todo 
    # el resto de texto innecesario y meterlos en un vector
    
    Structures_split_spaces=Structures.split("\t\t\r\n")
    

    Structures_split_spaces_2=[]
    for y in Structures_split_spaces:
        Structures_split_spaces_2.append(y.split(" "))
    v_structures=[]
    for x in Structures_split_spaces_2:
        for y in x:
            Structures_split_spaces_and_dash=y.split("-")
            if len(Structures_split_spaces_and_dash)==4:
                v_structures.append(Structures_split_spaces_and_dash[0][-1]+"-"+Structures_split_spaces_and_dash[1]+"-"+Structures_split_spaces_and_dash[2])
            elif len(Structures_split_spaces_and_dash)==3:
                v_structures.append(y)


    create_dict_json(movement_id, ConfigurationSummary, v_de_v_weight, v_de_v_spacing, Distance_following, v_structures)
    p2 = Process(target=start, args=('True',))
    print(threads2)
    threads2.append(p2)
    print(threads2)
    p2.start()

    
    return render(request, 'ManualInput.html')

