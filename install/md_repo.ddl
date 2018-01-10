--  TABLE ext_table
CREATE TABLE ext_table
(
   file_id          int(11),
   file_name        varchar(255),
   ext_table_name   varchar(255),
   delim            varchar(5),
   input_path       varchar(1024),
   hive_db          varchar(255)
);
ALTER TABLE ext_table ADD PRIMARY KEY (file_id);

--  TABLE ext_table_def
CREATE TABLE ext_table_def
(
   file_id           int(11),
   col_name          varchar(255),
   target_col_name   varchar(255),
   col_desc          varchar(255),
   col_order         int(11),
   d_type            varchar(45),
   start             int(10),
   len               int(10),
   mask_indicator	 int(11) DEFAULT 0,
   std_type_cd_ind   int(11) DEFAULT 0,
   validation_check_col_name	 varchar(225) DEFAULT NULL,
   pii_indicator	 int(1),
   sensitive_indicator	 int(1)
   
);
ALTER TABLE ext_table_def ADD PRIMARY KEY (file_id, col_order);

--  TABLE target_table
CREATE TABLE target_table
(
   table_id         int(11),
   table_name       varchar(255),
   operation_type   varchar(10),
   hive_db          varchar(255)
);
ALTER TABLE target_table ADD PRIMARY KEY (table_id);

--  TABLE target_table_def
CREATE TABLE target_table_def
(
   table_id      int(11),
   col_name      varchar(255),
   col_desc      varchar(255),
   col_order     int(11),
   d_type        varchar(45)
);
ALTER TABLE target_table_def ADD PRIMARY KEY (table_id, col_order);
