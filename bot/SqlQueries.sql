-- Queries for various purposes

-- Get current members
SELECT * FROM redditors WHERE member = TRUE

-- Get specific member
SELECT * FROM redditors WHERE redditId = %s

-- Get members with reminder subscription
SELECT * FROM redditors WHERE member = TRUE AND reminder = TRUE

-- Get last comment from redditor
SELECT * FROM comments WHERE authorId = %s ORDER BY createdUtc DESC LIMIT 1

-- Get last post from redditor
SELECT * FROM submissions WHERE authorId = %s ORDER BY createdUtc DESC LIMIT 1

-- Get oldest comment from redditor
SELECT * FROM comments WHERE authorId = %s ORDER BY createdUtc ASC LIMIT 1

-- Get oldest post from redditor
SELECT * FROM submissions WHERE authorId = %s ORDER BY createdUtc DESC LIMIT 1

-- Add reminder to user
UPDATE redditors SET reminder = TRUE WHERE redditID = %s

-- Remove reminder from user
UPDATE redditors SET reminder = FALSE WHERE redditID = %s