# -*- coding: utf-8 -*-
"""
Author: Prabhat Turlapati
"""
import os
import datetime
import configparser
import pandas as pd
from bokeh.layouts import widgetbox, column, gridplot
from bokeh.plotting import figure, curdoc, show
from bokeh.models.widgets import MultiSelect, Button, Select, CheckboxGroup, \
CheckboxButtonGroup, DateRangeSlider, Div
from bokeh.themes import Theme

#Custom imports
from orm_generic import Connection

# Get DB configs from config file
SCRIPT_DIRECTORY = os.path.join(os.path.dirname(__file__))
CONFIG = configparser.RawConfigParser()

# Initialize Custom Class Objects and required global variables
conn_obj = Connection('plotting_tool_database', 'postgres', 'localhost', 'password')

#get the equipment set data
CAT_QUERY = conn_obj.get_categories()

#create the widget for categories
CATEGORY_LIST = sorted(CAT_QUERY)
list_of_categories = CheckboxGroup(labels=CATEGORY_LIST, \
                                  active=[])
list_of_files = MultiSelect(title="Option:", \
                            value=[], \
                            options=[""])

list_plot1 = Select(title="Select sub-category for Plot 1:", \
                    value="Plot1Data", \
                    options=["Select One.."])
list_plot2 = Select(title="Select sub-category for Plot 2:", \
                    value="Plot2Data", \
                    options=["Select One.."])
list_plot3 = Select(title="Select sub-category for Plot 3:", \
                    value="Plot3Data", \
                    options=["Select One.."])

# Button for range windows
range_window_button = Button(label="Ok")
start = datetime.datetime.strptime("1988-01-01", '%Y-%m-%d').date()
end = datetime.datetime.strptime("1991-12-31", '%Y-%m-%d').date()
date_slider = DateRangeSlider(title="Date Range", \
                            start=start, \
                            end=end, \
                            value=(start, end), \
                            step=365)

def category_callback(attr, old, new):
    """Button to select categories"""
    active_equipment = [list_of_categories.labels[i] for i in
                        list_of_categories.active]
    print(active_equipment)
    new_file_list = []
    blank_entry = [""]
    new_file_list.extend(blank_entry)
    for each in active_equipment:
        print("Category:", each)
        file_list = conn_obj.get_category_list(category=each)
        new_file_list.extend(file_list)

    new_file_set = set(new_file_list)
    list_plot1.options = sorted(list(new_file_set))
    list_plot2.options = sorted(list(new_file_set))
    list_plot3.options = sorted(list(new_file_set))

# Create a figure whenever option is changed
def create_figure(df, x_range=None, y_range=None, title=None):
    """Create a figure and plot the data"""
    plot = figure(plot_height=200, \
            tools='pan,box_zoom,hover,reset', \
               x_axis_type='datetime', \
               title=title, \
               sizing_mode = 'scale_width')
    plot.xaxis.axis_label = "Time"
    plot.yaxis.axis_label = "mean temperature"
    if x_range != None:
        plot.x_range = x_range
    if y_range != None:
        plot.y_range = y_range

    plot.line(df.iloc[:, 0], \
              df.iloc[:, 1], \
              color='#A5CEE3', \
              legend='Channel')
    print("Plotted ")
    return plot    
    
# callback for plot 1
def plot1_list_callback(attr, old, new):
    """Callback for the first plot.
    The plot changes based on option selected."""
    print(new)
    option = list_plot1.value
    if option != "":
        category = conn_obj.get_category_name(option)
        print("Equipment: ", category)
        print("selected channel name: ", option)
        test_df_plot_1 = conn_obj.get_fact(category=category, \
                                               selected_option=option)
        min_tmstmp = test_df_plot_1.iloc[:, 0].min().date()
        max_tmstmp = test_df_plot_1.iloc[:, 0].max().date()
        left = datetime.datetime.strptime(str(min_tmstmp), '%Y-%m-%d').date()
        right = datetime.datetime.strptime(str(max_tmstmp), '%Y-%m-%d').date()
        date_slider.value = (left, right)
        print(test_df_plot_1.shape[0])
        if test_df_plot_1.shape[0] > 1:
            LAYOUT.children[2] = create_figure(test_df_plot_1, \
                           title=option)
        else:
            LAYOUT.children[2] = create_figure(DUMMY_DF, \
                           title="No Data to Plot")
    else:
        print("blank selected!!")
        LAYOUT.children[2] = create_figure(DUMMY_DF, \
                       title="Nothing Selected..")

# callback for plot 2
def plot2_list_callback(attr, old, new):
    """Callback for the second plot.
    The plot changes based on option selected."""
    print(new)
    option = list_plot1.value
    if option != "":
        category = conn_obj.get_category_name(option)
        print("Equipment: ", category)
        print("selected channel name: ", option)
        test_df_plot_1 = conn_obj.get_fact(category=category, \
                                               selected_option=option)
        min_tmstmp = test_df_plot_1.iloc[:, 0].min().date()
        max_tmstmp = test_df_plot_1.iloc[:, 0].max().date()
        left = datetime.datetime.strptime(str(min_tmstmp), '%Y-%m-%d').date()
        right = datetime.datetime.strptime(str(max_tmstmp), '%Y-%m-%d').date()
        date_slider.value = (left, right)
        print(test_df_plot_1.shape[0])
        if test_df_plot_1.shape[0] > 1:
            LAYOUT.children[3] = create_figure(test_df_plot_1, \
                           title=option)
        else:
            LAYOUT.children[3] = create_figure(DUMMY_DF, \
                           title="No Data to Plot")
    else:
        print("blank selected!!")
        LAYOUT.children[3] = create_figure(DUMMY_DF, \
                       title="Nothing Selected..")

# callback for plot 3
def plot3_list_callback(attr, old, new):
    """Callback for the third plot.
    The plot changes based on option selected."""
    print(new)
    option = list_plot1.value
    if option != "":
        category = conn_obj.get_category_name(option)
        print("Equipment: ", category)
        print("selected channel name: ", option)
        test_df_plot_1 = conn_obj.get_fact(category=category, \
                                               selected_option=option)
        min_tmstmp = test_df_plot_1.iloc[:, 0].min().date()
        max_tmstmp = test_df_plot_1.iloc[:, 0].max().date()
        left = datetime.datetime.strptime(str(min_tmstmp), '%Y-%m-%d').date()
        right = datetime.datetime.strptime(str(max_tmstmp), '%Y-%m-%d').date()
        date_slider.value = (left, right)
        print(test_df_plot_1.shape[0])
        if test_df_plot_1.shape[0] > 1:
            LAYOUT.children[4] = create_figure(test_df_plot_1, \
                           title=option)
        else:
            LAYOUT.children[4] = create_figure(DUMMY_DF, \
                           title="No Data to Plot")
    else:
        print("blank selected!!")
        LAYOUT.children[4] = create_figure(DUMMY_DF, \
                       title="Nothing Selected..")


# callback for range button
def range_window_button_callback():
    """Callback for the range window selection 'OK' button.
    The plots change based on range selected."""
    print("button clicked")
    print("left slider:", date_slider.value_as_datetime[0], \
          " Right slider: ", date_slider.value_as_datetime[1])
    if list_plot1.value != "":
        start_range = str(date_slider.value_as_datetime[0])
        end_range = str(date_slider.value_as_datetime[1])
        category = conn_obj.get_category_name(list_plot1.value)
        test_df_plot_1 = conn_obj.get_fact_time_filtered(category, \
                                                      list_plot1.value, \
                                                      start_range, \
                                                      end_range)
        if test_df_plot_1.shape[0] > 1:
            LAYOUT.children[2] = create_figure(test_df_plot_1, \
                           title=list_plot1.value)
        else:
            LAYOUT.children[2] = create_figure(DUMMY_DF, \
                           title="No data to plot")
    else:
        print("blank selected!!")
        LAYOUT.children[2] = create_figure(DUMMY_DF, \
                           title="Nothing Selected..")
    if list_plot2.value != "":
        start_range = str(date_slider.value_as_datetime[0])
        end_range = str(date_slider.value_as_datetime[1])
        category = conn_obj.get_category_name(list_plot2.value)
        test_df_plot_2 = conn_obj.get_fact_time_filtered(category, \
                                                      list_plot2.value, \
                                                      start_range, \
                                                      end_range)
        if test_df_plot_2.shape[0] > 1:
            LAYOUT.children[3] = create_figure(test_df_plot_2, \
                           x_range=LAYOUT.children[2].x_range, \
                           title=list_plot2.value)
        else:
            LAYOUT.children[3] = create_figure(DUMMY_DF, \
                           title="No data to plot")
    else:
        print("blank selected!!")
        LAYOUT.children[3] = create_figure(DUMMY_DF, \
                           title="Nothing Selected..")
    if list_plot3.value != "":
        start_range = str(date_slider.value_as_datetime[0])
        end_range = str(date_slider.value_as_datetime[1])
        category = conn_obj.get_category_name(list_plot2.value)
        test_df_plot_3 = conn_obj.get_fact_time_filtered(category, \
                                                      list_plot3.value, \
                                                      start_range, \
                                                      end_range)
        if test_df_plot_2.shape[0] > 1:
            LAYOUT.children[4] = create_figure(test_df_plot_3, \
                           x_range=LAYOUT.children[2].x_range, \
                           title=list_plot3.value)
        else:
            LAYOUT.children[4] = create_figure(DUMMY_DF, \
                           title="No data to plot")
    else:
        print("blank selected!!")
        LAYOUT.children[4] = create_figure(DUMMY_DF, \
                           title="Nothing Selected..")


# callback calls
list_of_categories.on_change('active', category_callback)
list_plot1.on_change('value', plot1_list_callback)
list_plot2.on_change('value', plot2_list_callback)
list_plot3.on_change('value', plot3_list_callback)
range_window_button.on_click(range_window_button_callback)


#dummy df
DUMMY_DF = pd.DataFrame([['2012-05-01 00:00:00', 0], \
                         ['2012-05-01 01:00:00', 0]], \
        columns=list('01'))

with open(SCRIPT_DIRECTORY+'\\bokeh_html.html', 'r') as myfile:
    HTML=myfile.read().replace('\n', '')


DIV = Div(text=HTML)
THEME = Theme(filename= SCRIPT_DIRECTORY+"/theme.yaml")
DIV_LAYOUT = column(DIV, sizing_mode='scale_width')
CONTROLS = gridplot([[list_of_categories], \
                     [list_plot1,list_plot2,list_plot3], \
                     [date_slider,range_window_button], \
                        [None, None]],
                    toolbar_options=dict(logo=None))
LAYOUT_HTML = column(CONTROLS)
LAYOUT = column(DIV_LAYOUT, LAYOUT_HTML, create_figure(DUMMY_DF), create_figure(DUMMY_DF), create_figure(DUMMY_DF), sizing_mode='scale_width')
show(LAYOUT)
curdoc().title = "Bokeh Plotting Tool"
curdoc().theme = THEME
curdoc().add_root(LAYOUT)
