---
layout: post
title: "Script to delete all objects in a Oracle schema"
tags:
 - Oracle
 - script
categories:
 - tips
image:
 feature: feature_image_green.png
comments: true
---

Use the following script to drop all objects in a specific schema in an Oracle Database without droping the schema itself. It saves you from recreating the schema, its associated user, its rights, etc.


### create script file

Create a file called ```empty_user.sql``` with the following content:

{% highlight sql %}
purge recyclebin;
declare
    -- FK first, then unique, then PK
    cursor cursor_constraints is select table_name, constraint_name
                          from user_constraints
                         where constraint_type in ('P', 'R', 'U')
                        order by decode(constraint_type, 'R', 0, 'U', 1, 'P', 2, 3);
    cursor cursor_mviews is select mview_name from user_mviews;
    cursor cursor_views is select view_name from user_views;
    cursor cursor_mviews_logs is select master from user_mview_logs;
    cursor cursor_tables is select table_name from user_tables;
    cursor cursor_synonyms is select synonym_name from user_synonyms;
    cursor cursor_sequences is select sequence_name from user_sequences;
begin
    for current_val in cursor_constraints
    loop
        execute immediate 'alter table ' || current_val.table_name || ' drop constraint ' || current_val.constraint_name;
    end loop;
    for current_val in cursor_mviews
    loop
        execute immediate 'drop materialized view ' || current_val.mview_name;
    end loop;
    for current_val in cursor_views
    loop
        execute immediate 'drop view ' || current_val.view_name;
    end loop;
    for current_val in cursor_mviews_logs
    loop
        execute immediate 'drop materialized view log on ' || current_val.master;
    end loop;
    for current_val in cursor_tables
    loop
        execute immediate 'drop table ' || current_val.table_name || ' purge';
    end loop;
    for current_val in cursor_synonyms
    loop
        execute immediate 'drop synonym ' || current_val.synonym_name;
    end loop;
    for current_val in cursor_sequences
    loop
        execute immediate 'drop sequence ' || current_val.sequence_name;
    end loop;
end;
/
quit
{% endhighlight %}

> line with "/" is required to execute the preceding PL/SQL procedure
> line with "quit" is usefull to automatically exit sqlplus when procedure has been executed

### Execute with sqlplus

{% highlight bash %}
sqlplus user/user_pwd @empty_user.sql
{% endhighlight %}

You can expect output such as the following:

{% highlight sh %}
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
{% endhighlight %}

# Credits

The origin of the above script is one largely used at [Ekino](https://twitter.com/3k1n0) to which multiple developers (including myself) contributed.
