def start(manual_input):
    global threads2
    global threads
    pid = os.getpid()

    if manual_input=='False':
        sequence_number_count=181
        while(True):
            
            sequence_number= 'sequence_num='+str(sequence_number_count)
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
