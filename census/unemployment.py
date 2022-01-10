from ssl import get_default_verify_paths
import datacommons_pandas as dc
from numpy.lib.function_base import select
import pandas as pd
from seaborn.palettes import color_palette
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def num_col(count):
  if count%3 ==0:
    facet_col=3
  elif count%4 ==0:
    facet_col = 4
  elif count%5 == 0:
    facet_col = 5
  else:
    facet_col = 2
  return facet_col


def get_data():
  #dcid
  usa = 'country/USA'

  #get_places_in takes in the dcids and place_type
  states = dc.get_places_in([usa],'State')[usa]
  cities = dc.get_places_in([usa],'City')[usa]
  counties = dc.get_places_in([usa],'Country')[usa]

  # Get StatVarObservations for states. Can only retrieve 5 stats at a time
  # Since these stats don't have a data value, it is the most current stats
  state1 = dc.build_multivariate_dataframe(states, ['UnemploymentRate_Person', 'Count_Person_Unemployed'])
  female_age1 = dc.build_multivariate_dataframe(states, ['dc/5py5mzgsf2s0d', 'dc/prnecsckhxz07', 'dc/xmq3l1ryzhyp', 'dc/53htvdr97h714', 'dc/9h6hbz7nr496g' ])
  female_age2 = dc.build_multivariate_dataframe(states, ['dc/nnzdv3n5ght81', 'dc/tk0gp5l0c29c7', 'dc/rxnjd566thxdb','dc/dj7nl21cdjbh4'])
  male_age1 = dc.build_multivariate_dataframe(states, ['dc/b75jf3c2z7ty', 'dc/hgtn4j6e0jwp8', 'dc/7y0n4j9lvh58c', 'dc/yfby1t5v33r26', 'dc/ptd4yvqnswh1d'])
  male_age2 = dc.build_multivariate_dataframe(states,['dc/wsfjth7s5j2x1', 'dc/rt6rc914jphrd', 'dc/h6wd8y1nqs6b1', 'dc/f7xdhznm3e2xf'])

  #merge stats into df 
  female_age_df = pd.merge(female_age1, female_age2, on=["place"]).reset_index()
  male_age_df = pd.merge(male_age1, male_age2, on=["place"]).reset_index()

  #rename the columns
  female_age_df = female_age_df.rename({"place":"geoid", "dc/5py5mzgsf2s0d":"16-19", "dc/prnecsckhxz07":"20_21", "dc/xmq3l1ryzhyp":"22-24", 
                        "dc/53htvdr97h714":"25-34", "dc/9h6hbz7nr496g":"35-44", "dc/nnzdv3n5ght81":"45-54",
                        "dc/tk0gp5l0c29c7":"55-64", "dc/rxnjd566thxdb":"65-74", "dc/dj7nl21cdjbh4":"75+"}, axis=1)
  male_age_df = male_age_df.rename({"place":"geoid", "dc/b75jf3c2z7ty":"16-19", "dc/hgtn4j6e0jwp8":"20_21", "dc/7y0n4j9lvh58c":"22-24", 
                        "dc/yfby1t5v33r26":"25-34", "dc/ptd4yvqnswh1d":"35-44", "dc/wsfjth7s5j2x1":"45-54",
                        "dc/rt6rc914jphrd":"55-64", "dc/h6wd8y1nqs6b1":"65-74", "dc/f7xdhznm3e2xf":"75+"}, axis=1)
  return female_age_df, male_age_df

def geo_mapping(df):
  states_list = []
  for geoid in df["geoid"]:
    name_dict = dc.get_property_values([geoid], "name")
    state = name_dict.get(geoid)
    states_list.append(state[0])
    #2. mapping of state to geoid to create time series
  geoid_list = [geoid for geoid in df['geoid']]
  states_dict = dict(zip(geoid_list, states_list))
  return states_dict, states_list

def data_mapping(dict, selection_list):
  df = pd.DataFrame(columns=["state", "geoid", "date", "rate"]) 
  select_count = 0
  selected_id_list = []

  for state_name in selection_list:
    select_count+=1
    for geoid, state in dict.items():
      #first get the geoid of the state
      if state == state_name:
        selected_id_list.append(geoid)

  for i,id in enumerate(selected_id_list):
    #creating the dataframe 
    state_rate = dc.build_time_series(id, "UnemploymentRate_Person")
    rates_df = pd.DataFrame({'state':selection_list[i], 'geoid':id,
                            'date':state_rate.index,
                          'rate':state_rate.values})
    df = df.append(rates_df, ignore_index=True)
  return selected_id_list, df

def gender_data(geo_id_list, selection_list):
  female_age_dict = {"dc/5py5mzgsf2s0d":"16-19", "dc/prnecsckhxz07":"20-21", "dc/xmq3l1ryzhyp":"22-24", 
                        "dc/53htvdr97h714":"25-34", "dc/9h6hbz7nr496g":"35-44", "dc/nnzdv3n5ght81":"45-54",
                        "dc/tk0gp5l0c29c7":"55-64", "dc/rxnjd566thxdb":"65-74", "dc/dj7nl21cdjbh4":"75+"}
  male_age_dict = {"dc/b75jf3c2z7ty":"16-19", "dc/hgtn4j6e0jwp8":"20-21", "dc/7y0n4j9lvh58c":"22-24", 
                        "dc/yfby1t5v33r26":"25-34", "dc/ptd4yvqnswh1d":"35-44", "dc/wsfjth7s5j2x1":"45-54",
                        "dc/rt6rc914jphrd":"55-64", "dc/h6wd8y1nqs6b1":"65-74", "dc/f7xdhznm3e2xf":"75+"}

  f_age_df = pd.DataFrame(columns = {'state', 'geoid', 'date', 'gender', 'age', 'value'})
  m_age_df = pd.DataFrame(columns = {'state', 'geoid', 'date', 'gender', 'age', 'value'})
  for i, geoid in enumerate(geo_id_list):
    for age_id in female_age_dict.keys():
      f_age = dc.build_time_series(geoid, age_id)
      age_col = female_age_dict.get(age_id)
      age_df = pd.DataFrame({'state':selection_list[i], 'geoid':geoid, 'date':f_age.index, 'gender':'female',
                            'age':age_col, 'value':f_age.values})
      f_age_df = f_age_df.append(age_df, ignore_index=True)
    for age_id in male_age_dict.keys():
      m_age = dc.build_time_series(geoid, age_id)
      age_col = male_age_dict.get(age_id)
      age_df = pd.DataFrame({'state':selection_list[i], 'geoid':geoid, 'date':m_age.index, 'gender':'male',
                            'age':age_col, 'value':m_age.values})
      m_age_df = m_age_df.append(age_df, ignore_index=True)
  gender_age = pd.concat([f_age_df, m_age_df])
  return gender_age

def plot_all_states_rates(df):
  fig = px.line(df.sort_values(by='date', ascending=True), x='date', y="rate",
  labels={"State": "state"}, color="state", color_discrete_sequence=px.colors.qualitative.Set3)
  fig.update_layout(
      xaxis=dict(
          rangeselector=dict(
              buttons=list([
                  dict(count=1,
                      label="1m",
                      step="month",
                      stepmode="backward"),
                  dict(count=6,
                      label="6m",
                      step="month",
                      stepmode="backward"),
                  dict(count=1,
                      label="YTD",
                      step="year",
                      stepmode="todate"),
                  dict(count=1,
                      label="1y",
                      step="year",
                      stepmode="backward"),
                  dict(step="all")
              ])
          ),
          rangeslider=dict(
              visible=True
          ),
          type="date"
      ),
      font=dict(
          family="Courier New, monospace",
          size=12
      )
  )
  st.plotly_chart(fig, use_container_width=True)

def plot_gender(gender_df, counter):
  bars = px.bar(gender_df.sort_values(by='date', ascending=True), x="age", y="value", color="gender", barmode="group", facet_col="state",
              category_orders={"age": ["16-19", "20-21", "22-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"],
                                "sex": ["Male", "Female"]},
              animation_frame="date", animation_group="age", facet_col_wrap=num_col(counter))

  bars.update_layout(
      title="# of Unemployed by Gender and Age ",
      legend_title="Gender",
      font=dict(
          family="Courier New, monospace",
          size=12
      ),
      yaxis_title=None,
      xaxis_title=None,
      width=1100,height=500
  )
  bars.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  bars.update_yaxes(title=None)
  st.plotly_chart(bars, use_container_width=True, width=1100,height=500)


def main():
  st.title('USA Unemployment')
  female_age_df, male_age_df = get_data()
  states_dict, states_list = geo_mapping(female_age_df)

  #1. select a state - state_multi returns a list
  with st.form(key='Selecting columns'):
    state_multi = st.multiselect('Select state(s): ', (states_list), default=['New York', 'California'])
    submit_button = st.form_submit_button(label='Run')
  counter=0
  if submit_button:
    # set condition for multiselect:
    for i in state_multi:
      counter+=1
    if counter>10:
      st.warning("Only a maximum of 10 states can be displayed.")
      return
    else:
      selected_id_list, states_rate_df = data_mapping(states_dict, state_multi)
      gender_df = gender_data(selected_id_list, state_multi)

      #3. plotting time series of unemployment rate for selected state
      plot_all_states_rates(states_rate_df)
      #plotting time series of unemployment by age
      
      plot_gender(gender_df, counter)
      # plot2
  

if __name__ == "__main__":
  main()
