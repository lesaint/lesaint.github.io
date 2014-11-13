---
layout: post
title: "Change tablespace of all objects of a specific Oracle User"
tags:
 - Oracle
 - script
 - SqlPlus
 - bash
categories:
 - tips
image:
 feature: feature_image_green.png
comments: true
---

Here is a convenient PL/SQL script to run with SqlPlus to change the tablespace of the objects (tables, indexes, lobs) of a specific user in a blink. It can also be use to fix inconsistency in tablespace used by the user objects.

We will then see how to use a bash script to make its use less error prone and non interractive.


# The PL/SQL script

The PL/SQL script below changes the tablespace of the tables, indexes and lob objects of the current user. It supports using a different tablespace for data and indexes.

Create file, e.g. called `change_tablespaces.sql`, with the following content. 

```sql
declare
    cursor tab_cur is select table_name from user_tables where tablespace_name != '&&Data';
    cursor ind_cur is select index_name from user_indexes where tablespace_name != '&&Index' and index_type != 'LOB';
    cursor lob_cur is select table_name, column_name from user_lobs where tablespace_name != '&&Index';
    cursor ind2_cur is select index_name from user_indexes where status != 'VALID';
begin
    for tab_val in tab_cur
    loop
        execute immediate 'alter table ' || tab_val.table_name || ' move tablespace &&Data';
    end loop;
    for ind_val in ind_cur
    loop
        execute immediate 'alter index ' || ind_val.index_name || ' rebuild tablespace &&Index';
    end loop;
    for lob_val in lob_cur
    loop
        execute immediate 'alter table ' || lob_val.table_name || ' move lob(' || lob_val.column_name || ') store as (tablespace &&Index)';
    end loop;
    -- some indexes need to be rebuilt a second time after their tablespace has been changed
    for ind2_val in ind2_cur
    loop
        execute immediate 'alter index ' || ind2_val.index_name || ' rebuild';
    end loop;
end;
/
-- exits SqlPlus
quit
```

Please notice that the script uses SqlPlus variables prefixed with `&&`: `&&Data` and `&&Index`. The former holds the name of the tablespace for Data (ie. tables and lobs) and the later the name of the tablespace for Indexes.

>Sqlplus variables can also be defined with a single `&` but in such case SqlPlus will ask for a value each time the variable is used. Sqlplus prompts for the value of variables defined with `&&` only once.

## Use it

Connect to the server hosting the Oracle database or to a machine with remote access configured to the Oracle database for `SqlPlus`.

To change the tablespace for a specific user, connect to that user with SqlPlus and run the script.

You can do that in a single command line (e.g. for user `MYUSER`):

```sh
sqlplus MYUSER/MYUSER @change_tablespaces.sql
```

Sqlplus will prompt the user to provide a value for each variables (first `&&Data`, then `&&Index`). It is best to input the name of the tablespace in upper case.

Here is what it should look like.

```sh
%> sqlplus MYUSER/MYUSER @change_tablespace.sh
SQL*Plus: Release 11.2.0.3.0 Production on Thu Nov 13 13:02:49 2014
Copyright (c) 1982, 2011, Oracle.  All rights reserved.
Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
With the Partitioning, Automatic Storage Management, OLAP, Data Mining
and Real Application Testing options
Enter value for data: CAA
old   2:     cursor tab_cur is select table_name from user_tables where tablespace_name != '&&Data';
new   2:     cursor tab_cur is select table_name from user_tables where tablespace_name != 'CAA';
Enter value for index: XAA
old   4:     cursor ind_cur is select index_name from user_indexes where tablespace_name != '&&Index' and index_type != 'LOB';
new   4:     cursor ind_cur is select index_name from user_indexes where tablespace_name != 'XAA' and index_type != 'LOB';
old   6:     cursor lob_cur is select table_name, column_name from user_lobs where tablespace_name != '&&Index';
new   6:     cursor lob_cur is select table_name, column_name from user_lobs where tablespace_name != 'XAA';
old  15:    execute immediate 'alter table ' || tab_val.table_name || ' move tablespace &&Data';
new  15:    execute immediate 'alter table ' || tab_val.table_name || ' move tablespace CAA';
old  22:    execute immediate 'alter index ' || ind_val.index_name || ' rebuild tablespace &&Index';
new  22:    execute immediate 'alter index ' || ind_val.index_name || ' rebuild tablespace XAA';
old  29:    execute immediate 'alter table ' || lob_val.table_name || ' move lob(' || lob_val.column_name || ') store as (tablespace &&Index)';
new  29:    execute immediate 'alter table ' || lob_val.table_name || ' move lob(' || lob_val.column_name || ') store as (tablespace XAA)';
PL/SQL procedure successfully completed.
SQL>
```

# The bash script

Using the above script with SqlPlus directly has several issues coming from the fact it is interactive:

1. it is open to typing errors and there is no way to double check
2. it can not be scripted

So, here is a bash script which will solve these problems by wrapping the `sqlplus` command line.

The following script:

* assumes the `change_tablespace.sql` is available and in the same directory as the script
* does not run until all parameters have been specified
* displays how to it should be used if at least one parameter is missing
* displays a message with the information gathered from the command line and ask for confirmation before proceeding
* could obviously be improved but does the job, feel free to customize it to meet your needs
* use several sqlplus options to avoid verbose SqlPlus logs (see comments in the script)

```sh
#!/bin/bash

if [ $# -lt 4 ]; then
  echo "$(basename $0) <user_login> <user_pwd> <data_tablespace_name> <index_tablespace_name>"
  exit 0
fi

function proceedOrExit() {
    proceed="";
    while true; do
        case $proceed in
            'y')
                break;
                ;;
            'n')
                exit 0;
                ;;
            *)
                echo -n "Enter 'y' to proceed, 'n' to exit script : ";
                read proceed;
                ;;
        esac
    done
}

user=$1
password=$2
data=$3
index=$4

echo "changing tablespace of user $user (password=$password) 
   - tablespace for data is $data
   - tablespace for indexes is $index"
proceedOrExit

# -s argument suppresses sqlplus welcome and quit messages
sqlplus -s $user/$password << EOF
-- this suppresses the value substitution echoed by sqlplus
set verify off 

define data = $data
define index = $index

@change_tablespace.sql

quit

EOF

exit 0
```

## use it

Assuming you created a script called `change_tablespace.sh` (and made it executable  `chmod +x change_tablespace.sh`), you can run the script with a command as the following:

```sh
./change_tablespace.sh MYUSER MYUSER CAA XAA
```

and you will get an output such as the following:

```sh
changing tablespace of user MYUSER (password=MYUSER) 
   - tablespace for data is CAA
   - tablespace for indexes is XAA
Enter 'y' to proceed, 'n' to exit script : y

PL/SQL procedure successfully completed.
```

# Resources

* [In depth look at Sqlplus variables](http://www.orafaq.com/node/515)
