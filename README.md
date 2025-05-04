# Game_Analytics
## Problem Statement:

The SportRadar Event Explorer project aims to develop a comprehensive solution for managing, visualizing, and analyzing sports competition data extracted from the Sportradar API.

This application transforms raw JSON data into structured SQL tables and uses Streamlit to deliver an interactive dashboard. It enables users to explore rankings, competitor stats, venues, and more — making it an essential tool for sports enthusiasts, analysts, and organizations seeking deeper insights into competition structures and event trends.

## Features:

Parse JSON data from Sportradar API into structured Pandas DataFrames

Store and manage data using MySQL relational database,

Interactive Streamlit web application with multiple tabs:

Tennis Dashboard Overview

Search & Filter Competitors

Competitor & Country Analysis

Complexes & Venues Explorer

Custom SQL Query Executor

Cached loading for optimized performance
Clean UI with filters, sliders, and dynamic metric cards

## Stack	Tools

Backend : Python, SQLAlchemy, MySQL

Frontend : Streamlit

Data Parsing : JSON, Pandas

API Provider : Sportradar

## Project Structure

Game_Analytics/

│

├── app.py                    # Main Streamlit application

├── sql_queries.py            # Contains SQL queries categorized by topic

├── README.md                 # Project documentation

│
├── data/                     # Jupyter Notebooks for each dataset from API

│   ├── Competition.ipynb     # Parsing competitions and categories

│   ├── Complexes.ipynb       # Processing venues and complexes

│   ├── Competitor.ipynb      # Handling competitor and ranking data


## Contact

Have questions or ideas? Reach out at vishnumunnikrishnan@gmail.com


