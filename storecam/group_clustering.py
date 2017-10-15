import pymysql
import pymysql.cursors
import pandas as pd
import requests
import json
import datetime
import time
import numpy as np
import pytz
a = 1
df_raw = load.firebase('hugyn.cohlopat2sz6.us-west-2.rds.amazonaws.com')
while a==1:
  time.sleep(300)
  df_unclustered = df_raw[df_raw['clustered'] == None]
  df_unclustered['plus_time_one'] = df_unclustered['time_entered'] + 20
  df_unclustered['minus_time_one'] = df_unclustered['time_entered'] - 20
  df_unclustered['plus_time_two'] = df_unclustered['time_leaving'] + 20
  df_unclustered['minus_time_two'] = df_unclustered['time_leaving'] - 20
  list_one = df_unclustered['time_entered'].tolist()
  list_two = df_unclustered['time_leaving'].tolist()


  for x in df_unclustered:
      time_entered = [i for i in list_one if (i >= df_unclustered['plus_time_one']) & (i <= df_unclustered['minus_time_one'])]
      time_leaving = [i for i in list_two if (i >= df_unclustered['plus_time_two']) & (i <= df_unclustered['minus_time_two'])]
      df1 = df_unclustered.merge(j2, how='left', on=['time_entered'], errors='coerce')
      df2 = df1.merge(j3, how='left', on=['time_leaving'], errors='coerce')
      df3 = df2[(df2['time_entered'] != None) & (df2['time_leaving'] != None)]
      if df3['Age'].nunique() = 1:
          df3['clustered'] = 'Friends'
      elif df3['Age'].nunique() = 2:
          df3['clustered'] = 'Family'
      else:
          df3['clustere'] = 'Single'
      df_raw = df_raw.merge(df3, how='left', on=['time_entered', 'time_leaving']
