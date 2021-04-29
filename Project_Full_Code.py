import matplotlib as mpl
import matplotlib.pyplot as plt
import requests
import pickle
import json
import json
import pandas as pd
import numpy as np
import re

api_url_base = 'https://stat.ripe.net/data/'

''' This function returns the evolution of the number of autonomous systems between starttime and endtime '''
def nb_asn(starttime,endtime):
    url='{}country-routing-stats/data.json?resource=lb&starttime={}&endtime={}&resolution=1w'.format(api_url_base,starttime,endtime)
    response = requests.get(url)
    if response.status_code == 200:
        country_asn_json = json.loads(response.content.decode('utf-8'))
        a = len(country_asn_json["data"]["stats"])
        country_asn_ris_list = [country_asn_json["data"]["stats"][l]["asns_ris"] for l in range(0,a)]
        country_asn_stats_list = [country_asn_json["data"]["stats"][l]["asns_stats"] for l in range(0,a)]
        return country_asn_ris_list, country_asn_stats_list
    else:
        print("error")
#nb_asn('2017-01-16T02:00','2021-04-11T03:00')

''' This function returns a list of the Lebanese autonomous sytems in Lebanon '''
def get_country_asn(country_code, timestamp):
    api_url = '{}country-asns/data.json?resource={}&query_time={}&lod=1'.format(api_url_base, country_code, timestamp)
    response = requests.get(api_url)
    if response.status_code == 200:
        country_asn_json = json.loads(response.content.decode('utf-8'))
        country_asn_list = country_asn_json["data"]["countries"][0]["routed"]
        country_asn_list = re.findall(r'\((.*?)\)', country_asn_list)
        country_asn_stats = country_asn_json["data"]["countries"][0]["stats"]
        return country_asn_list, country_asn_stats
    else:
        return None

''' This function returns the evolution of the average number of transit relations '''
def variation_nei(list_time):
    left=[]
        
    for t in list_time:
        print(t)
        count=0
        liste_asn=get_country_asn("LB",t)[0]
        for asn in liste_asn:
            api_url = '{}asn-neighbours/data.json?resource={}&starttime={}'.format(api_url_base, asn,t) #
            
            asn_neighbours_json1 = requests.get(api_url)
            if (asn_neighbours_json1.status_code == 200):
                asn_neighbours_json = json.loads(asn_neighbours_json1.content.decode('utf-8'))
                count+= int(asn_neighbours_json['data']['neighbour_counts']['left'])
                if int(asn_neighbours_json['data']['neighbour_counts']['left'])==0:
                    print(t.split('-')[0],asn)
        count=count/len(liste_asn)
        left.append(count)
    i=0
    while i<len(left):
        print(list_time[i].split('-')[0]+'-'+list_time[i].split('-')[1],':',left[i])
        i=i+1
    return left
#list_time=["2018-01-01T00:00:00","2018-02-01T00:00:00","2018-03-01T00:00:00","2018-04-01T00:00:00","2018-05-01T00:00:00","2018-06-01T00:00:00","2018-07-01T00:00:00","2018-08-01T00:00:00","2018-09-01T00:00:00","2018-10-01T00:00:00","2018-11-01T00:00:00","2018-12-01T00:00:00","2019-01-01T00:00:00","2019-02-01T00:00:00","2019-03-01T00:00:00","2019-04-01T00:00:00","2019-05-01T00:00:00","2019-06-01T00:00:00","2019-07-01T00:00:00","2019-08-01T00:00:00","2019-09-01T00:00:00","2019-10-01T00:00:00","2019-11-01T00:00:00","2019-12-01T00:00:00","2020-01-01T00:00:00","2020-02-01T00:00:00","2020-03-01T00:00:00","2020-04-01T00:00:00","2020-05-01T00:00:00","2020-06-01T00:00:00","2020-07-01T00:00:00","2020-08-01T00:00:00","2020-09-01T00:00:00","2020-10-01T00:00:00","2020-11-01T00:00:00","2020-12-01T00:00:00","2021-01-01T00:00:00","2021-02-01T00:00:00","2021-03-01T00:00:00"]
#variation_nei(list_time)

''' This function returns two lists containing the evolution of the number of IPv4 and IPv6 prefixes '''
def nb_pref(starttime,endtime):
    url='{}country-routing-stats/data.json?resource=lb&starttime={}&endtime={}&resolution=1w'.format(api_url_base,starttime,endtime)
    response = requests.get(url)
    if response.status_code == 200:
        country_asn_json = json.loads(response.content.decode('utf-8'))
        a = len(country_asn_json["data"]["stats"])
        ipv4_prefixes=[country_asn_json["data"]["stats"][l]["v4_prefixes_ris"] for l in range(0,a)]
        ipv6_prefixes=[country_asn_json["data"]["stats"][l]["v6_prefixes_ris"] for l in range(0,a)]
        return ipv4_prefixes, ipv6_prefixes
    else:
        print("error")
# nb_pref('2014-01-16T02:00','2021-04-11T03:00')

''' This function returns the list of IPv4 prefixes in Lebanon '''
def list_prefixes():
    asn_pref_json1 = requests.get('https://stat.ripe.net/data/ris-prefixes/data.json?resource=42020&list_prefixes=true')
    if (asn_pref_json1.status_code == 200):
        asn_pref_json = json.loads(asn_pref_json1.content.decode('utf-8'))
    l=[]
    for i in asn_pref_json['data']['prefixes']['v4']:
        for j in asn_pref_json['data']['prefixes']['v4'][i]:
            l.append(j)
    return l

''' This function returns the evolution of the number of "Withdraw" BGP updates '''
def withdraw():
    l=list_prefixes()
    res=[0]*13
    for pref in l:
        print(l.index(pref))
        asn_upd_json1 = requests.get('https://stat.ripe.net/data/bgp-update-activity/data.json?resource={}&starttime=2017-01-16T02:00&endtime=2018-01-16T02:00&hide_empty_samples=false'.format(pref))
        if (asn_upd_json1.status_code == 200):
            asn_upd_json = json.loads(asn_upd_json1.content.decode('utf-8'))
        for i in range(0,13):
            res[i]+= int(asn_upd_json['data']['updates'][i]['withdrawals'])
    return res
# withdraw()

''' Boxplot of "Withdraw" updates '''
# res=[326202, 1125258, 502362, 550437, 484494, 385669, 407719, 241963, 389023, 553793, 391002, 341792, 466207, 1284509, 477673, 395832, 400684, 682457, 438539, 489379, 486071, 476242, 1003265, 1573415, 1314072, 702496, 1018705, 854115, 1182532, 693738, 574094, 1641182, 918111, 840262, 705153, 1223847, 1051751, 1199985]
# # res0=[101702, 90337, 217574, 31159, 43123, 207554, 70916, 64421, 295474, 57942, 811778, 90080]
# res1=res[0:12]
# res2=res[12:25]
# res3=res[25:]
# res=[res1,res2,res3]
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# rez=np.array(rez)
# df = pd.DataFrame(np.array(rez),columns=['2018','2019','2020'])
# boxplot = df.boxplot(column=['2018','2019','2020'])
# boxplot = df.boxplot(rot=45, fontsize=10)
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of 'Withdraw' Updates", fontsize=10)
# # df.plot(ylim=(0,1600000))
# plt.ylim(0,1800000)
# plt.show()

''' Boxplot for number of IPv4 prefixes '''
# res=nb_pref('2014-01-16T02:00','2021-04-11T03:00')[0]
# res1=res[0:50]
# res2=res[50:50*2]
# res3=res[50*2:50*3]
# res4=res[50*3:50*4]
# res5=res[50*4:50*5]
# res6=res[50*5:50*6]
# res7=res[50*6:50*7]
# res8=res[50*7:]
# res8=res8+res8
# res=[res1,res2,res3,res4,res5,res6,res7,res8]
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# rez=np.array(rez)
# df = pd.DataFrame(np.array(rez),columns=['2014','2015','2016','2017','2018','2019','2020','2021'])
# boxplot = df.boxplot(column=['2014','2015','2016','2017','2018','2019','2020','2021'])
# boxplot = df.boxplot(rot=45, fontsize=10)
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of IPv4 Prefixes", fontsize=10)
# plt.ylim(0,1600)
# plt.show() 

''' Boxplot for number of IPv6 prefixes '''
# res=nb_pref('2014-01-16T02:00','2021-04-11T03:00')[1]
# res1=res[0:50]
# res2=res[50:50*2]
# res3=res[50*2:50*3]
# res4=res[50*3:50*4]
# res5=res[50*4:50*5]
# res6=res[50*5:50*6]
# res7=res[50*6:50*7]
# res8=res[50*7:]
# res8=res8+res8
# res=[res1,res2,res3,res4,res5,res6,res7,res8]
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# rez=np.array(rez)
# df = pd.DataFrame(np.array(rez),columns=['2014','2015','2016','2017','2018','2019','2020','2021'])
# boxplot = df.boxplot(column=['2014','2015','2016','2017','2018','2019','2020','2021'])
# boxplot = df.boxplot(rot=45, fontsize=10)
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of IPv6 Prefixes", fontsize=10)
# plt.ylim(0,80)
# plt.show() 

''' Boxplot of average transit connections '''
# with open('avg_transit.txt') as f:
#     lines = f.readlines()
# liste_avg=[]
# for i in lines:
#     liste_avg.append(i.split(':')[1])
# k=0
# while k<len(liste_avg):
#     j=liste_avg[k].split()[0] 
#     liste_avg[k]=float(j)      #pour enlever les espaces
#     k+=1
# res=liste_avg
# plt.plot(res)
# plt.show()
# res1=res[0:12]
# res2=res[12:12*2]
# res3=res[12*2:12*3]
# res4=res[12*3:]
# res4=res4*4
# res=[res1,res2,res3,res4]
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# rez=np.array(rez)
# df = pd.DataFrame(np.array(rez),columns=['2018','2019','2020','2021'])
# boxplot = df.boxplot(column=['2018','2019','2020','2021'])
# boxplot = df.boxplot(rot=45, fontsize=10)
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Average Number of Transit Relations Between ASes", fontsize=10)
# plt.ylim(0,1.55)
# plt.show() 

''' Plot number of ASNs '''
# res = nb_asn('2010-01-16T02:00','2021-04-11T03:00')
# res= list(res)
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# df = pd.DataFrame(list(zip( res[0] , res[1] )), index=pd.date_range("1/16/2010","4/11/2021", periods=586), columns=["Routed ASNs","Registered ASNs"])
# df.plot(grid=True,ylim=(0,200))
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of ASNs", fontsize=10)
# plt.show()
# 
''' Plot for number of IPv4 prefixes '''
# res=nb_pref('2014-01-16T02:00','2021-04-11T03:00')[0]
# df = pd.DataFrame(res, index=pd.date_range("1/16/2014","4/11/2021", periods=377))
# df.plot(legend=False,grid=True,ylim=(0,1600))
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of IPv4 Prefixes", fontsize=10)
# plt.show()
 
''' Plot for number of IPv6 prefixes '''
# res=nb_pref('2014-01-16T02:00','2021-04-11T03:00')[1]
# df = pd.DataFrame(res, index=pd.date_range("1/16/2014","4/11/2021", periods=377))
# df.plot(legend=False,grid=True,ylim=(0,80))
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number  of IPv6 Prefixes", fontsize=10)
# plt.show()

'''Plot Number of Secure Internet Servers '''
# res=[83,160,272,339,454,547,592,813,1195,1415,1838]
# df = pd.DataFrame(res, index=pd.date_range("1/01/2010","1/1/2020", periods=len(res)))
# df.plot(legend=False,grid=True,ylim=(0,2000))
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Number of Secure Internet Servers", fontsize=10)
# plt.show()

'''Plot Internet Penetration'''
# res=[43.68,52,61.25,70.5,73,74,76.11,78.2,78.2,78.2,78.2]
# df = pd.DataFrame(res, index=pd.date_range("1/01/2010","1/1/2020", periods=len(res)))
# df.plot(legend=False,grid=True,ylim=(0,80))
# plt.xlabel("Date", fontsize=10)
# plt.ylabel("Individuals using the Internet(% of population)", fontsize=10)
# plt.show()

''' Boxplot Internet Speed '''
# with open('Internet_Speed.txt') as f:
#     lines = f.readlines()
# ul=[]
# dl=[]
# for i in lines:
#     ul.append(i.split()[0])
#     dl.append(i.split()[1])
# del(ul[0])
# del(dl[0])
# k=0
# while k<len(ul):
#     ul[k]=float(ul[k])
#     dl[k]=float(dl[k])
#     k=k+1
# res=[ul,dl]
# rez = [[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
# rez=np.array(rez)
# df = pd.DataFrame(np.array(rez),columns=['Download','Upload'])
# boxplot = df.boxplot(column=['Download','Upload'])
# boxplot = df.boxplot(rot=45, fontsize=10)
# # plt.xlabel("Date", fontsize=10)
# plt.ylabel("Internet Speed (Mbps)", fontsize=10)
# plt.ylim(0,90)
# plt.show()