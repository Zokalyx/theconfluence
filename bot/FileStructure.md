# File structure

Yes, I know, Sorry for writing 36 functions in random places. Here I am now, trying to fit them together, altough I'm probably not the best at this.

Here I list the files as imports, not necessarily reflecting their paths.

### Main

- Database Handler: Provides methods for connecting, reading and writing to db
- Comment Stream: Continually scans for comments, saving them in db
- Submission Stream: Continually scans for submissions, saving them in db. Look for the weekly Run post and save it in a variable
    - Run Parser: Process the new run info (update database and stuff)
    - Sub Manager: If wanted, update the flairs of the users in the server and remove/add users
- Inbox Stream: Continually scans for messages in inbox, calling methods from the following classes
    - Reminders: Provides methods related to the reminder system. Also, sends reminders each week
    - Run Calculator: Calculates who *should* be kicked from the sub and who should be added (using Redditor Queue) and posts the results
        - Redditor Queue: Continually picks random redditors, and provides a list of them when needed