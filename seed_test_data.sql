-- seed_test_data.sql
-- TEST TOOLING for the performance test (#10). Adds 10,000 marked test assets.
-- Run cleanup_test_data.sql afterwards.

insert into hardware_details (system_name, model, manufacturer, asset_type, ip_address)
select top (10000)
    concat('SEED-', row_number() over (order by (select null))),
    'Test model', 'Test maker', 'Windows', '10.0.0.1'
from sys.all_objects a cross join sys.all_objects b;

insert into asset (hardware_id, employee_id, notes, purchase_date)
select hardware_id, 1, 'SEED', '2025-01-01'
from hardware_details
where system_name like 'SEED-%';