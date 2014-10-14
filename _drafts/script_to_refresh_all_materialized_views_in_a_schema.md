---
layout: post
title: "Script to Refresh all materialized views in a schema"
tags:
 - Oracle
 - script
categories:
 - Tips
image:
 feature: feature_image_green.png
---

Use the following script to refresh all materialized view in a schema of Oracle SGDB.


Connect to the user of the schema where you can to refresh all materalized views and execute the following PL/SQL procedure:

```sql
DECLARE
  v_number_of_failures NUMBER(12) := 0;
BEGIN
  DBMS_MVIEW.REFRESH_ALL_MVIEWS(v_number_of_failures,'C','', TRUE, FALSE);
END;
```

### Execute with sqlplus

Create a file called ```refresh_all_materialised_views.sql``` with the following content:

```sql
DECLARE
v_number_of_failures NUMBER(12) := 0;
BEGIN
DBMS_MVIEW.REFRESH_ALL_MVIEWS(v_number_of_failures,'C','', TRUE, FALSE);
END;
/
```

> Warning, mind the "/" on the last line, it is required to make oracle execute the PL/SQL procedure

Execute with Sqlplus:

```bash
sqlplus user/user_pwd @refresh_all_materialised_views.sql
```
You may add an extra line at the end of ```refresh_all_materialised_views.sql``` to automatically exit Sqlplus when the procedure has been executed (successfully or not):

```sql
quit
```

You should see something like the following output:

```bash
my_machine:$ sqlplus user/user_pwd @refresh_all_materialised_views.sql

SQL*Plus: Release 11.2.0.3.0 Production on Tue Oct 14 10:37:04 2014

Copyright (c) 1982, 2011, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
With the Partitioning, Automatic Storage Management, OLAP, Data Mining
and Real Application Testing options


PL/SQL procedure successfully completed.

Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
With the Partitioning, Automatic Storage Management, OLAP, Data Mining
and Real Application Testing options

my_machine:$
```

### Source

* [Script to Refresh ALL materialized views in a schema](http://www.bash-dba.com/2011/10/refreshing-all-materialized-view-in.html)
