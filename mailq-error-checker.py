"""Mailq Error Checker
Author: m4sc0t
Last Update: 2020-10-20

Script to parse mailq output.
When output contains some trigger from error_triggers file, 
email with output line will be sent to you.
"""
import sys
import subprocess
import smtplib
import os
import logging

logging.basicConfig(filename='/root/skripten/mailqchecker/debug-mailqchecker.log',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

def checkLastLog():

    output = mailqcheck('mailq')
    with open("/root/skripten/mailqchecker/last-check-result.txt", "r") as myfile:
        data = myfile.read()
    if str(data) == str(output):
        logging.debug('No new errors have been found since the last check.\n')
    else:
        logging.debug("New errors have been found since the last check. File last-check-result.txt will be overwritten.\n")
        f = open("/root/skripten/mailqchecker/last-check-result.txt", "w")
        f.write(str(output))
        f.close()
        notify_mail(output)

def mailqcheck(cmd):

    """Function to parse mailq output"""
    temp = subprocess.Popen([cmd], stdout=subprocess.PIPE)
    output = str(temp.communicate())
    output = output.split("\n")
    # TODO: find better way to do this
    # cut all new line symbols from output
    output = output[0].split('\\n\\n')
    # array to save result
    res = []
    # temp result (juggle with data)
    temp_res = []
    # array to store error triggers from file
    error_triggers = []

    with open('/root/skripten/mailqchecker/error_triggers') as error_triggers_file:
        for trigger_line in error_triggers_file:
            # cut new line symbol in array element
            trigger_line = trigger_line.rstrip()
            error_triggers.append(trigger_line)

    # write result in temp array res
    for output_line in output:
        temp_res.append(output_line)

    # check if some element from error_triggers occurs in an array temp_res
    for trigger in error_triggers:
        trigger_value = trigger
        for element in temp_res:
            if trigger_value in element:
                # cut new line and paste occurs element in final array res
                element = ' '.join(element.split()).replace("\\n", "")
                res.append(element)
                logging.debug(res)
    return res

def notify_mail(text):
    """Function to send mail with needed output"""

    SERVER = "SERVER ADRESS"
    FROM = "SERVER NAME HERE OR E-MAIL"
    TO = ['EMAIL']
    SUBJECT = "Error in mailq found"

    TEXT = text

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()


if __name__ == '__main__':
    checkLastLog()
