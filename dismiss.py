import loguru
from pcpi import session_loader

import sys

loguru_logger = loguru.logger

session_manager = session_loader.load_from_env(logger=loguru_logger)
cspm_session = session_manager.create_cspm_session()

filename = 'in.csv'
if '-file' in sys.argv:
    filename = sys.argv[sys.argv.index('-file')+1]

if '.csv' not in filename:
    loguru_logger.error('Invalid file format. Exiting...')
    exit()

#Open CSV and get alert IDs to dismiss
alert_ids = []
with open(filename, 'r') as infile:
    for line in infile:
        if 'I-' not in line.split(',')[0]:
            continue
        a_id = line.split(',')[0].strip()
        print(a_id)
        alert_ids.append(a_id)

payload = {
    "alerts":alert_ids,
    "dismissalNote":"DISMISSAL SCRIPT",
    "filter":{
        "timeRange":{"type":"to_now","value":"epoch"}
    }
}

loguru_logger.info(f'Dismissing alerts')
res = cspm_session.request('POST', '/alert/dismiss', json=payload)

if res.status_code == 200:
    loguru_logger.info(f'Successfully dismissed {len(alert_ids)} alerts')

###
