cd graphs
cd leaderboard
call python -m checkcomment
call python -m htmlcreator
cd ..
cd ..
call git add .
call git commit -m "Checked comments and posts"
call git push
pause