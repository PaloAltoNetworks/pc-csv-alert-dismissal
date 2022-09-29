from operator import index
import loguru
from pcpi import session_loader

import sys


def dismiss(alert_ids, dismissal_note):
    payload = {
        "alerts":alert_ids,
        "dismissalNote":dismissal_note,
        "filter":{
            "timeRange":{"type":"to_now","value":"epoch"}
        }
    }
    loguru_logger.info(f'Dismissing alerts with note: {dismissal_note}')
    res = cspm_session.request('POST', '/alert/dismiss', json=payload)
    if res.status_code == 200:
        loguru_logger.info(f'Successfully dismissed {len(alert_ids)} alerts')


loguru_logger = loguru.logger

session_manager = session_loader.load_from_file(logger=loguru_logger)
cspm_session = session_manager.create_cspm_session()

filename = 'input.csv'
if '-file' in sys.argv:
    filename = sys.argv[sys.argv.index('-file')+1]

if '.csv' not in filename:
    loguru_logger.error('Invalid file format. Exiting...')
    exit()

#Open CSV and get alert IDs to dismiss
alerts = []
counter = 0
with open(filename, 'r') as infile:
    for line in infile:
        if counter == 0: #Skip headers line of file
            counter+=1
            continue

        a_id = line.split(',')[0].strip()
        d_note = line.split(',')[2].strip()

        alerts.append([a_id,d_note])

        counter+=1

#Break apart alerts based on dismissal note
alert_ids = []
chunk = []
curr_note = alerts[0][1]
index = 0
offset = 0
while index+offset < len(alerts):
    while True:
        alert_ids.append(alerts[offset+index][0])
        index+=1
        if offset+index >= len(alerts):
            dismiss(alert_ids, curr_note)
            break

        if curr_note != alerts[offset+index][1]:
            dismiss(alert_ids, curr_note)
            offset += index
            index = 0
            curr_note = alerts[offset+index][1]
            alert_ids = []
            break