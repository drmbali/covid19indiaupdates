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


# In[2]:


def matcher_detailed(pdat_i,pdats_i,latLong):
    key=999999999
    for j in range(len(latLong)):
        latlong_district=(latLong['district'][j].strip()).lower()
        latlong_state=(latLong['state'][j].strip()).lower()
        if(fuzz.ratio(pdat_i,latlong_district)>85):
            if(fuzz.ratio(pdats_i,latlong_state)>92):
                key=j
    if(key!=999999999):
        return [latLong['long'][key],latLong['lat'][key]]
    else:
        return 0
def jsonWriter(dist,state,conf,act,rec,dead,coor,stateCounter,india_totalCases,india_activecases,india_recovered,india_deaths):
    if(coor):
        
        g={}
        g['type']="Point"
        g['coordinates']=coor
        
        d={}
        d['updatedOn']=str(datetime.datetime.now().date())
        d['city']=dist
        d['district']=dist
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


# In[3]:


damnation=requests.get("https://api.covid19india.org/v2/state_district_wise.json")
districtupdateddata=damnation.json()

latLong=pd.read_excel('latlonginMainupd.xlsx')


# In[5]:


daataa=[]
stateCounter={}

indcnfrmd=indactive=indrcvrd=inddeaths=0
for i in range(1,len(districtupdateddata)):
    stateCases=0
    d=districtupdateddata[i]
    state=str(d.get('state'))
    dist=d.get('districtData')
    for D in dist:
        district=str(D.get('district'))
        active=int(D.get('active'))
        rcvrd=int(D.get('recovered'))
        cnfrmd=int(D.get('confirmed'))
        deaths=int(D.get('deceased'))
        stateCases=stateCases+cnfrmd
        indcnfrmd=indcnfrmd+cnfrmd
        indactive=indactive+active
        indrcvrd=indrcvrd+rcvrd
        inddeaths=inddeaths+deaths
    stateCounter[state]=stateCases
        
for i in range(1,len(districtupdateddata)):
    d=districtupdateddata[i]
    state=str(d.get('state'))
    dist=d.get('districtData')
    for D in dist:
        district=str(D.get('district'))
        active=int(D.get('active'))
        rcvrd=int(D.get('recovered'))
        cnfrmd=int(D.get('confirmed'))
        deaths=int(D.get('deceased'))
        if(cnfrmd!=0):
            coor=matcher_detailed(district.lower(),state.lower(),latLong)
            if(coor):
                x=jsonWriter(district,state,cnfrmd,active,rcvrd,deaths,coor,stateCounter,indcnfrmd,indactive,indrcvrd,inddeaths)
                if(x):
                    daataa.append(x)
            else:
                iterr=59
Dayumn={}
Dayumn['type']="FeatureCollection"
Dayumn['features']=daataa
with open('covid19-geojsonALT.json', 'w') as outfile:
        json.dump(Dayumn, outfile)


import boto3
s3_client = boto3.client('s3',
                          aws_access_key_id='AWS ACCESS KEY',
                          aws_secret_access_key='SECRET ACCESS KEY',
                          aws_session_token='SESSION TOKEN (NOT REQUIRED FOR ALL THE AWS USERS)',
                          region_name='REGION NAME'
                          )
bucket='dl-model-bucket-101'
file_name='covid19-geojsonALT.json'
response = s3_client.upload_file(file_name, bucket,file_name,ExtraArgs={'ACL': 'public-read'}) ## WE MADE OUR DATA SOURCE PUBLIC, SO GIVEN PUBLIC ACCESS, THIS PARAMETER CAN BE REMOVED TO KEEP YOUR GEOJSON FILE PRIVATE. 
#response = s3_client.upload_file(file_name, bucket,file_name) #WITHOUT MAKING DATA SOURCE PUBLIC
print('successfully uploaded to s3 bucket!!!!!!!!')
