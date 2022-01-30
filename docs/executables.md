# Executables - 29/1/2022

The `/executables` directory contains batch files which facilitate the execution of many python scripts.

- `checkcomments.bat`: runs the `checkcomments` script and later runs the script to update the HTML in the webpage.
- `createbasic.bat`: Runs the scripts to create `pro.csv` and `probyuser.csv`
- `gitpush.bat`: Adds every new file to the git repo, asks for a commit message and commits, and then pushes to master.
- `updatevideo.bat`: Runs [manim](https://www.manim.community) to create the video that is seen in the home page of the website. This should only be run whenever the top 5 of the sub changes.
- `retrieverun.bat`: Runs the scripts that retrieve arrivals and departures from the last weekly post in the sub. Also, this updates the `week.txt` file.
- `updateactivity.bat`: Updates the activity graph of the website. Since this takes a long time, this script should be run once in a while.
- `updatelast.bat`: Runs the `updatelast.py` script to update the "Last" post of the bot.
- `updatewebsite.bat`: Runs all the scripts corresponding to all website sections, except for the activity chart.

There are also more executables that are so commonly used that they're in the top level directory:

- `retrieve.bat`: Same as `retrieverun.bat`.
- `master.bat`: Retrieves data, updates the bot, processes the data, updates the website and posts.
- `noretrieve.bat`: Same as `master.bat`, but does not retrieve data. This is used when retrieval is unsuccessful and it had to be done manually. In that case, `week.txt` must be updated manually.