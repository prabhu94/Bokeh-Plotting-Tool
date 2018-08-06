# Bokeh Plotting Tool 

This is a repository which contains code that can help any user understand the different features that bokeh provides for data visualizations. In this code, I am essentially introducing new users to the bokeh visualization package and the Postgres DB, and how to connect these and develop a web-application which is hosted on the server that Bokeh provides.

## 1. Software Requirement
* Postgres 10 Database
* Python 3.6
* Bokeh 0.12 + 
* psycopg2

## 2. The Data

To create a mock database I used data from the datamarket website, which was available for public use. The data is essentially weather data of a region, which I manipulated for the purposes of this tutorial.

## 3. Building the tool

There are three tasks that are essential to completing this tool:

* Building the database 
* Building the bokeh interface in python 
* Deploying using the bokeh server

## 3. Deployment

Deployment can be done remotely using the ` bokeh serve ` command.

## References:

* https://datamarket.com/
* https://bokeh.pydata.org
* http://initd.org/psycopg/
* https://www.postgresql.org/
