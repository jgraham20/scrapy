#!/usr/bin/env python
"""Scrapy admin script is used to create new scrapy projects and similar
tasks"""
import os
import string
from optparse import OptionParser
import re

import scrapy
from scrapy.utils.misc import render_templatefile, string_camelcase
from scrapy.utils.python import ignore_patterns, copytree

usage = """
scrapy-admin.py [options] [command]
 
Available commands:
     
    startproject <project_name>
      Starts a new project with name 'project_name'
"""

PROJECT_TEMPLATES_PATH = os.path.join(scrapy.__path__[0], 'templates/project')

# This is the list of templatefile's path that are rendered *after copying* to
# project directory.
TEMPLATES = (
        'scrapy-ctl.py',
        '${project_name}/settings.py.tmpl',
        '${project_name}/items.py.tmpl',
        '${project_name}/pipelines.py.tmpl',
        )

IGNORE = ignore_patterns('*.pyc', '.svn')

def main():
    parser = OptionParser(usage=usage)
    opts, args = parser.parse_args()

    if not args:
        parser.print_help()
        return

    cmd = args[0]
    if cmd == "startproject":
        if len(args) >= 2:
            project_name = args[1]
            if not re.search(r'^[_a-zA-Z]\w*$', project_name): # If it's not a valid directory name.
                # Provide a smart error message, depending on the error.
                if not re.search(r'^[_a-zA-Z]', project_name):
                    message = 'make sure the project_name begins with a letter or underscore'
                else:
                    message = 'use only numbers, letters and underscores'
                print "scrapy-admin.py: %r is not a valid project name. Please %s." % (project_name, message)
            else:
                project_root_path = project_name

                roottpl = os.path.join(PROJECT_TEMPLATES_PATH, 'root')
                copytree(roottpl, project_name, ignore=IGNORE)

                moduletpl = os.path.join(PROJECT_TEMPLATES_PATH, 'module')
                copytree(moduletpl, '%s/%s' % (project_name, project_name),
                         ignore=IGNORE)

                for path in TEMPLATES:
                    tplfile = os.path.join(project_root_path,
                            string.Template(path).substitute(project_name=project_name))
                    render_templatefile(tplfile, project_name=project_name,
                            ProjectName=string_camelcase(project_name))
        else:
            print "scrapy-admin.py: missing project name"
    else:
        print "scrapy-admin.py: unknown command: %s" % cmd

if __name__ == '__main__':
    main()