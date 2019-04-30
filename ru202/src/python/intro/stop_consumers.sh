kill -9 `ps -ef|grep python|grep consumer.py|cut -f 3 -d ' '`
kill -9 `ps -ef|grep python|grep consumer-average.py|cut -f 3 -d ' '`
