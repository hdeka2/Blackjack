'''
Name: Heemakshi Deka
Class: Frydenberg CS230
Data: Volcanoes

Description: .
. . select_country allows the user to select a country from the country_list pulling the data from the
"Country" column in the volcanoes.csv file and displays only volcanoes from the selected country. rock_type_volcano allows
the user to select one of the different rock types pulling from the "Dominant Rock Type" column in the volcanoes.csv file.


'''


import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.patches as mpatches

#bar_chart takes data from the column "Dominant Rock Type" from the volcanoes.csv and compares the data in a bar graph
def bar_chart(volcanoes):
    volcanoes["Dominant Rock Type"].value_counts().plot(kind='bar', color='coral')
    plt.xlabel("Dominant Rock Type", fontname="Times New Roman", fontweight="bold")
    plt.ylabel("Volcano Count", fontname="Times New Roman", fontweight="bold")
    plt.title("Number of Volcanoes By Different Dominant Rock Type", fontname="Times New Roman", fontweight="bold")
    plt.grid(b=True, which="major", axis="both", color="white")
    red_patch = mpatches.Patch(color='coral', label='Volcano Count')
    plt.legend(handles=[red_patch])

    return plt

#pie_chart takes data from the column "Activity Evidence" and displays the data in a pie chart
def pie_chart(volcanoes):
    colors = ['salmon', 'tomato', 'coral', 'sienna', 'chocolate', 'peru']

    activity_evidence = volcanoes["Activity Evidence"]
    uncertain_tuple = ("Evidence Uncertain", "Uncertain Evidence")
    activity_evidence.replace({uncertain_tuple[0]: "Uncertain", uncertain_tuple[1]: "Uncertain"}, inplace=True) # duplicate entry in CSV for same value (uncertain)

    activity_evidence.value_counts().plot(kind='pie', autopct='%1.1f%%', colors=colors) # sorted by descending value_counts order

    # grab legend order to match color
    volcanoes["frequency"] = volcanoes.groupby("Activity Evidence")["Activity Evidence"].transform('count')
    volcanoes.sort_values('frequency', inplace=True, ascending=False)

    activity_evidence_by_frequency = volcanoes["Activity Evidence"].unique()

    patches = [mpatches.Patch(color=colors[i], label="{:s}".format(activity_evidence_by_frequency[i])) for i in range(len(activity_evidence_by_frequency))] #maps through color and columns

    plt.axis('off')
    plt.title("Volcano Eruptions By Last Volcano Activity", loc='right')
    plt.legend(handles=patches)
    plt.legend(bbox_to_anchor=(1.05, 1.0, 0.3, 0.2), loc='upper left')
    return plt

#volcano_stats takes data from column "Elevation (m)" and spits out the maximum, minimum, median, and mode
values longitude and latitude
def volcano_stats(volcanoes):
    stats = pd.to_numeric(volcanoes["Elevation (m)"], downcast='signed')
    statistics = {}
    statistics["max"] = stats.max()
    statistics["min"] = stats.min()
    statistics["mean"] = stats.mean().round()
    statistics["median"] = stats.median()
    return statistics

#map_display displays the map based on the 
def map_display(volcanoes, z=1):
    lat_long_tuple = ("lat", "lon")
    coordinates = volcanoes[["Latitude", "Longitude"]]
    coordinates = coordinates.rename(columns={'Latitude': lat_long_tuple[0], "Longitude": lat_long_tuple[1]})
    coordinates = coordinates.apply(pd.to_numeric)
    st.map(coordinates, zoom=z)


def select_country(volcanoes):
    country_list = volcanoes["Country"]
    country_list = list(set(country_list))
    country_list.sort()
    option = st.selectbox("Select Country:", country_list)
    st.write("Selected:", option)
    df_new = volcanoes[volcanoes['Country'] == option]
    st.write(df_new)


def rock_type_volcano(volcanoes):
    rock_type_list = volcanoes["Dominant Rock Type"].drop_duplicates().tolist()
    rock_type_list.sort()
    selection = st.sidebar.selectbox("Select Dominant Rock Type:", rock_type_list)
    map_display(volcanoes)


def tectonic_setting_volcano(volcanoes):
    tectonic_setting_list = volcanoes["Tectonic Setting"].drop_duplicates().tolist()
    tectonic_setting_list.sort()
    make_choice = st.sidebar.selectbox("Select Tectonic Setting:", tectonic_setting_list)
    tectonic_setting = volcanoes["Tectonic Setting"].loc[volcanoes["Country"] == make_choice].loc
    map_display(volcanoes)


def main():
    volcanoes = pd.read_csv("volcanoes.csv")
    volcanoes = volcanoes.drop(0, 0)
    page = st.sidebar.selectbox("Select page", ["Home", "Volcano Analytics", "Pie Chart", "Bar Chart", "Map"])
    if page == "Home":
        header = '<p styles="font-family: serif; color:Black; font-size: 44px:">Welcome to Volcano Data Analytics<p>'
        sub_header = '<p styles="font-family: serif; color:Black; font-size: 22px:">by Heemakshi Deka<p>'
        st.markdown(header, unsafe_allow_html=True)
        st.markdown(sub_header, unsafe_allow_html=True)
        from PIL import Image
        img = Image.open("volcano.png")
        st.image(img, width=700)

    elif page == "Pie Chart":
        st.title("Volcano Activity Evidence Records")
        pie = pie_chart(volcanoes)
        st.pyplot(pie, clear_figure=True)

    elif page == "Bar Chart":
        st.title("Dominant Rock Types Comparison")
        st.pyplot(bar_chart(volcanoes), clear_figure=True)

    elif page == "Volcano Analytics":
        st.title("Volcano Elevation Statistics")
        st.subheader("Maximum, Minimum, Mean, and Median of Height in Elevations (Meters)")
        stats = volcano_stats(volcanoes)
        st.write("Maximum Elevation:", stats["max"])
        st.write("Minimum Elevation:", stats["min"])
        st.write("Mean Elevation:", stats["mean"])
        st.write("Median Elevation:", stats["median"])
    elif page == "Map":
        st.title("All Volcanoes Map")
        map_display(volcanoes)
        page = st.sidebar.selectbox("Further Volcano Analytics", ["Volcanoes by Country", "Volcanoes by Dominant Rock Type", "Volcanoes by Tectonic Setting"])

        if page == "Volcanoes By Country":
            st.title("Volcanoes Based on Country")
            st.subheader("Choice Displayed on Map")
            select_country(volcanoes)
        elif page == "Find Volcano Based on Dominant Rock Type":
            st.title("Volcanoes by Rock Type")
            st.subheader("Displays Choice on Map")
            rock_type_volcano(volcanoes)
        elif page == "Find Volcanoes Based on Tectonic Setting":
            st.title("Volcanoes by Tectonic Setting")
            tectonic_setting_volcano(volcanoes)


main()
