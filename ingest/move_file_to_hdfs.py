#!/usr/bin/python
import sys
import subprocess
import mysql.connector
import ingestionUtil

# Get arguments
print("Initializing Environment...")
P_FILE_ID = str(sys.argv[1])
P_LOCAL_FILE_PATH = str(sys.argv[2]) if len(sys.argv) > 2 else None

# Establish MYSQL connection
try:
    conn = ingestionUtil.connect_to_mysql()
    cursor = conn.cursor()

    # Get HDFS path and file name stored in metadata db
    SQL_STR = "SELECT input_path, file_name fn FROM ext_table"
    SQL_STR += " WHERE file_id=" + P_FILE_ID
    cursor.execute(SQL_STR)
    for (input_path, fn) in cursor:
        hdfs_path = input_path
        file_name = fn

    conn.close()

except Exception as e:
    print("Error: " + str(e))
    sys.exit(-1)

try:
    # If no local path is provided, use a default local path plus the file name associated with the file id
    if P_LOCAL_FILE_PATH is None:
		print("Reading in directory " + "/home/maria_dev/dgaas/ingest/")
		P_LOCAL_FILE_PATH = "/home/maria_dev/dgaas/ingest/" + file_name
    # If yes, use it, placeholder for some logic later on...
    else:
        P_LOCAL_FILE_PATH = P_LOCAL_FILE_PATH + file_name

    print("Checking if " + hdfs_path + "/" + file_name + " exists")
    file_exists = subprocess.call("hadoop fs -test -f " + hdfs_path + "/" + file_name, shell=True)
    if file_exists == 0:
        print("File exists on HDFS, hence exiting...")
        exit(file_exists)

    # Check if the path directory exists
    # If directory exists, use the existing directory
    # If not, create the directory and any directory above it
    path_exists = subprocess.call("hadoop fs -test -d " + hdfs_path, shell=True)
    if path_exists == 0:
        print("Path exists \n")
    else:
        print("Path do not exist, creating... \n")
        return_code = subprocess.call("hadoop fs -mkdir -p " + hdfs_path, shell=True)
        if return_code == 0:
            print("Path creation: success \n")
        else:
            print("Path creation: failed \n")
            raise Exception("Path creation failed")

    # Change the permissions of the directory so files can be used for external tables
    return_code = subprocess.call("hadoop fs -chmod 777 " + hdfs_path, shell=True)
    if return_code == 0:
        print("Path -chmod: successful \n")
    else:
        print("Path -chmod: failed \n")
        raise Exception("Path -chmod failed")

    # Move file onto HDFS
    print("Copying file: " + P_LOCAL_FILE_PATH + " to HDFS: " + hdfs_path + "\n")
    return_code = subprocess.call("hadoop fs -put " + P_LOCAL_FILE_PATH + " " + hdfs_path, shell=True)
    if return_code == 0:
        print("Move to hdfs successful \n")
    else:
        print("Move to hdfs failed, error: " + str(return_code) + " \n")
		
    print("Move to hdfs done ")
    exit(return_code)

except Exception as e:
    print("Error: " + str(e) + "\n")
    print("Error: " + str(e))
    sys.exit(-1)
