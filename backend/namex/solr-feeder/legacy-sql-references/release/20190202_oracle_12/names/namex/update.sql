-- noinspection SqlNoDataSourceInspectionForFile
-- noinspection SqlNoDataSourceInspectionForFile

-- Update the location of the Oracle Wallet used to make web service calls.

UPDATE configuration
    SET value = 'file:/u01/app/oracle/product/12.2.0.1/dbhome_1/data/wallet'
    WHERE application = 'GLOBAL' AND name = 'oracle_wallet';
