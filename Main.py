# This is a sample Python script.

import logging
import sys
import datetime
import certstream
from DBHelper import DBHelper



# Filters
f = open('filters_include.txt') # Open file on read mode
filters_include_list = f.read().splitlines() # List with stripped line-breaks
f.close() # Close file
filters_include_length = len(filters_include_list)

print("Lenght=", filters_include_length);
#print("Filters=", filters_include)
for filter in filters_include_list:
  print(filter)


def print_callback(message, context):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]


        # Check filters
        check_if_in_filter = any(substring in domain for substring in filters_include_list)
        if check_if_in_filter:
            print(domain)
            #sys.stdout.write("FOUND", u"[{}] {} (SAN: {})\n".format(datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), domain, ", ".join(message['data']['leaf_cert']['all_domains'][1:])))

        sys.stdout.flush()

# MariaDB
domain = "Rrr"
db = DBHelper('localhost', 'root', '', 'quick')
q = "INSERT INTO `q_domains_monitoring_domains_filtered` (`filtered_id`, `filtered_domain_value`) VALUES (NULL, ", domain, ")"
db.query(q)

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')