#!/usr/bin/env python
import sys
import os
from datetime import date, time, datetime, timedelta
import pprint
import time
import qb
import datetime
import traceback
import copy
import gc
reload(sys).setdefaultencoding('UTF-8')
sys.dont_write_bytecode = True

CURRENT_PATH = os.path.dirname(__file__)+'/../'

REMOVEFLAG = 'remove'
CONFIGURATION_PATH =  CURRENT_PATH + 'conf/conf.txt'
PY_PATH =CURRENT_PATH + 'callback'
LOG_PATH = r"/sw/ple/studio/etc/log/server/qube_wrangler_callback/server_log/"
INTERVALTIME = 10


def clean_data_from_data():
    """This function is used to read configuration and output a list compose parameters that we need"""
    final_data = list()
    sub_data = []
    data = list()
    with open(CONFIGURATION_PATH) as rough_data: #Read data from configuration
        for sub_rough_data in rough_data:
            sub_rough_data = sub_rough_data.split("\n")
            while "" in sub_rough_data:
                sub_rough_data.remove('')
            for sub_rough_data_str in sub_rough_data:
                sub_rough_data_str = sub_rough_data_str.split(":")
            data.append(sub_rough_data_str)
    for sub_data in data:#clean those datas
        sub_dict = {"main":"","condition":"","value":"","method":""}
        for i in range(len(sub_data)):
            if i==0:
                sub_dict["main"] = sub_data[i]

            elif i==1:
                sub_dict["condition"] = sub_data[i]

            elif i == 2:
                sub_dict["value"] = sub_data[i]
            elif i == 3:
                sub_dict["method"] = sub_data[i]
        final_data.append(sub_dict)
    last_list = list()
    for items in final_data:
        if items not in last_list:
            last_list.append(items)
    return last_list

def condition(final_data):#
    condition = list()
    for items in final_data:
        condition.append(items["value"])
    return condition

def serch_data_from_qube(search_seq):
    """"search data from qb.api"""
    rough_result = list()
    for items in search_seq:
        if items["main"] == "Jobinfo":
            if items["condition"] =="status":
                rough_result.append(qb.jobinfo(status = "running"))
                rough_result.append(qb.jobinfo(status = "pending"))
                rough_result.append(qb.jobinfo(status = "blocked"))
                rough_result.append(qb.jobinfo(status = "failed"))
            else :
                raise IOError("Input unsupportable parameter","in cong.text")
        elif items["main"] == "Hostinfo":
            if items["condition"] == "state":
                rough_result.append(qb.hostinfo(state = "active"))
                rough_result.append(qb.hostinfo(state = "panic"))
                rough_result.append(qb.hostinfo(state = "none"))
            else :
                raise IOError("Input unsupportable parameter","in cong.text")
    return rough_result


def clean_search_date(rough_result):
    """Structuring and clean the data from serch_data_from_qube"""
    fina_data = list()
    for sub_rough_result in rough_result:
        for items in sub_rough_result:
            sub_list = {"id":"","user":"","status":"","name":""}
            if type(items) == qb.Job:
                sub_list["id"]= items['id']
                sub_list["user"]= items['user']
                sub_list["status"]= items['status']
                sub_list["name"] = items['name']
                fina_data.append(sub_list)
            elif type(items) == qb.Host:
                sub_list["id"]= items['name']
                sub_list["status"]= items['state']
                sub_list["user"]= "chenrong"
                sub_list["name"] = "WORKER"
                fina_data.append(sub_list)
            else:
                raise ValueError, "can not support this class"
    return fina_data

def compare(new_list,old_list,condition_list):
    """compare two results, if they are different ,run the callback function."""
    result = list()
    rough_result = list()
    sub_list = list()
    
    for older_item in old_list:
        if older_item not in new_list:
            if older_item["name"] == "WORKER":
                rough_result=(qb.hostinfo(name = older_item["id"]))
            else:
                rough_result=(qb.jobinfo(id = older_item["id"]))
            
                if rough_result:
                    pass
                else:
                    rough_result = [qb.Job(data={'id': older_item.get('id'), 'user': older_item.get('user'), 'status': REMOVEFLAG, 'name': older_item.get('name')})]
                
            sub_list.append(rough_result)
            result_list = clean_search_date(sub_list)
            for i in result_list:
                if i["status"] in condition_list:
                    result.append(i)
    clean_list = list()
    for sub_items in result:
        if sub_items not in clean_list:
            clean_list.append(sub_items)
   
    return clean_list


def write_log(usetime,end_time,erros,search_result):
    file_time  = time.strftime('%Y-%m-%d')
    file_name = file_time +".log"
    path =LOG_PATH
    file_path = path+file_name
    #new = open(file_path,"a")
    #new.close()
    with open (file_path,"a") as f:
        f.write("cost time: ")
        f.write(str(usetime))
        f.write(" end time: ")
        f.write(str(end_time))
        f.write("\n")
        if erros:
            f.write(" errors message: ")
            f.write(erros)
            f.write("\n")
        if search_result:
            f.write(" task ")
            f.write(str(search_result))
            f.write("\n")

def run_callback(search_list,final_data):
    """Accronding the configuration, run differernt callback function"""
    fina_list = list()
    clean_list=list()
    for s_items in search_list:
        for f_items in final_data:
            conf_dict={"opeart":"","id":"","status":"","changedTime":"","name":""}
            if s_items["status"] == f_items["value"]:#match the search condition and the search result
                conf_dict["opeart"] = f_items["method"]
                conf_dict["id"] = s_items["id"]
                conf_dict["status"] = s_items["status"]
                conf_dict["changedTime"] = time.strftime('%Y-%m-%d %H:%M:%S')
                conf_dict["name"] =  s_items["name"]
                fina_list.append(conf_dict)
    for items in fina_list:
        if items not in clean_list:
            clean_list.append(items)
    files = os.listdir(PY_PATH)
    files = [f.replace('.py', '') for f in files if f.endswith('.py')]
    for sub_items in clean_list:
        for sub_list in search_list:
            if sub_items["opeart"] in files:
                exec "import %s" %sub_items["opeart"]
                exec "reload( %s )" %sub_items["opeart"]
                exec "%s.main(sub_list)"%sub_items["opeart"]

    return


def runtask(interval_time = INTERVALTIME):#product two list to campare
    print '[%s]' % time.strftime('%Y-%m-%d %H:%M:%S'), 'server started.'
    sys.stdout.flush()
    old_list=[]
    new_list=[]
    while True:

        if old_list:
            time.sleep(interval_time)
            start_time = datetime.datetime.now()
            final_data = clean_data_from_data()
            condition_list = condition(final_data)
            final_data = clean_data_from_data()
            rough_result = serch_data_from_qube(final_data)
            new_list  = clean_search_date(rough_result)

        else:
            final_data = clean_data_from_data()
            rough_result = serch_data_from_qube(final_data)
            old_list  = clean_search_date(rough_result)
            time.sleep(interval_time)
            start_time = datetime.datetime.now()
            condition_list = condition(final_data)
            final_data = clean_data_from_data()
            rough_result = serch_data_from_qube(final_data)
            new_list  = clean_search_date(rough_result)
        erros =""
        search_result = compare(new_list,old_list,condition_list)
        try:
            run_callback(search_result,final_data)
        except:
           erros = traceback.format_exc()

        # remove the value of the older_list,copy the new_list to the older_list,remove the value  of new_list
        old_list = []
        old_list = copy.deepcopy(new_list)
        new_list = []
        end_time = datetime.datetime.now()
        usetime = end_time - start_time
        write_log(usetime,end_time,erros,search_result)

        gc.collect()

runtask()
