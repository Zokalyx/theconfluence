# Documentation - 29/1/2022

# Workflow

The process in which scripts are executed is the following:

1. The bot is called and publishes the results on its profile page
2. The results are used to remove and add users manually
3. The official list of departures and arrivals is posted
4. The post is scraped manually or automatically to save the lists in the `/data` directory
5. The data is processed to generate useful `.csv` files
6. The bot publishes the current members in its profile page as a means of data storage
7. Each webpage section has its script run, which updates images or other information for the site
8. Repeat weekly

# Stack

The whole process is very manual in many ways, and tools are not optimal:
- The website is hosted on Github pages, which means that it is static and does not support templates, databases and other useful tools
- The scripts have to be run manually - although this is made easy by using batch files
- Scripts are written in Python. Each file should be run in the directory its in.
- The bot is hosted on Heroku, which does not have a permanent file system (a remote database should be used if we needed to)

# Notes

- It's important to distinguish from week and run number. There are many weeks in which a run did not happen. As a rule of thumb, all files use weeks and not runs.
- All docs have their time of last update in their titles.
