"""
Name: log_cleaner.py

Author: Guru Pai

Date: 6/6/2019

This python script deletes older log files, based on a retention period setting in the properties file.

Arguments:
    1. Properties file: Properties file with cleanup settings.

NOTE: None
"""
__version__ = 1.0

import os
import sys
import time
import logging
import configparser
from datetime import date
from datetime import datetime

properties_file = ''
properties = {}

# Logger setting
logger = logging.getLogger(__name__)
shandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(filename)s - [%(funcName)20s:%(lineno)-3d] - %(levelname)-8s - %(message)s')
shandler.setFormatter(formatter)
logger.addHandler(shandler)
logger.setLevel(logging.DEBUG)

def usage():
    print('usage: log_cleaner.py log_cleaner.properties')
    sys.exit(1)

def read_properties(properties_file):
    """
    Function reads the properties file (log_cleanup.properties) to retrieve the retention period and 
    the log folder name.
    """
    props = configparser.ConfigParser()

    try:
        with open(properties_file, 'r') as prop_file:
            props.read_file(prop_file)
    except IOError as exp:
        logger.error('%s - Cannot continue' % exp)
        raise

    logger.debug('Properties file opened successfully.. Reading the file now..')

    try:
        properties['log_retention_days'] = props['criteria']['log_retention_days']
        properties['log_folder'] = props['general']['log_folder']

        logger.debug('Read successful..')
    except (configparser.NoSectionError, configparser.NoOptionError, configparser.Error, KeyError) as exp:
        logger.error('%s. Cannot continue' % exp)
        raise
    else:
        logger.info('Properties file: %s' % properties_file)
        logger.info('Retention days:%s' % properties['log_retention_days'])
        logger.info('Log folder name:%s' % properties['log_folder'])

        return

def rm_files():
    """
    Function removes old log files that were last modified prior to 'log_retention_days'
    which is set in the log_cleaner.properties file.
    """
    rm_count = 0
    current_time = time.time()

    log_home = properties['log_folder']
    ret_period = properties['log_retention_days']

    for root, directories, filenames in os.walk(log_home):
        for fname in filenames:
            file_name = os.path.join(root, fname)
            try:
                modif_time = os.path.getctime(file_name)

                if (current_time - modif_time) // (24 * 3600) >= float(ret_period):
                    logger.debug("Removing the file:%s with modification TS: %s; Diff:%s" % (os.path._getfullpathname(file_name), time.ctime(modif_time), (current_time - modif_time) // (24 * 3600)))
                    os.unlink(file_name)
                    logger.info('Removed file:%s' % file_name)
                    rm_count += 1
            except (FileNotFoundError, os.error) as exp:
                logger.error('An error occurred while processing the log files. Aborting.. %s' % exp)
                raise

        # Remove the folder if empty folders
        if os.listdir(root) == []: 
            os.removedirs(root)
            logger.info("Removing empty folder:%s" %  root)
        else: 
            logger.debug("Folder:%s not empty. Keeping.." %  root)

    if (rm_count == 0):
        logger.info('Zero files were deleted. Files modified prior to %d were not found' % float(ret_period))
    else:
        logger.info('Total files deleted:%s' % rm_count)

    return

def main(argv):
    args = argv[1:]

    count = len(args)

    if count == 1:
        properties_file = args.__getitem__(0)
        logger.debug('Properties file: %s' % properties_file)

        try:
            read_properties(properties_file)
        except (configparser.NoSectionError, configparser.NoOptionError, configparser.Error, IOError, KeyError) as exp:
            logger.error('An error occurred while reading properties file. Aborting.. %s' % exp)
            sys.exit(2)

        # Setup logging to file
        log_file = properties['log_folder'] + '\\log_cleaner_' + time.strftime('%Y%m%d%H%M%S')+".log"
        fhandler = logging.FileHandler(log_file, 'w')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)

        try:
            rm_files()
        except (FileNotFoundError, IOError) as exc:
            logger.error('An error occurred while deleting log files. Aborting')
            sys.exit(3)
    else:
        print('Properties file name and mngt_name are required arguments..')
        usage()

if __name__ == "__main__":
    main(sys.argv)