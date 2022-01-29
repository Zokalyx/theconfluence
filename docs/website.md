# Website - 29/1/2022

The website displays all sorts of data and tools related to the subreddit. Each section has its own directory, listed as titles below.

The website is written in vanilla HTML, CSS and JavaScript. Corresponding scripts to each section are written in Python.

## Rogue files

There are some files that do not have a specific directory.

- `index.html`: Must be in the top level directory for the website to be accessible via `zokalyx.github.io/theconfluence`, which is the shortest possible URL.
- `template.html`: Template containing the header and footer of the site
- `script.js`: Script common to all sections; adds the "X days since inception" in the top bar and also provides responsiveness to different screen sizes.
- `ideas.txt`: Cool features that could be added to the site.

## Activity

This section contains two spider charts, one of which shows the activity in the subreddit as a function of week day, and the other shows the same as a function of the hour of the day.

## Allgraph

This section produces the images in the colorful number timecourse.

Each image has two variants, one of which is high quality and the other is a preview.

## Anniversaries

This section provides a list of upcoming anniversaries and semiversaries.

These are the dates when a user has either stayed for exactly 6 months in the sub or N years.

## Converter

This section provides an interactive tool that converts between date, week number and run number.

## Leaderboard

This section contains the 1-200 list of all users in the sub and their flair numbers.

## Lowestleave

This section contains a lot of information regarding departures

As the name suggest, there is a list of people and graphs corresponding to the lowest number that appears in the departures of all weeks.

Additionally, there are graphs that represent subretention. Subretention is the same as [retention](#retention), but only considering users that have stayed for at least one full week.

## Map

This section has a map containing pins that represent the location of volunteer confluencers. The pins are anonymous.

The map is generated and populated using the [Google Maps API](https://developers.google.com/maps/documentation).

## Marbles

This section contains links to all marble races.

## Math

This section contains a mathematical analysis of retention in the sub. LaTeX is rendered using [MathJax](http://docs.mathjax.org/en/latest/).

## Noruns

This section contains links to posts in which there are explanations as to why a certain week did not have a run.

## Population

This section produces a graph that shows how many people there were in total in the sub at a given week.

## Retention

This section produces a graph that shows weekly retention. Retention is the percentage of users from the last run that did not leave in this run.

## Searchbyuser

This section provides an interactive tool to see the flair number history of any user in the sub.

The graph is created using [p5.js](https://p5js.org/reference/). Data is retrieved from directly from the repo using an Ajax request.

## Seniority

This section contains a variant of the leaderboard, which ignores "sloths", meaning that current users are sorted based on when they first joined the sub and not their current flair number.

## Time-stayed

This section contains statistics related to how many weeks users tend to stay in the sub.
