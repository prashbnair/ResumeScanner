import re
import json
import boto3
import os
import logging.config
from tika import parser
from nlp import lang_processor

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('scanner')


def get_text(file_name, bucket_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(file_name, file_name)

    logger.info('Downloaded file from S3')

    text = convert_to_text(file_name)

    if os.path.exists(file_name):
        os.remove(file_name)

    return text


def convert_to_text(file_name):
    logger.info("Converting file to text")
    parsed = parser.from_file(file_name)
    full_text = parsed["content"]
    return full_text


def get_email(text):
    match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', text, re.I)
    return match.group()


def get_phone_number(text):
    match = re.search(r'(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?', text)
    return match.group()


def get_organizations(text):
    return lang_processor.get_organizations(text)


def get_details(file_name, bucket_name):
    text = get_text(file_name, bucket_name)
    # print(text)
    email = get_email(text)
    phone_number = get_phone_number(text)
    org_list = get_organizations(text)
    data = {'email': email.strip(),
            'phone_number': phone_number.strip(),
            'org_list': org_list
            }
    json_data = json.dumps(data)
    # print(json_data)
    logger.inf:memoryviewo(json_data)
    return json_data


# get_details('xyz.docx', 'xyz-bucket')
