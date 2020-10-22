# mailq-error-checker

small python script to parse mailq output for errors by keywords/triggers and notify admin.

Use error_triggers file to add more triggers. newline = new trigger

```
$:~/mailq-error-checker# cat error_triggers
certificate
TLS
tls
SOME NEW TRIGGER HIER
```

to check errors every 30 min add 
```
*/30 * * * *    /usr/bin/python3 /PATH TO SKRIPT/mailq-error-checker.py
```
to cron.

