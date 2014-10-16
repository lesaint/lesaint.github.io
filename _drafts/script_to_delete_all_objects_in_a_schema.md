---
layout: post
title: "Script to delete all objects in a schema"
tags:
 - Oracle
 - script
categories:
 - tips
image:
 feature: feature_image_green.png
---

Use the following script to drop all objects in a specific schema without droping the schema itself.
Using this script saves you from recreating the schema, its associated user, its rights, ...


### create script file

Create a file called ```empty_user.sql``` with the following content:

```sql
purge recyclebin;
declare
    -- FK first, then unique, then PK
    cursor const_cur is select table_name, constraint_name
                          from user_constraints
                         where constraint_type in ('P', 'R', 'U')
                        order by decode(constraint_type, 'R', 0, 'U', 1, 'P', 2, 3);
    cursor mview_cur is select mview_name from user_mviews;
    cursor view_cur is select view_name from user_views;
    cursor mvlog_cur is select master from user_mview_logs;
    cursor tab_cur is select table_name from user_tables;
    cursor syn_cur is select synonym_name from user_synonyms;
    cursor seq_cur is select sequence_name from user_sequences;
begin
    for const_val in const_cur
    loop
        execute immediate 'alter table ' || const_val.table_name || ' drop constraint ' || const_val.constraint_name;
    end loop;
    for mview_val in mview_cur
    loop
        execute immediate 'drop materialized view ' || mview_val.mview_name;
    end loop;
    for view_val in view_cur
    loop
        execute immediate 'drop view ' || view_val.view_name;
    end loop;
    for mvlog_val in mvlog_cur
    loop
        execute immediate 'drop materialized view log on ' || mvlog_val.master;
    end loop;
    for tab_val in tab_cur
    loop
        execute immediate 'drop table ' || tab_val.table_name || ' purge';
    end loop;
    for syn_val in syn_cur
    loop
        execute immediate 'drop synonym ' || syn_val.synonym_name;
    end loop;
    for seq_val in seq_cur
    loop
        execute immediate 'drop sequence ' || seq_val.sequence_name;
    end loop;
end;
/
quit
```

> line with "/" is required to execute the preceding PL/SQL procedure
> line with "quit" is usefull to automatically exit sqlplus when procedure has been executed

### Execute with sqlplus

```bash
sqlplus user/user_pwd @empty_user.sql
```

You can expect output such as the following:

```sh
my_machine:$ sqlplus user/user_pwd @empty_user.sql

SQL*Plus: Release 11.2.0.3.0 Production on Tue Oct 14 12:27:32 2014

Copyright (c) 1982, 2011, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
With the Partitioning, Automatic Storage Management, OLAP, Data Mining
and Real Application Testing options


Recyclebin purged.


PL/SQL procedure successfully completed.

Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
With the Partitioning, Automatic Storage Management, OLAP, Data Mining
and Real Application Testing options
my_machine:$
```
