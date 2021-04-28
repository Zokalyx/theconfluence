cd ..
cd website
cd leaderboard
copy /y names.txt "C:\Users\White Python\Desktop\Fran\ManimCE\leaderboard"
cd "C:\Users\White Python\Desktop\Fran\ManimCE\venv\Scripts"
call activate.bat
cd "C:\Users\White Python\Desktop\Fran\ManimCE\leaderboard"
call manim makevideo.py Render -qh -r 400,1200 --media_dir "C:\Users\White Python\Desktop\Fran\theconfluence\website\videos"
cd "C:\Users\White Python\Desktop\Fran\ManimCE\venv\Scripts"
call deactivate.bat
cd "C:\Users\White Python\Desktop\Fran\theconfluence\executables"
pause