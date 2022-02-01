-- Queries for various purposes

-- Get current members
SELECT * FROM redditors WHERE member = TRUE;

-- Get specific member
SELECT * FROM redditors WHERE redditId = "k0irn";

-- Get members with reminder subscription
SELECT * FROM redditors WHERE member = TRUE AND reminder = TRUE;

-- Get last comment from redditor
SELECT * FROM comments WHERE authorId = "k0irn" ORDER BY createdUtc DESC LIMIT 1;

-- Get last post from redditor
SELECT * FROM submissions WHERE authorId = "k0irn" ORDER BY createdUtc DESC LIMIT 1;

-- Get oldest comment from redditor
SELECT * FROM comments WHERE authorId = "k0irn" ORDER BY createdUtc ASC LIMIT 1;

-- Get oldest post from redditor
SELECT * FROM submissions WHERE authorId = "k0irn" ORDER BY createdUtc DESC LIMIT 1;