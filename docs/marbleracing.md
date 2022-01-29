# Marble Racing - 29/1/2022

Marble racing is a minigame between members of The Confluence, in which they compete as marbles, using the Marbles On Stream game. Races are recorded and published on Youtube (unlisted) and the subreddit.

This is not a strictly necessary part of the project. It only contains utilities to facilitate the tracking of points and publishing the scoreboard.

## Season 1

Season 1 was very manual scoreboard-wise.

## Season 2

Season 2 contains a very useful python script which has the options to:

- Create a random list of names to test races and saves it to `random.csv`
- Creates a list of competitors and save it in `competitors.csv`, filtering the ones that have stayed for at least one week
- Reads the results of a race (`results.txt`) and updates `scoreboard.json`
- Removes the last race from the scoreboard
- Saves files, including `scoreboard.xlsx`
- Make a backup in `backup.json` and clear every file
- Automatically type the custom scores into Marbles On Strem
- Automatically click for setting configurations inside of Marbles On Stream
- Execute a debugging function
- Toggle test mode ON or OFF
- Show help
- Quit

The pretty scoreboard that can be published in Google Sheets is saved in `scoreboard.xlsx`.

## Season 3

There are currently no plans for season 3.
