# mailqchecker

Script to check errors in mailq.

To adjust the trigger list, just add trigger as newline in error_trigers file. 
```
root@mail:~/mailqchecker# cat error_triggers
certificate
TLS
tls
SOME NEW TRIGGER HIER
```
to add the following script in cron.
```
vim /etc/crontab
```
and add this line to the end of crontab
```
*/10 * * * *    python3 /PATH TO SCRIPT/mailqchecker/mailqcheck.py
```
reload cron.
```
/etc/init.de/cron reload
```

## NOTE:
use full path to file or add skript folder to CRON PATH!
