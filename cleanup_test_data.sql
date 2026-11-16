-- cleanup_test_data.sql
-- Removes everything seed_test_data.sql added.
delete from asset where notes = 'SEED';
delete from hardware_details where system_name like 'SEED-%';