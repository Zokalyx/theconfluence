# Data - 29/1/2021

The `/data` directory contains the data corresponding to all arrivals and departures, plus a handful of related scripts.
This scripts always generate every file starting from week 1, which means that deleting current `.csv` files won't cause any issues.

The following titles correspond to each subdirectory.

# Common files

There are currently four files that aren't placed inside of a specific folder because they are used by all of the scripts here.

- `broken.txt`: contains the numbers corresponding to weeks that did not have a run
- `notes.txt`: has a "detective log" of past issues with the `.csv` files
- `shh.txt`: has keys used to log in to Reddit - this file must be `.gitignore`d
- `week.txt`: has the number of the current week

# Arrivals

Arrivals are the new users of each run. Their raw data is stored in individual `.txt` files, one for each week. Weeks that didn't have a run have empty files. The format of each file should be:

```
1 Name1

2 Name2

3 Name3
```

This is how the weekly posts are formatted in the subreddit.

Note: some of the first `.txt` files contain a dot right next to each number - although this is not recommended to be used, the script that processes these files can handle them.

# Departures

Departures are stored in a similar way to arrivals.

# Basic

The `/basic` directory contains scripts and `.csv` files related to processed arrivals and departures that is generally useful for the rest of the system.

## Retrieval

The weekly retrieval of arrivals and departures can be done with `retrieverun.py`, which looks for the corresponding post in the subreddit and tries to extract the relevant lists of names.

## Raw data

`rawcreator.py` is a script that creates the `raw.csv` file based on all of the arrivals and departures mentioned before.

The format of `raw.csv` is the following:

```
1,2,3,4,5,...
departure1,departure2,departure3,...
1,2,3,4,5,...
arrival1,arrival2,arrival3,...
```

And this is repeated for all weeks. Weeks with no runs have corresponding to empty lines in the file.

## Processed data

`procreator.py` creates `pro.csv` using the `raw.csv` file, which is formatted in the following way:

```
1,name1,name1,name1,name2...
2,name2,name2,name2,name4...
3,name3,name4,name4,name5...
```

Where the first column corresponds to the *flair number* of the user, and the other columns corresponding to the user holding that number in any given week. This means that this file grows *horizontally*... (😅)

## Processed by user data

The last file allows for quickly knowing which user had a specific flair at a given week. To perform the opposite calculation (to know which flair corresponded to a user), the following file is more useful (`probyuser.csv`, generated by `probyusercreator.py`, using `pro.csv`):

```
name1,1,1,1,0,0,0,...
name2,2,2,2,1,1,1,...
name3,3,0,0,0,0,0,...
name4,4,3,3,2,2,2,...
```

Where each row corresponds to the flair number of a specific user in a given week. `0` means that they are not a member anymore.

# Misc

The miscellaneous folder (for lack of a better word) contains various scripts with different utilites.

## Update last

`updatelast.py` updates the post named "Last" of the bot so that it can use it next time it is called. The title of the post is accompanied by the run number. This post contains a list of all current members and their flair number.

## Time machine

The time machine is actually a part of the website, so code might as well be moved to `/website/searchbyuser` (TODO?).

`timemachinecreator.py` scrapes from all the posts of every user and looks for the oldest one that they posted in The Confluence. The same is done with comments (only in posts inside of the subreddit). The time and date of these oldest posts and comments is saved in `timemachine.csv`.

The reason why the subreddit is not directly scraped is because [it's not possible to go over 1000 posts](https://praw.readthedocs.io/en/latest/code_overview/other/listinggenerator.html?highlight=1000) in a specific subreddit or user. But since users generally have less than 1000 posts in all of their history within the sub, that's a useful workaround.

The columns of the file are:

```
username, oldest post ID, oldest post time, oldest comment post ID, oldest comment time, oldest comment ID
```

Time is stored as UNIX time and the ID's are used to create the corresponding URLs.

In practice, `timemachinecreator.py` should not be always used
since it may take hours to complete the process. On a weekly basis, `updatepostsandtimemachine.py` should be used, which only scans the last 200 posts and adds the new data to the csv - it'd be really rare for someone to do their first comment on a really old post.

## Posts

All posts are "saved" in `posts.csv`. The process of creating this file is similar to that of the time machine. One can create the file for the first time using `postfinder.py`, but to update it, `updatepostsandtimemachine.py` should be used.

The columns of the file are:

```
post ID, post time, post title, poster
```

Since this might reveal potentially sensitive information in the titles, this file should be `.gitignore`d.

## Script updater

The website has a little counter at the top that shows how many days have passed since the very first run. This is calculated using javascript, but the javascript file needs to know which week we're on. `scriptupdater.py` simply opens `script.js` and updates the first line.

## Name corrector

`namecorrector.py` is a standalone script which goes over every name in `pro.csv` and tries to fix capitalization mistakes (`Zoka` vs `zoka`) in the arrivals and departures files. The results are printed on the console.

## Check comment

`checkcomment.py` checks if a user commented since the last run started and saves the results in `commented.csv`. **This file is not currently used**, it was used to show in the website a checkmark next to users that did comment. But this required being run manually and it was not very practical.