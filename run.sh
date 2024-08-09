nohup python app_chat1.py >logs/log/logs.txt 2>&1 & echo $! > logs/pid/run.pid
nohup python app_chat2.py >logs/log/logs2.txt 2>&1 & echo $! > logs/pid/run2.pid
