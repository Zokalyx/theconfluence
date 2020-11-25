cd leaderboard
python -m htmlcreator
call rendervideo.bat
cd ..\retention
python -m creategraph
cd ..\population
python -m creategraph
cd ..\time-stayed
python -m creategraph
python -m creategraph2
pause