# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:54:13 2018

@author: STurlapati
"""
import pandas as pd
import psycopg2


class Connection():
    """ All Queries need to be written in this class here. 
    Any new query needs to be added as a function here."""
    # initialize the db configuration
    def __init__(self, dbname, user, host, password):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password

    # Creating connection
    def create_connection(self):
        """Connector function using psycopg2 and attributes"""
        dbname = "dbname = "+"'"+self.dbname+"' "
        user = "user = "+"'"+self.user+"' "
        host = "host = "+"'"+self.host+"' "
        password = "password = "+"'"+self.password+"' "
        connection_info = dbname + user + host + password
        try:
            conn = psycopg2.connect(connection_info)
        except psycopg2.Error:
            print("Unable to connect to DB")
        return conn
    
    #getting the categories
    def get_categories(self):
        conn = self.create_connection()
        query = "select distinct category from categories"
        eq_query = pd.read_sql(query, conn).iloc[:, 0].values.tolist()
        conn.close()
        return eq_query
    
    
    def get_category_list(self, category):
        """ Function for getting the list of categories using a query """
        try:
            conn = self.create_connection()
            query = """SELECT sub_category 
					  FROM categories
					  WHERE category = '%s'"""%(category)
            file_list = pd.read_sql(query, conn).iloc[:, 0].values.tolist()
            conn.close()
        except (psycopg2.Error, ValueError):
            print("Error at get_category_list, check connection or query")
        return file_list

    def get_category_name(self, selected_option):
        """ Function for getting a single category name using a query """
        try:
            conn = self.create_connection()
            query = """SELECT distinct category
					   FROM categories
					   WHERE sub_category = '%s'"""%(selected_option)
            equipment = pd.read_sql(query, conn).iloc[0, 0]
            conn.close()
        except (psycopg2.Error, ValueError):
            print("Error at get_category_name, check connection or query")
        return equipment

    
    def get_fact(self, category, selected_option):
        """ Function for getting the data for plotting using a query """
        try:
            conn = self.create_connection()
            query = """WITH sub_category_lookup AS (
								SELECT id 
								FROM categories 
								WHERE sub_category = '%s' 
								AND category = '%s')
                    		SELECT date_time, 
                            	data 
                    		FROM fact
                    		WHERE  category_id = (select category_id FROM sub_category_lookup)  
                    		ORDER BY date_time ; """%(selected_option, \
                            category)
            data_frame = pd.read_sql(query, conn)
            conn.close()
        except (psycopg2.Error, ValueError):
            print("Error at get_fact, check connection or query")
        return data_frame

    def get_fact_time_filtered(self, category, selected_option, \
                             start_tmstmp, \
                             end_tmstmp):
        """ Function for getting time filtered data for plotting using a query """
        try:
            conn = self.create_connection()
            query = """WITH sub_category_lookup AS (
								SELECT id 
								FROM categories 
								WHERE category = '%s' 
								AND sub_category = '%s')	
					   SELECT date_time,
							  data 
				       FROM fact
					   WHERE category_id = (select id FROM sub_category_lookup)  
					   AND (date_time>= '%s' AND date_time<'%s'	)				   
					   ORDER BY date_time ;"""%(category, selected_option, \
                        start_tmstmp, end_tmstmp)
                       
            data_frame = pd.read_sql(query, conn)
            print(query)
            conn.close()
        except (psycopg2.Error, ValueError):
            print("Error occured at get_fact_time_filtered, check connection or query")
        return data_frame        
        