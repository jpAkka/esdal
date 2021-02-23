def writejson():
    global timestamp
    global d_ESRN
    global global_status
    global unable_to_assess_one_or_more_structures
    global data

    data_json={}
    dateTimeObj = datetime.now()

    
    esdalstructureresults = {}
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
    print(".::::::::::::::::::::::::::::::::::.................")
    print(string_notice_reference)
    datatext=string_notice_reference+'.json'

    with open(datatext, 'w') as outfile:
        json.dump(data_json, outfile , indent=4)

    return datatext













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

    datatext=string_notice_reference+'_recalculate.json'

    with open(datatext, 'w+') as outfile:
        json.dump(data_json, outfile , indent=4)

    return datatext