#!/bin/bash
#############################################################################################
# Run ddl script to create metadata store for DGAAS
#
#############################################################################################

# Source installation response file
. ./install_response.sh

#if [[ $# -lt 1 ]]
#then
#    echo "ERROR: Invalid argument count"
#    echo "usage: fwk_setup_project.sh DsProject"
#    exit 1
#fi


# Drop database if exists
echo Dropping database ${mysql_db} if it already exists...
mysql -h ${mysql_server} -u ${mysql_user} -p${mysql_password} -e "drop database if exists ${mysql_db}"


# Create Database
echo Creating database ${mysql_db}...
mysql -h ${mysql_server} -u ${mysql_user} -p${mysql_password} -e "create database ${mysql_db}"

# Run ddl script
mysql -h ${mysql_server} -u ${mysql_user} -p${mysql_password} ${mysql_db} < md_repo.ddl

echo Metadata data repository created successfully.



