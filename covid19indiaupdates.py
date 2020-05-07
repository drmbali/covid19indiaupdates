#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import json
import datetime
import time
from collections import Counter
import requests
from flask import Flask,jsonify


# In[2]:


def zoneData():
    #https://api.covid19india.org/zones.json
    global zonesPanda
    damnationZones=requests.get("https://api.covid19india.org/zones.json")
    districtzones=damnationZones.json()
    zonesD=districtzones.get('zones')
    Zdistrict=[]
    Zstate=[]
    Zlong=[]
    Zlat=[]
    Zzone=[]
    for i in range(len(zonesD)):
        zonedata=zonesD[i]
        dist=zonedata['district']
        pradesh=zonedata['state']
        coordinates=matcher_detailed(dist.lower(),pradesh.lower(),district=True)
        if(coordinates!=0):
            Zdistrict.append(str(dist))
            Zstate.append(str(pradesh))
            Zlong.append(coordinates[0])
            Zlat.append(coordinates[1])
            Zzone.append(str(zonedata['zone']))
        else:
            #print("Not Found: ",dist,pradesh)
            k="who cares"
    zonesPanda['district']=Zdistrict
    zonesPanda['state']=Zstate
    zonesPanda['zone']=Zzone
    zonesPanda['long']=Zlong
    zonesPanda['lat']=Zlat

def matcher_final(pdat_i,pdats_i,district=True):
    global zonesPanda
    key=999999999
    city=False
    for j in range(len(zonesPanda)):
        latlong_district=(zonesPanda['district'][j].strip()).lower()
        latlong_state=(zonesPanda['state'][j].strip()).lower()
        #print("*******************district mode: ON***************************")
        if(fuzz.ratio(pdat_i,latlong_district)>85):
            if(fuzz.ratio(pdats_i,latlong_state)>92):
                key=j
    if(key!=999999999):
        return([zonesPanda['long'][key],zonesPanda['lat'][key]],zonesPanda['zone'][key])
    else:
        return(0,0)

def jsonWriter(dist,state,conf,act,rec,dead,coor,zone):
    global stateCounter,india_totalCases,india_activecases,india_recovered,india_deaths
    if(coor):
        
        g={}
        g['type']="Point"
        g['coordinates']=coor
        
        d={}
        d['updatedOn']=str(datetime.datetime.now().date())
        d['city']=dist
        d['district']=dist
        d['zone']=zone
        d['state']=state
        d['totalConfirmed']=conf
        d['totalActive']=act
        d['totalRecovered']=rec
        d['totalDeaths']=dead
        d['totalIndia']=india_totalCases
        d['activeIndia']=india_activecases
        d['recoveryIndia']=india_recovered
        d['deathsIndia']=india_deaths
        d['statecount']=stateCounter.get(state)
        d['nearbycount']=conf
        
        onerow={}
        onerow['type']='Feature'
        onerow['properties']=d
        onerow['geometry']=g
        
        return onerow


def matcher_detailed(pdat_i,pdats_i,district=True):
    global latLong
    key=999999999
    city=False
    for j in range(len(latLong)):
        latlong_city=(latLong['city1'][j].strip()).lower()
        latlong_district=(latLong['district'][j].strip()).lower()
        latlong_state=(latLong['state'][j].strip()).lower()
        if(city==True):
            #print("*******************city mode: ON***************************")
            if(fuzz.ratio(pdat_i,latlong_city)>85):
                if(fuzz.ratio(pdats_i,latlong_state)>92):
                    key=j
        elif(district==True):
            #print("*******************district mode: ON***************************")
            if(fuzz.ratio(pdat_i,latlong_district)>85):
                if(fuzz.ratio(pdats_i,latlong_state)>92):
                    key=j
    if(key!=999999999):
        return [latLong['long'][key],latLong['lat'][key]]
    else:
        return 0

def mainer():
    latLong=pd.read_excel('latlonginMainupd.xlsx')
    #print(datetime.datetime.now())
   
    india_totalCases = 0
    india_activecases = 0
    india_recovered= 0
    india_deaths= 0
    zonesPanda=pd.DataFrame()
    zoneData()
    daataa=[]
    stateCounter={}
    damnation=requests.get("https://api.covid19india.org/state_district_wise.json")
    districtupdateddata=damnation.json()
    for key in districtupdateddata.keys():
        statecount=0
        for k in (districtupdateddata.get(key).get('districtData').keys()):
            disConfirmed=districtupdateddata.get(key).get('districtData').get(k).get("confirmed")
            disActive=districtupdateddata.get(key).get('districtData').get(k).get("active")
            disRecovered=districtupdateddata.get(key).get('districtData').get(k).get("recovered")
            disDeaths=districtupdateddata.get(key).get('districtData').get(k).get("deceased")
            disDelta=districtupdateddata.get(key).get('districtData').get(k).get("delta")
            coor,zone=matcher_final(k.lower(),key.lower())
            india_totalCases=india_totalCases+int(disConfirmed)
            india_recovered=india_recovered+int(disRecovered)
            india_deaths=india_deaths+int(disDeaths)
            statecount=statecount+int(disConfirmed)
            stateCounter[key]=statecount
    india_activecases=india_totalCases-(india_recovered+india_deaths)
    for key in districtupdateddata.keys():    
        for k in (districtupdateddata.get(key).get('districtData').keys()):
            #print(districtupdateddata.get(key).get('districtData').get(k))
            disConfirmed=districtupdateddata.get(key).get('districtData').get(k).get("confirmed")
            disActive=districtupdateddata.get(key).get('districtData').get(k).get("active")
            disRecovered=districtupdateddata.get(key).get('districtData').get(k).get("recovered")
            disDeaths=districtupdateddata.get(key).get('districtData').get(k).get("deceased")
            disDelta=districtupdateddata.get(key).get('districtData').get(k).get("delta")
            coor,zone=matcher_final(k.lower(),key.lower())
            #if(key=="West Bengal"):
                #print(k,": ",key)
            if(coor):
                x=jsonWriter(k,key,disConfirmed,disActive,disRecovered,disDeaths,coor,zone)
                if(x):
                    daataa.append(x)
            else:
                iterr=59
    Dayumn={}
    Dayumn['type']="FeatureCollection"
    Dayumn['features']=daataa
    with open('covid19-geojsonALT.json', 'w') as outfile:
            json.dump(Dayumn, outfile)


# In[3]:


def covid19data():
    with open('covid19-geojsonALT.json') as dfile:
        data = json.load(dfile)
    return(data)


# In[4]:


app=Flask(__name__)
@app.route("/",methods=["GET"])
def coronavirus():
    mainer()
    return "Scraped"

@app.route("/coronadata",methods=["GET"])
def updates():
    return(covid19data())


# In[5]:


if __name__=="__main__":
    zonesPanda=pd.DataFrame()
    latLong=pd.read_excel('latlonginMainupd.xlsx')
    stateCounter={}
    india_totalCases=0
    india_activecases=0
    india_recoveres=0
    india_deaths=0
    app.run()


# In[ ]:




