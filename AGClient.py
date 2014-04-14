#!/usr/bin/python
# -*- coding: utf-8 -*-

''' UC3M Moodle (AulaGlobal)
Only allow three webservice methods:
core_webservice_get_site_info
core_enrol_get_users_courses
core_course_get_contents '''

import urllib2
import json
import os
import argparse
import xml.etree.ElementTree as et

domain = 'aulaglobal.uc3m.es'
webservice = '/webservice/rest/server.php'
service = 'ag_mobile'


# First we need the token

def get_token(user, passwd):
    url_token = 'https://' + domain + '/login/token.php?username=' \
        + user + '&password=' + passwd + '&service=' + service
    req = urllib2.Request(url_token)
    resp = urllib2.urlopen(req).read()

    # JSON :)

    data = json.loads(resp.decode('utf8'))
    token = data.get('token')

    # Error, password / username wrong?

    if token is None:
        print data.get('error')
        exit()
    return token


# Get the userid necessary for get user courses

def get_user_info(token):
    url_info = 'https://' + domain + webservice + '?wstoken=' + token \
        + '&wsfunction=core_webservice_get_site_info'
    req = urllib2.Request(url_info)
    resp = urllib2.urlopen(req).read()

    # Yes, is a XML

    root = et.fromstring(resp)
    name = root.find("SINGLE/KEY[@name='fullname']/VALUE")  # Who am i
    user_id = root.find("SINGLE/KEY[@name='userid']/VALUE").text
    print 'User ID: ' + user_id + ', ' + name.text
    return user_id


# Just simply return a list of courses ids

def get_courses(token, userid):
    url_courses = 'https://' + domain + webservice + '?wstoken=' \
        + token + '&wsfunction=core_enrol_get_users_courses&userid=' \
        + userid
    req = urllib2.Request(url_courses)
    resp = urllib2.urlopen(req).read()

    # print url_courses

    root = et.fromstring(resp)
    ids = root.findall("MULTIPLE/SINGLE/KEY[@name='id']/VALUE")  # This is a list
    return ids


# Get the course contents (files urls)

def get_course_content(token, course_id):
    url_course = 'https://' + domain + webservice + '?wstoken=' + token \
        + '&wsfunction=core_course_get_contents&courseid=' + course_id
        
    req = urllib2.Request(url_course)
    resp = urllib2.urlopen(req).read()
    root = et.fromstring(resp)
    xml_modules = "MULTIPLE/SINGLE/KEY[@name='modules']/MULTIPLE/"
    xml_contents = "SINGLE/KEY[@name='contents']/MULTIPLE/SINGLE"
    file_contents =  root.findall(xml_modules+xml_contents )  
    files = []
    for file_content in file_contents:
        file_url = file_content.find("KEY[@name='fileurl']/VALUE").text
        file_name = file_content.find("KEY[@name='filename']/VALUE"
                ).text
        file_type = file_content.find("KEY[@name='type']/VALUE").text
        if file_type == 'file':
            moodle_file = {}
            # print 'File: ' + file_name
            moodle_file['file_name'] = file_name
            moodle_file['file_url'] = file_url
            files.append(moodle_file)

    return files


def save_files(token, course_id, files):
    path = 'cursos/' + course_id
    if not os.path.exists(path):
        os.makedirs(path)

    for moodle_file in files:
        print 'Downloading: ' + moodle_file['file_name']
        url = moodle_file['file_url'] + '&token=' + token
        file = path + '/' + moodle_file['file_name']
        response = urllib2.urlopen(url)
        fh = open(file, 'wb')
        fh.write(response.read())
        fh.close()


def main():
    parser = \
        argparse.ArgumentParser(description='Aula Global from  Command Line'
                                )
    parser.add_argument('-u', metavar='User (NIA)', action='store',
                        required=True)
    parser.add_argument('-p', metavar='Password', action='store',
                        required=True)
    args = parser.parse_args()

    token = get_token(args.u, args.p)
    userid = get_user_info(token)
    ids = get_courses(token, userid)
    for course_id in ids:
        print 'Course ID: ' + course_id.text
        files_url = get_course_content(token, course_id.text)
        save_files(token, course_id.text, files_url)


if __name__ == '__main__':
    main()
