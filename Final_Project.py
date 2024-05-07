'''
Name: Michael Zlochevsky
CS 230: Section 4
Data: Rest_Areas.csv

Description:
The following code targets specific aspects of the California rest stops data. There are several graphs and maps that can be accessed by the user to gain a better understanding of the data.
'''


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

path = "C:/Users/micha/OneDrive - Bentley University/Sophomore Year - Semester 2 (OneDrive)/Introduction to Programming with Python (CS 230-4)/pythonProject/Final_Project_Folder/"
df = pd.read_csv(path + 'Rest_Areas.csv')

# [DA7] Drop Column: removing empty columns
df.drop(columns=['POSTMILE_P', 'POSTMILE_S'], inplace=True)


# [DA1] Cleaning Data: removing any rows with empty values
df.dropna(inplace=True)

#[PY1]: Function with default value
def sort_data_function(choice = "CITY"):
    if choice == "CITY":
        df.set_index('CITY', inplace=True)
        # [DA2] Sorting data by alphabetical order of the CITY
        df.sort_values(by='CITY', ascending=True, inplace=True)
    elif choice == "COUNTY":
        df.set_index('COUNTY', inplace=True)
        # [DA2] Sorting data by alphabetical order of the COUNTY
        df.sort_values(by='COUNTY', ascending=True, inplace=True)
    else:
        print("Incorrect input, try again...")
        initial_input = input("Enter the colomn that you want the data to be indexed by and sorted by (alphabetically), CITY or COUNTY: ").upper().strip()
        sort_data_function(initial_input)

#[PY2]: Function that returns more than one value
def highest_latitude_rest_stop(curiosity):
    if curiosity == "yes":
        #[DA3] Top largest value of a column
        row_with_max_latitude = df.loc[df['LATITUDE'].idxmax()]
        highest_lat_stop = row_with_max_latitude['NAME']
        highest_lat_address = row_with_max_latitude['ADDRESS']
        return highest_lat_stop, highest_lat_address
    elif curiosity == "no":
        pass
    else:
        print("Incorrect input, try again...")
        northern_travel_response = input("For northern state travelers: Would you like to find out the highest latitude rest stop with the address, yes or no? ").lower().strip()
        highest_latitude_rest_stop(northern_travel_response)
        if northern_travel_response == "yes":
            highest_lat_stop, highest_lat_address = highest_latitude_rest_stop(northern_travel_response)
            print(f"The highest latitude rest stop is the {highest_lat_stop} with the address {highest_lat_address}")
        else:
            pass


initial_input = input("Enter the colomn that you want the data to be indexed by and sorted by (alphabetically), CITY or COUNTY: ").upper().strip()
sort_data_function(initial_input)

print()
print()

northern_travel_response = input("For northern state travelers: Would you like to find out the highest latitude rest stop with the address, yes or no? ").lower().strip()
highest_latitude_rest_stop(northern_travel_response)
if northern_travel_response == "yes":
    highest_lat_stop, highest_lat_address = highest_latitude_rest_stop(northern_travel_response)
    print(f"The highest latitude rest stop is the {highest_lat_stop} with the address {highest_lat_address}")
else:
    pass



if initial_input == "CITY":
    st.write("This is the data for car-only rest stops (no RVs allowed)")

    # [DA4] Filtering data by one condition: only listing the data for rest locations that are car-only and are not for RVs
    df_car_only_locations = df[df['RV_STATION'] == 'No']
    st.write("Many people who stop at rest stations want to conveniently enter and leave, without any large RV vehicles blocking their paths. Therefore, it is good to filter the RV-friendly locations out.")
    st.dataframe(df_car_only_locations)

    city_grouping = df_car_only_locations.groupby('CITY').size()
    df_cg = city_grouping.reset_index(name='Count')
    st.write("The number of car-only rest stops per city (no RVs allowed)...")
    st.dataframe(df_cg)

    # [VIZ1]: PieChart
    city_grouping.plot(kind='pie', autopct='%.2f%%', textprops={'fontsize': 5}, pctdistance=0.95)
    plt.title("Percent of total car-only rest stops that are in each city (no RVs allowed)")
    plt.ylabel('')
    # To get rid of the PyplotGlobalUseWarning, it suggested using the following line
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


    # [DA5] Filtering data by two or more conditions: every amenity included
    df_everything_locations = df[(df['RESTROOM'] == 'Yes') & (df['WATER'] == 'Yes') & (df['PICNICTAB'] == 'Yes') & (df['PHONE'] == 'Yes') & (df['HANDICAP'] == 'Yes') & (df['RV_STATION'] == 'Yes') & (df['VENDING'] == 'Yes') & (df['PET_AREA'] == 'Yes')]

    st.write("The following table displays the rest stops that have all amenities included")
    st.dataframe(df_everything_locations)

    st.write("Based on the table above, it would be interesting to find out the number of rest stops per city providing each specific ammenity...")


    #Code for dropdown and bar chart based on ChatGPT, see section 1 of AI Report document.
    # [ST1] Widget: dropdown
    selected_amenity = st.selectbox('Select an amenity:', ['RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING', 'PET_AREA'])

    amenity_counts = df_everything_locations[df_everything_locations[selected_amenity] == 'Yes'].groupby('CITY').size()

    # [VIZ2] Bar Chart
    fig, ax = plt.subplots()
    amenity_counts.plot(kind='bar', ax=ax)
    ax.set_title(f'Number of Rest Stops per City Providing {selected_amenity}')
    ax.set_ylabel('Number of Rest Stops')
    ax.set_xlabel('City')

    st.pyplot(fig)

elif initial_input == "COUNTY":
    st.write("This is the data for car-only rest stops (no RVs allowed)")

    # [DA4] Filtering data by one condition: only listing the data for rest locations that are car-only and are not for RVs
    df_car_only_locations = df[df['RV_STATION'] == 'No']
    st.write("Many people who stop at rest stations want to conveniently enter and leave, without any large RV vehicles blocking their paths. Therefore, it is good to filter the RV-friendly locations out.")
    st.dataframe(df_car_only_locations)

    county_grouping = df_car_only_locations.groupby('COUNTY').size()
    df_cg = county_grouping.reset_index(name='Count')
    st.write("The number of car-only rest stops per county (no RVs allowed)...")
    st.dataframe(df_cg)

    # [VIZ1]: PieChart
    county_grouping.plot(kind='pie', autopct='%.2f%%', textprops={'fontsize': 5}, pctdistance=0.95)
    plt.title("Percent of total car-only rest stops that are in each county (no RVs allowed)")
    plt.ylabel('')
    # To get rid of the PyplotGlobalUseWarning, it suggested using the following line
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    # [DA5] Filtering data by two or more conditions: every amenity included
    df_everything_locations = df[(df['RESTROOM'] == 'Yes') & (df['WATER'] == 'Yes') & (df['PICNICTAB'] == 'Yes') & (df['PHONE'] == 'Yes') & (df['HANDICAP'] == 'Yes') & (df['RV_STATION'] == 'Yes') & (df['VENDING'] == 'Yes') & (df['PET_AREA'] == 'Yes')]

    st.write("The following table displays the rest stops that have all amenities included")
    st.dataframe(df_everything_locations)

    st.write("Based on the table above, it would be interesting to find out the number of rest stops per county providing each specific ammenity...")

    # Code for dropdown and bar chart based on ChatGPT, see section 1 of AI Report document.
    # [ST1] Widget: dropdown
    selected_amenity = st.selectbox('Select an amenity:',['RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING','PET_AREA'])

    amenity_counts = df_everything_locations[df_everything_locations[selected_amenity] == 'Yes'].groupby('COUNTY').size()

    # [VIZ2] Bar Chart
    fig, ax = plt.subplots()
    amenity_counts.plot(kind='bar', ax=ax)
    ax.set_title(f'Number of Rest Stops per County Providing {selected_amenity}')
    ax.set_ylabel('Number of Rest Stops')
    ax.set_xlabel('County')

    st.pyplot(fig)


#[ST2] Widget: Radio Buttons
map_type = st.sidebar.radio("Select map type:", ('Simple Map', 'Scatter Map'))

map_data = df[['LATITUDE', 'LONGITUDE']].dropna()

#[VIZ3]: Simple Map
if map_type == 'Simple Map':
    st.write("This is a map of every available rest stop location based on LONGITUDE and LATITUDE values...")
    st.map(map_data)
else:
    #[VIZ4]: Scatter Map
    st.write("")
    fig, ax = plt.subplots()
    ax.scatter(map_data['LONGITUDE'], map_data['LATITUDE'])
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Scatter Map of Rest Stops')
    st.pyplot(fig)


