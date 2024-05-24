#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

file_path = 'C:/Users/Praveenaa/Desktop/Resilience/data/AZ2021WaterSewerRatesTables_Final.xlsx'
sheet1_name = 'Table of Participants'
sheet2_name = 'Residential Water Billing'

df1 = pd.read_excel(file_path, sheet_name=sheet1_name)
df2 = pd.read_excel(file_path, sheet_name=sheet2_name)

column_index1 = 1  
column_index2 = 0  

column_name1 = df1.columns[column_index1]
column_name2 = df2.columns[column_index2]

merged_df = pd.merge(df1, df2, left_on=column_name1, right_on=column_name2)

print(merged_df)


# In[3]:


merged_df


# In[4]:


first_row_values = merged_df.iloc[1].values
print(first_row_values)


# In[5]:


column_names = merged_df.columns.tolist()
column_names


# In[6]:


merged_df = merged_df.rename(columns={"Unnamed: 12": "CDP"})


# In[7]:


column_names = merged_df.columns.tolist()
column_names


# In[8]:


merged_df = merged_df.drop(0)


# In[9]:


merged_df['Zero Gallons \n(0 cf)'] = pd.to_numeric(merged_df['Zero Gallons \n(0 cf)'])

merged_df = merged_df.sort_values(by='Zero Gallons \n(0 cf)', ascending=False).drop_duplicates(subset='CDP')

print(merged_df)


# In[10]:


first_row_values = merged_df.iloc[0].values
print(first_row_values)


# In[11]:


import geopandas as gpd
import folium

CT_path = "C:/Users/Praveenaa/Desktop/Resilience/data/tl_rd22_04_tract/tl_rd22_04_tract.shp"
df_CT = gpd.read_file(CT_path)

place_path = "C:/Users/Praveenaa/Desktop/Resilience/census/combined_shp/combined_shp.shp"
df_places = gpd.read_file(place_path, mask=df_CT)

df_PSA = df_places[df_places['NAMELSAD'].isin(merged_df['CDP'])]


# In[12]:


df_PSA = df_PSA.rename(columns={"NAMELSAD": "CDP"})


# In[13]:


df = pd.merge(merged_df, df_PSA, on='CDP')

print(df)


# In[14]:


gdf = gpd.GeoDataFrame(df, geometry='geometry')


# In[15]:


column_names = gdf.columns.tolist()
column_names


# In[16]:


first_row_values = gdf.iloc[1].values
print(first_row_values)


# In[18]:


joined_layer = gpd.sjoin(df_CT, gdf, how='left', op='intersects')


# In[19]:


columns_to_drop = ['STATEFP_left',
 'COUNTYFP',
 'TRACTCE',
 'NAME_left',
 'MTFCC_left',
 'FUNCSTAT_left',
 'ALAND_left',
 'AWATER_left',
 'INTPTLAT_left',
 'INTPTLON_left',
 'index_right',
 '#',
 'Services Provided\n(Water=W,\nSewer=S,\nBoth=B)',
 'Approx. Number of Water Connections\n(from EPA SDWIS)',
 'Service Population (Approx.)_x',
 'Institutional Arrangement',
 "Residential Rates Changed Since Last Year's Survey?",
 'Unnamed: 6',
 'Year or Date of Last Rates Change',
 'Institutional Arrangement',
 "Residential Rates Changed Since Last Year's Survey?",
 'Unnamed: 6',
 'Year or Date of Last Rates Change',
 'Service Population (Approx.)_y',
 'Source Water\n(GW=Groundwater,\nSW=Surface Water,\nGU=GW under inf.,\nP=Purchase)',   
 'Zero Gallons \n(0 cf)',
 'Unnamed: 3',
 '4,000 Gallons \n(535 cf)',
 'Unnamed: 5',
 '5,000 Gallons \n(668 cf)',
 'Unnamed: 7',
 '6,000 Gallons \n(802 cf)',
 'Unnamed: 9',
 'Unnamed: 11',
 '15,000 Gallons \n(2,005 cf)',
 'Unnamed: 13',
 'STATEFP_right',
 'PLACEFP',
 'PLACENS',
 'GEOID_right',
 'NAME_right',
 'LSAD',
 'CLASSFP',
 'PCICBSA',
 'PCINECTA',
 'MTFCC_right',
 'FUNCSTAT_right',
 'ALAND_right',
 'AWATER_right',
 'INTPTLAT_right',
 'INTPTLON_right']
joined_layer = joined_layer.drop(columns_to_drop, axis=1)


# In[20]:


joined_layer


# In[21]:


joined_layer.to_csv('CT_WaterStructure.csv')


# In[20]:


joined_layer['Utility / Rate Structure'] = joined_layer['Utility / Rate Structure'].astype(str)

joined_layer['Median Household Income in 2020 (U. S. Census Bureau)'] = joined_layer['Median Household Income in 2020 (U. S. Census Bureau)'].astype(str)

joined_layer['County'] = joined_layer['County'].astype(str)

joined_layer['CDP'] = joined_layer['CDP'].astype(str)

joined_layer['GEOID_left'] = joined_layer['GEOID_left'].astype(str)
joined_layer['NAMELSAD'] = joined_layer['NAMELSAD'].astype(str)
joined_layer['10,000 Gallons \n(1,337 cf)'] = joined_layer['10,000 Gallons \n(1,337 cf)'].astype(str)


joined_layer = joined_layer.groupby('GEOID_left').agg({'Utility / Rate Structure': ','.join,
                                        'NAMELSAD':'first',
                                        'County': ','.join,
                                        'Median Household Income in 2020 (U. S. Census Bureau)': ','.join,
                                        'CDP': ','.join,
                                        '10,000 Gallons \n(1,337 cf)':','.join,
                                        'geometry': 'first'}).reset_index()

print(joined_layer)


# In[21]:


target_value = 'Census Tract 9414.02'

for index, row in joined_layer.iterrows():
    if row['NAMELSAD'] == target_value:
        print(row)


# In[22]:


joined_layer = gpd.GeoDataFrame(joined_layer, geometry='geometry')


# In[23]:


joined_layer.head(10)


# In[24]:


df_sorted = df_CT.sort_values(by='NAMELSAD', ascending=True)

df_sorted.head(10)


# In[25]:


values_not_in_joined_layer = joined_layer[~joined_layer['NAMELSAD'].isin(df_CT['NAMELSAD'])]

print(values_not_in_joined_layer)


# In[27]:


joined_layer = joined_layer.set_crs(epsg=4269)


# In[28]:


joined_layer['County'] = joined_layer['County'].apply(lambda x: ','.join(set(x.split(','))))

print(joined_layer)


# In[30]:


def process_income_values(income):
    if pd.isna(income) or income == '':
        return income  # Return NaN or empty string as-is
    values = [float(x) for x in income.split(',') if x != '']
    if not values:
        return ''  # Handle empty values (e.g., '')
    min_value = str(min(values))
    max_value = str(max(values))
    return min_value + ',' + max_value

joined_layer['Median Household Income in 2020 (U. S. Census Bureau)'] = joined_layer['Median Household Income in 2020 (U. S. Census Bureau)'].apply(process_income_values)


# In[31]:


joined_layer = joined_layer.rename(columns={'10,000 Gallons \n(1,337 cf)': '10,000 Gallons'})
joined_layer = joined_layer.rename(columns={'Median Household Income in 2020 (U. S. Census Bureau)': 'Median Household Income in 2020 (Min, Max)'})


# In[32]:


joined_layer['10,000 Gallons'] = joined_layer['10,000 Gallons'].replace('nan','1000')


# In[33]:


joined_layer


# In[34]:


joined_layer['10,000 Gallons'] = joined_layer['10,000 Gallons'].str.split(',').apply(lambda x: max(map(float, x)))


# In[35]:


joined_layer = joined_layer.drop(['County'], axis=1)


# In[36]:


joined_layer.explore(tooltip="NAMELSAD", popup=True)


# In[37]:


joined_layer.to_csv('WaterBill_CensusTract.csv', index=False)

