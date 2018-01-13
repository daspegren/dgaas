#!/usr/bin/python
import sys
import subprocess
import mysql.connector
import ingestionUtil

# Read Parameters
print("Initializing Environment...")
P_FILE_ID = str(sys.argv[1])
P_LOCAL_FILE_PATH = str(sys.argv[2]) if len(sys.argv) > 2 else None

LOGFILE = ingestionUtil.log_path(sys.argv)

print("Logging to file: " + LOGFILE)
log = open(LOGFILE, 'w')

log.write("File ID: " + P_FILE_ID + "\n")
if P_LOCAL_FILE_PATH is not None:
    log.write("Local File Path: " + P_LOCAL_FILE_PATH + "\n")
log.write("\n")


# Establish MYSQL connection
try:
    log.write("Connecting to mySQL server... \n")
    cnx = ingestionUtil.connect_to_mysql()
    cursor = cnx.cursor()
    log.write("Connection to mySQL Successful \n")

    # Obtain HDFS path and file name stored on metadata
    SQL_STR = "SELECT input_path, file_name fn FROM ext_table"
    SQL_STR += " WHERE file_id=" + P_FILE_ID
    cursor.execute(SQL_STR)
    for (input_path, fn) in cursor:
        hdfs_path = input_path
        file_name = fn

    cnx.close()
    log.write("Connection Closed \n")

except Exception as e:
    log.write("MySQL Error: " + str(e) + "\n")
    log.close()
    print("Error: " + str(e))
    sys.exit(-1)

try:
    # If no local path is provided, use a default local path plus the file name associated with the file id
    if P_LOCAL_FILE_PATH is None:
        '''
        Read this from config file maybe?
        '''
        P_LOCAL_FILE_PATH = '/daas/source/' + file_name
    # Otherwise update the file name based on local path to avoid potential regex in metadata file name
    else:
        file_name = P_LOCAL_FILE_PATH.split("/")[0]

    # Check if file already exists
    # If file exists, use the existing file and exit program
    file_exists = subprocess.call("hadoop fs -test -f " + hdfs_path + file_name, shell=True)
    if file_exists == 0:
        log.write("copy_2_hdfs error: file exists, existing file will be used \n")
        exit(file_exists)

    # Check if the path directory exists
    # If directory exists, use the existing directory
    # If not, create the directory and any directory above it
    path_exists = subprocess.call("hadoop fs -test -d " + hdfs_path, shell=True)
    if path_exists == 0:
        log.write("copy_2_hdfs path check: path exists \n")
    else:
        log.write("copy_2_hdfs path check: path do not exist, creating... \n")
        ret_code = subprocess.call("hadoop fs -mkdir -p " + hdfs_path, shell=True)
        if ret_code == 0:
            log.write("copy_2_hdfs path creation: success \n")
        else:
            log.write("copy_2_hdfs path creation: failed \n")
            raise Exception("copy_2_hdfs path creation failed")

    # Change the permissions of the directory so files can be used for external tables
    ret_code = subprocess.call("hadoop fs -chmod 777 " + hdfs_path, shell=True)
    if ret_code == 0:
        log.write("copy_2_hdfs path -chmod: successful \n")
    else:
        log.write("copy_2_hdfs path -chmod: failed \n")
        raise Exception("copy_2_hdfs path -chmod failed")

    # Move file onto HDFS
    log.write("Copying file: " + P_LOCAL_FILE_PATH + " to HDFS: " + hdfs_path + "\n")
    ret_code = subprocess.call("hadoop fs -put " + P_LOCAL_FILE_PATH + " " + hdfs_path, shell=True)
    if ret_code == 0:
        log.write("copy_2_hdfs success \n")
    else:
        log.write("copy_2_hdfs failed, error: " + str(ret_code) + " \n")

    log.close()
    print("copy_2_hdfs success ")
    exit(ret_code)

except Exception as e:
    log.write("Error: " + str(e) + "\n")
    log.close()
    print("Error: " + str(e))
    sys.exit(-1)
