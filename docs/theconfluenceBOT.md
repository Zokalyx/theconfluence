# Bot - 30/1/2022

[The Confluence Bot](https://www.reddit.com/user/TheconfluenceBOT) is a Reddit bot that checks which users did not comment or post during the last week. Additionally, it picks random users to be invited into the subreddit.

The bot has a [details and FAQ](https://www.reddit.com/user/theconfluenceBOT/comments/ks2m4w/instructions_and_faq/) post.

## New bot

New bot is in development. Read the latest [new design draft](https://github.com/Zokalyx/theconfluence/blob/main/theconfluenceBOT/newdesign.md).

## Instructions

The bot will respond to users in the `DEBUGGERS` or `WHITELIST` lists. If a user belongs to the former, it will execute a dry run, and no posts will be submitted, unless the body of the message or its title contains the keyword `official`. Official runs result in new posts.

## Arrivals

The selection process is random, but it follows an algorithm:

![Arrivals](https://i.imgur.com/lWHrfAN.jpeg)

Additionally, 10 random people are chosen just in case.

The posts in which these users are found are posted in the "Detailed arrivals" posts.

## Departures

The departure process follows an algorithm too:

![Departures](https://i.imgur.com/P3BTMKJ.jpeg)

Departures are only shown in the run summary.

## New flairs

For convenience, the new flair numbers of all users is posted in the "New flairs for old users" posts.

## Summary

The summary should contain all the information that has to be posted on the weekly run posts.

- Retention
- List of departures
- List of arrivals

They need not contain detailed information.