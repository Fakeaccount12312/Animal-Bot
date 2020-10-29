pkill -f bot.py
pkill -f leafman_bot.py
sleep 10s
git pull
sleep 10s
python3 bot.py -u &>> log.txt &
sleep 10s
python3 leafman_bot.py -u &>> log.txt &