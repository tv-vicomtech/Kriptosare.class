DROP KEYSPACE IF EXISTS kryptosare;

CREATE KEYSPACE kryptosare 
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'replication_factor' : 1 
  };

USE kryptosare;

CREATE TABLE address (
    label int,
    class int,
    user text,
    address text PRIMARY KEY,
    tx_recv double,
    tx_sent double,
    amount_recv double,
    amount_sent double,
    balance double,
    unique int,
    sibling double 
);

CREATE TABLE entity (
    label int,
    user text PRIMARY KEY,
    tx_recv double,
    tx_sent double,
    amount_recv double,
    amount_sent double,
    balance double,
    add_recv double,
    add_sent double
);

CREATE TABLE motifs1 (
    id double PRIMARY KEY,
    label int,
    class int,
    outuser text,
    address_recv_dist double,
    tx_sent double,
    amount_recv double,
    address_sent_dist double,
    amount_sent double,
    tx_recv_tot double,
    fees double,
    loop_in_out int,
    direct_in_out int,
    repetition int 
);

CREATE TABLE motifs2 (
    id double PRIMARY KEY,
    label int,
    class int,
    outuser text,
    address_recv_dist_to_out double,
    fee2 double,
    tx_sent_from_mid double,
    amount_recv_to_out double,
    address_sent_from_mid double,
    amount_sent_from_mid double,
    address_recv_to_mid double,
    amount_recv_to_mid double,
    tx_sent_from_in double,
    address_sent_from_in double,
    amount_sent_from_in double,
    fee1 double,
    loop_mid_out int,
    direct_mid_out int,
    loop_in_mid int,
    direct_in_mid int,
    loop_in_out int,
    direct_in_out int,
    repetition int
);

CREATE TABLE enriched_entity (
    label int,
    predict_class1 double,
    predict_class2 double,
    predict_class3 double,
    predict_class4 double,
    predict_class5 double,
    predict_class6 double,
    user text PRIMARY KEY,
    tx_recv double,
    tx_sent double,
    amount_recv double,
    amount_sent double,
    balance double,
    add_recv double,
    add_sent double,
    add_cnt1 double,
    add_cnt2 double,
    add_cnt3 double,
    add_cnt4 double,
    add_cnt5 double,
    add_cnt6 double,
    mot1_cnt1 double,
    mot1_cnt2 double,
    mot1_cnt3 double,
    mot1_cnt4 double,
    mot1_cnt5 double,
    mot1_cnt6 double,
    mot2_cnt1 double,
    mot2_cnt2 double,
    mot2_cnt3 double,
    mot2_cnt4 double,
    mot2_cnt5 double,
    mot2_cnt6 double
);
