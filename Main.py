###
#
# File: Main.py
# Version 1.0.0
# Date 14:28 25.03.2021
# Copyright (c) 2021 Sindre Andre Ditlefsen
# License: http://opensource.org/licenses/gpl-license.php GNU Public License
#
###

import logging
import sys
import time
import certstream # pip install certstream
from DBAdapter import DBAdapter
from tldextract import extract
import os.path
from pygame import mixer # pip install pygame
from ReadFilesToList import ReadFilesToList
import re
import datetime



# Create tables ---------------------------------------------------------------------------------
def createTables():
    # MySQL create table
    db = DBAdapter('localhost', 'root', '', 'quick')
    db.open()

    domains_filtered = (
        "CREATE TABLE IF NOT EXISTS `q_domains_monitoring_domains_filtered` ( "
        "`filtered_id` int(11) NOT NULL AUTO_INCREMENT, "
        "`filtered_domain_id` int(11) DEFAULT NULL, "
        "`filtered_domain_value` varchar(200) DEFAULT NULL, "
        "`filtered_group_id` int(11) DEFAULT NULL, "
        "`filtered_by_user_id` int(11) DEFAULT NULL, "
        "`filtered_date` date DEFAULT NULL, "
        "`filtered_date_saying` varchar(100) DEFAULT NULL, "
        "`filtered_datetime` datetime DEFAULT NULL, "
        "`filtered_domain_sld` varchar(200) DEFAULT NULL, "
        "`filtered_domain_tld` varchar(20) DEFAULT NULL, "
        "`filtered_domain_sld_length` int(11) DEFAULT NULL, "
        "`filtered_score` int(11) DEFAULT NULL, "
        "`filtered_domain_registered_date` date DEFAULT NULL, "
        "`filtered_domain_registered_date_saying` varchar(100) DEFAULT NULL, "
        "`filtered_domain_registered_datetime` datetime DEFAULT NULL, "
        "`filtered_domain_seen_before_times` int(11) DEFAULT NULL, "
        "`filtered_domain_ip` varchar(100) DEFAULT NULL, "
        "`filtered_domain_host_addr` varchar(100) DEFAULT NULL, "
        "`filtered_domain_host_name` varchar(100) DEFAULT NULL, "
        "`filtered_domain_host_url` varchar(100) DEFAULT NULL, "
        "`filtered_domain_filters_activated` varchar(100) DEFAULT NULL, "
        "`filtered_domain_seen_by_group` int(11) DEFAULT NULL, "
        "`filtered_domain_emailed` int(11) DEFAULT NULL, "
        "`filtered_notes` varchar(200) DEFAULT NULL, "
        " PRIMARY KEY (`filtered_id`) "
        " ) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;")

    db.createTable(domains_filtered)

    db.close()

# Print callback ------------------------------------------------------------------------------------
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

        # Print domains
        #sys.stdout.write(u"[{}] {} (SAN: {})\n".format(datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), domain, ", ".join(message['data']['leaf_cert']['all_domains'][1:])))
        #sys.stdout.flush()


        # Remove www.
        domain_len = len(domain)
        if(domain_len > 4):
            check_for_www = domain[ 0 : 4 ]
            if(check_for_www == "www."):
                domain = domain[4:]



        # Check filters
        for line in filters_list():
            array = line.split("|")
            keyword = array[0]
            type = array[1]
            title = array[2]
            tld = array[3]

            # Domain tld check (example .com)
            check_domain = 0
            if (tld == "" or tld == "*"):
                check_domain = 1
            else:
                domain_tld = domain.split(".")[-1]
                filter_tlds_array = tld.split(",")
                for t in filter_tlds_array:
                    if t in domain_tld:
                        check_domain = 1

            if(check_domain == 1):
                # print("Checking domain " + domain);

                # Regex, Contains
                if (type == "regex"):
                    if re.match(keyword, domain):
                        print(domain + " (" + type + " " + keyword + ")")
                        insertDomain(domain, type + " " + keyword)
                elif (type == "contains"): # Contains
                    if keyword in domain:
                        print(domain + " (" + type + " " + keyword + ")")
                        insertDomain(domain, type + " " + keyword)
                # elifcontains
            # check_domain == 1

        # for line in filters_list

        sys.stdout.flush()


# Insert domain ------------------------------------------------------------------------------------
def insertDomain(domain, filter_activated):

    # MySQL Insert
    db = DBAdapter('localhost', 'root', '', 'quick')
    db.open()

    inp_date = time.strftime("%Y-%m-%d")
    inp_date_saying = time.strftime("%d %b %Y") # 5 Nov 2021
    inp_datetime = time.strftime("%Y-%m-%d %H:%M")

    # Domain sld
    tsd, td, tsu = extract(domain)  # prints abc, hostname, com from abc.hostname.com
    inp_domain_sld = td
    if(tsd != ""):
        inp_domain_sld = tsd + "." + td

    inp_domain_tld = tsu

    inp_domain_sld_length = len(inp_domain_sld)

    # Check for duplicates
    conditional_query = 'filtered_domain_value = %s '
    result = db.select('q_domains_monitoring_domains_filtered', conditional_query, 'filtered_id',
                       'filtered_domain_value', filtered_domain_value=domain)
    result_len = len(result)
    # print("result_len=" + str(result_len))
    if(result_len == 0):
        # No duplicate, insert
        last_row_id= db.lastRowId("q_domains_monitoring_domains_filtered")
        add = ("INSERT INTO q_domains_monitoring_domains_filtered "
                        "(filtered_id, filtered_domain_value, filtered_date, filtered_date_saying, filtered_datetime, "
                        "filtered_domain_sld, filtered_domain_tld, filtered_domain_sld_length, filtered_score, filtered_domain_registered_date, "
                        "filtered_domain_registered_date_saying, filtered_domain_registered_datetime, filtered_domain_seen_before_times, filtered_domain_ip, filtered_domain_host_addr,"
                        "filtered_domain_host_name, filtered_domain_host_url, filtered_domain_filters_activated, filtered_domain_seen_by_group, filtered_domain_emailed,"
                       "filtered_notes) "
                        "VALUES (%s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, "
                       "%s)")
        data = (last_row_id, domain, inp_date, inp_date_saying, inp_datetime,
                inp_domain_sld, inp_domain_tld, inp_domain_sld_length, 20, inp_date,
                inp_date_saying, inp_datetime, -1, '', '',
                '', '', filter_activated, 0, 0,
                "Python")
        db.insert(add, data)

        # Notify
        #soundName = "./sound/" + "note" + ".mp3"
        #mixer.init()
        #mixer.music.load(soundName)
        #mixer.music.play()


    db.close()




# Scriptstart ------------------------------------------------------------------------------------

# Create db tables
createTables()

# Read filters
filters_list = ReadFilesToList()

# Start logging
logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)
certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')

