#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import folium

CT_path = "C:/Users/Praveenaa/Desktop/Resilience/data/tl_rd22_04_tract/tl_rd22_04_tract.shp"
df_CT = gpd.read_file(CT_path)

place_path = "C:/Users/Praveenaa/Desktop/Resilience/census/combined_shp/combined_shp.shp"
df_places = gpd.read_file(place_path, mask=df_CT)


# In[2]:


import openpyxl

# Load the workbook
workbook = openpyxl.load_workbook('C:/Users/Praveenaa/Desktop/Resilience/data/AZ2021WaterSewerRatesTables_Final.xlsx')

# Select the specific sheet by name
sheet_name = 'Table of Participants'
sheet = workbook[sheet_name]

# Define the column letter for 'Primary Service Area'
column_letter = 'M'  # Replace with the appropriate column letter (e.g., 'A' for column A)

# Create a list to store the values from the column
primary_service_area_values = []

# Iterate over the rows in the column
for cell in sheet[column_letter]:
    # Access cell values
    primary_service_area_values.append(cell.value)

# Print the values
print(primary_service_area_values)

# Close the workbook when finished
workbook.close()


# In[3]:



# Filter the geopandas dataframe based on the included values
df_PSA = df_places[df_places['NAMELSAD'].isin(primary_service_area_values)]


# In[4]:


df_PSA


# In[5]:


columns_to_delete = ['STATEFP','PLACENS', 'PLACEFP','GEOID','NAME','LSAD','CLASSFP','PCICBSA','PCINECTA','ALAND','AWATER','FUNCSTAT','MTFCC','INTPTLAT','INTPTLON']
df_PSA = df_PSA.drop(columns_to_delete, axis=1)
columns_to_delete_CT = ['STATEFP','COUNTYFP', 'TRACTCE','GEOID','NAME','MTFCC','ALAND','AWATER','FUNCSTAT','MTFCC','INTPTLAT','INTPTLON']
df_CT = df_CT.drop(columns_to_delete_CT, axis=1)


# In[6]:


m = df_CT.explore(height=1000, width=1000, name="CensusTract",tooltip="NAMELSAD",popup=True)
m = df_PSA.explore(m=m, color="red", name="PrimaryServiceArea",tooltip="NAMELSAD",popup=True)
# this is completely optional
folium.LayerControl().add_to(m)


# In[7]:


m


# In[13]:


merged = gpd.overlay(df_PSA, df_CT, how='union')
merged.explore()


# In[19]:


# Perform spatial join
joined_layer = gpd.sjoin(df_CT, df_PSA, how='inner', op='intersects')
joined_layer.explore()


# In[20]:


# Perform spatial join
joined_layer = gpd.sjoin(df_CT, df_PSA, how='left', op='intersects')
joined_layer.explore()


# In[ ]:




