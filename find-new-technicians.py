#!/usr/bin/env python3
#!./.venv/Scripts/python.exe

__author__ = "Jared Bloomer, KW4JLB"
__copyright__ = "Copyright 2025, KW4JLB"
__credits__ = ["Jared Bloomer, KW4JLB"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jared Bloomer"
__email__ = "kw4jlb@arrl.net"
__status__ = "Production"

import sys
import argparse
import logging
import requests
import zipfile
import io
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def log(message, level='info'):
  if sys.stdout.isatty():
    match level:
      case 'notset':
        logger.info(message)
        print("INFO: " + message)
      case 'info':
        logger.info(message)
        print("INFO: " + message)
      case 'debug':
        logger.debug(message)
        print("DEBUG: " + message)
      case 'warning':
        logger.warning(message)
        print("WARNING: " + message)
      case 'error':
        logger.error(message)
        print("ERROR: " + message)
      case 'critical':
        logger.critical(message)
        print("CRITICAL: " + message)
  else:
    match level:
      case 'notset':
        logger.info(message)
      case 'info':
        logger.info(message)
      case 'debug':
        logger.debug(message)
      case 'warning':
        logger.warning(message)
      case 'error':
        logger.error(message)
      case 'critical':
        logger.critical(message)

def log_header():
  logger.info(" ___                                    ___ ___      ")
  logger.info("(   )                                  (   (   )     ")
  logger.info(" | |   ___ ___  ___  ___    ,--.     .-.| | | |.-.   ")
  logger.info(" | |  (   (   )(   )(   )  /   |    ( __| | | /   \  ")
  logger.info(" | |  ' /  | |  | |  | |  / .' |    (''\"| | |  .-. | ")
  logger.info(" | |,' /   | |  | |  | | / / | |     | || | | |  | | ")
  logger.info(" | .  '.   | |  | |  | |/ /  | |     | || | | |  | | ")
  logger.info(" | | `. \  | |  | |  | /  `--' |-.   | || | | |  | | ")
  logger.info(" | |   \ \ | |  ; '  | `-----| |-'   | || | | '  | | ")
  logger.info(" | |    \ .' `-'   `-' '     | | ___ | || | ' `-' ;  ")
  logger.info("(___ ) (___)'.__.'.__.'     (___(   )' (___) `.__.   ")
  logger.info("                                 ; `-' '             ")
  logger.info("                                  .__.'              ")

def getargs():
  parser = argparse.ArgumentParser(
    prog='',
    description='Search the FCC ULS to find newly licensed individuals',
    epilog='Developed and maintained by KW4JLB.'
  )

  parser.add_argument('-z', '--zipcode', nargs='+', action='store', help='What Zip Code To Search')
  parser.add_argument('-m', '--months', nargs='+', action='store', help='How Many Months from today to search for')

  return parser.parse_args()

def get_licenses():
  log('Downloading License Database')
  DATABASE_URL='https://data.fcc.gov/download/pub/uls/complete/l_amat.zip'
  db = requests.get(DATABASE_URL, stream=True)
  file = zipfile.ZipFile(io.BytesIO(db.content))
  file.extractall("./license_db")
  log('Download Complete')

def get_callsigns_by_zipcode(zip_code):
  log("Reading Database of Callsigns")
  en_headers=['record_type', 'unique_system_id', 'uls_file_no', 'ebf_no', 'call', 'entity_type', 'license_id', 'entity_name', 'first_name', 'middle_initial', 'last_name', 'suffix', 'phone', 'fax', 'email', 'address', 'city', 'state', 'zip', 'po_box', 'attn_line', 'sgin', 'frn', 'applicant_type_code', 'applicant_type_code_other', 'status_code', 'status_date', '37ghz_license_type', 'linked_unique_system_id', 'linked_call']
  en_dtypes = {
    'record_type': "string",
    'unique_system_id': "int",
    'uls_file_no': "string",
    'ebf_no': "string",
    'call': "string",
    'entity_type': "string",
    'license_id': "string",
    'entity_name': "string",
    'first_name': "string",
    'middle_initial': "string",
    'last_name': "string",
    'suffix': "string",
    'phone': "string",
    'fax': "string",
    'email': "string",
    'address': "string",
    'city': "string",
    'state': "string",
    'zip': "string",
    'po_box': "string",
    'attn_line': "string",
    'sgin': "string",
    'frn': "string",
    'applicant_type_code': "string",
    'applicant_type_code_other': "string",
    'status_code': "string",
    'status_date': "string",
    '37ghz_license_type': "string",
    'linked_unique_system_id': "string",
    'linked_call': "string"
  }

  en = pd.read_csv(
    'license_db/EN.dat',
    header=29,
    delimiter='|',
    names=en_headers,
    dtype=en_dtypes
  )

  log("Searching for Callsigns in Georgia")
  ga_calls=en[en['city'] == 'GA']

  log("Finding Callsigns in Zip Code: " + str(zip_code))
  zip_calls = ga_calls[ga_calls['state'].str.contains(str(zip_code))]
  
  return zip_calls

def search_calls(zip_calls):
  log("Collecting Callsign Information") 
  hd_headers = ['record_type', 'unique_system_id', 'uls_file_no', 'ebf_no', 'call', 'license_status', 'radio_service_code', 'grant_date', 'expired_date', 'cancellation_date', 'eligibility_rule_num', 'reserved', 'alien', 'alien_government', 'alien_corporation', 'alien_officer', 'alien_control', 'revoked', 'convicted', 'adjudged', 'ara', 'common_carrier', 'non_common_carrier', 'private_comm', 'fixed', 'mobile', 'radiolocation', 'satellite', 'developmental_or_sta', 'interconnected_service', 'certifier_first_name', 'certifier_mi', 'certifier_last_name', 'certifier_suffix', 'certifier_title', 'female', 'african_american', 'native_american', 'hawaiian', 'asian', 'white', 'hispanic', 'effective_date', 'last_action_date', 'auction_id', 'reg_stat_broad_serv', 'band_manager', 'type_serv', 'alien_ruling', 'licensee_name_change', 'whitespace_indicator', 'op_performace_requirement_choice', 'op_performace_requirement_answer', 'discontinuation_of_service', 'regulatory_compliance', '900mhz_eligible_certification', '900mhz_transition_plan_certification', '900mhz_return_spectrum_certification', '900mhz_payment_certification']
  hd_dtypes = {
    'record_type': "string",
    'unique_system_id': "int",
    'uls_file_no': "string",
    'ebf_no': "string",
    'call': "string",
    'license_status': "string",
    'radio_service_code': "string",
    'grant_date': "string",
    'expired_date': "string",
    'cancellation_date': "string",
    'eligibility_rule_num': "string",
    'reserved': "string",
    'alien': "string",
    'alien_government': "string",
    'alien_corporation': "string",
    'alien_officer': "string",
    'alien_control': "string",
    'revoked': "string",
    'convicted': "string",
    'adjudged': "string",
    'ara': "string",
    'common_carrier': "string",
    'non_common_carrier': "string",
    'private_comm': "string",
    'fixed': "string",
    'mobile': "string",
    'radiolocation': "string",
    'satellite': "string",
    'developmental_or_sta': "string",
    'interconnected_service': "string",
    'certifier_first_name': "string",
    'certifier_mi': "string",
    'certifier_last_name': "string",
    'certifier_suffix': "string",
    'certifier_title': "string",
    'female': "string",
    'african_american': "string",
    'native_american': "string",
    'hawaiian': "string",
    'asian': "string",
    'white': "string",
    'hispanic': "string",
    'effective_date': "string",
    'last_action_date': "string",
    'auction_id': "string",
    'reg_stat_broad_serv': "string",
    'band_manager': "string",
    'type_serv': "string",
    'alien_ruling': "string",
    'licensee_name_change': "string",
    'whitespace_indicator': "string",
    'op_performace_requirement_choice': "string",
    'op_performace_requirement_answer': "string",
    'discontinuation_of_service': "string",
    'regulatory_compliance': "string",
    '900mhz_eligible_certification': "string",
    '900mhz_transition_plan_certification': "string",
    '900mhz_return_spectrum_certification': "string",
    '900mhz_payment_certification': "string"
  }

  hd = pd.read_csv(
    'license_db/HD.dat',
    header=59,
    delimiter='|',
    names=hd_headers,
    dtype=hd_dtypes,
    na_values = "0"
  )

  log("Filtering results for Technician Licenses")
  technicians=hd[['call', 'license_status', 'grant_date', 'expired_date', 'cancellation_date', 'certifier_first_name', 'certifier_mi', 'certifier_last_name', 'certifier_suffix']].query('license_status == "T"')

  zip_calls_headers = ['record_type', 'unique_system_id', 'uls_file_no', 'ebf_no', 'call', 'entity_type', 'license_id', 'entity_name', 'first_name', 'middle_initial', 'last_name', 'suffix', 'phone', 'fax', 'email', 'address', 'city', 'state', 'zip', 'po_box', 'attn_line', 'sgin', 'frn', 'applicant_type_code', 'applicant_type_code_other', 'status_code', 'status_date', '37ghz_license_type', 'linked_unique_system_id', 'linked_call']
  zip_calls_dtypes = {
    'record_type': "string",
    'unique_system_id': "int",
    'uls_file_no': "string",
    'ebf_no': "string",
    'call': "string",
    'entity_type': "string",
    'license_id': "string",
    'entity_name': "string",
    'first_name': "string",
    'middle_initial': "string",
    'last_name': "string",
    'suffix': "string",
    'phone': "string",
    'fax': "string",
    'email': "string",
    'address': "string",
    'city': "string",
    'state': "string",
    'zip': "string",
    'po_box': "string",
    'attn_line': "string",
    'sgin': "string",
    'frn': "string",
    'applicant_type_code': "string",
    'applicant_type_code_other': "string",
    'status_code': "string",
    'status_date': "string",
    '37ghz_license_type': "string",
    'linked_unique_system_id': "string",
    'linked_call': "string"
  }

  zip_calls = pd.read_csv(
    'license_db/EN.dat',
    header=29,
    delimiter='|',
    names=zip_calls_headers,
    dtype=zip_calls_dtypes,
    na_values = "0"
  )

  ga_technicians = technicians[['call', 'grant_date', 'expired_date', 'cancellation_date', 'certifier_first_name', 'certifier_mi', 'certifier_last_name', 'certifier_suffix']].query('call in @zip_calls.call')

  return ga_technicians

def filter_by_date(offset, df):
  today = datetime.now()
  delta_date = (today - relativedelta(months=int(offset))).strftime('%m/%d/%Y')

  df['grant_date'] = pd.to_datetime(df['grant_date'], format='%m/%d/%Y')
  df2 = df.loc[df['grant_date'] > pd.Timestamp(delta_date)]

  return df2

if __name__ == "__main__":
  logger = logging.getLogger(__name__)
  logging.basicConfig(filename='uls_search.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
  log_header()
  log('Started')

  args = getargs()
  get_licenses()
  zip_calls = get_callsigns_by_zipcode(args.zipcode[0])
  zip_technicians = search_calls(zip_calls)
  filename=args.zipcode[0] + '.csv'
  final = filter_by_date(args.months[0], zip_technicians)
  final.to_csv(filename, sep='|', index=False)

  log('Finished')
