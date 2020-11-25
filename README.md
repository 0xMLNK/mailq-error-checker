# mailqchecker

Skript um zu Errors in mailq zu prüfen. 

Um Trigger list anzupassen, einfach in error_trigers file trigger als newline 
hinzufügen. 

```
root@vm-mail-gw:~/skripten/mailqchecker# cat error_triggers
certificate
TLS
tls
SOME NEW TRIGGER HIER
```
kann auch Satz sein. newline = newtrigger


um folgende skript in cron hinzufügen.

```
vim /etc/crontab
```
und am Ende 
```
*/10 * * * *    python3 /root/skripten/mailqchecker/mailqcheck.py
```
hinzufügen.
danach cron reloaden.
```
/etc/init.de/cron reload
```

## NOTE:
use full path to file or add skript folder to CRON PATH!
