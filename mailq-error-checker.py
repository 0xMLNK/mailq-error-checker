"""Mailq Error Checker
Author: @derMelnik

Script to parse mailq output.
When output contains some trigger from error_triggers file, 
email with output line will be sent to you.
"""

import subprocess
import logging
import smtplib
import os

#for crontab use full path to file
logging.basicConfig(filename='debug-mailq-error-checker.log', 
                    format='%(asctime)s:%(levelname)s:%(message)s', 
                    level=logging.DEBUG)

def mailqcheck(cmd):
    """Function to parse mailq output"""

    temp = subprocess.Popen([cmd], stdout=subprocess.PIPE)
    output = str(temp.communicate())
    output = output.split("\n")
    # TODO: find better way to do this
    # cut all new line symbols from output
    output = output[0].split('\\n\\n')
    #array to save result
    res = []
    #tempory result (juggle with data)
    temp_res = []
    #array to store error triggers from file        
    error_triggers = []
    
    #for crontab use full path to file
    with open('error_triggers') as error_triggers_file:
        for trigger_line in error_triggers_file:
            #cut new line symbol in array element
            trigger_line = trigger_line.rstrip()
            error_triggers.append(trigger_line)

    #write result in temp array res
    for output_line in output:
          temp_res.append(output_line)
          
    #check if some element from error_triggers occurs in an array temp_res
    for trigger in error_triggers:
        trigger_value = trigger
        for element in temp_res:
            if trigger_value in element:
                #cut new line and paste occurs element in final array res
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
    
    #if array is not empty send mail otherwise write into log
    res_arr = mailqcheck('mailq')
    if not res_arr:
        logging.debug('No problems with defined triggers found.')
    else:
        notify_mail(res_arr)
