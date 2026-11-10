-- The schema for the ScottishGlen Asset Tracker (MySQL).
-- Tables are created in dependency order: a table must exist before another points at it.

-- The client's five fixed departments. A separate table so the names stay consistent.
-- Staff pick from a list instead of typing.
create table department (
    department_id int auto_increment primary key,
    department_name varchar(50) not null
);

-- The people responsible for assets. Each employee works in one department.
-- Created before asset because asset points to it.
create table employee (
    employee_id int auto_increment primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) not null,
    department_id int not null,
    foreign key (department_id) references department(department_id)
    );

-- Hardware details collected automatically from the machine, not typed in by staff.
-- Created before asset because asset points to it.
create table hardware_details (
    hardware_id int auto_increment primary key,
    system_name varchar(100) not null,
    model varchar(100) not null,
    manufacturer varchar(100) not null,
    ip_address varchar(100) not null,
    asset_type varchar(100) not null
);

-- One row per tracked asset. Linked to the responsible employee and to its hardware details.
-- notes and purchase_date are optional because not every asset has them (e.g. no purchase sticker).
create table asset (
    asset_id int auto_increment primary key,
    notes varchar(255), -- 255 characters: room for a couple of sentences without unbounded text.
    purchase_date date,
    hardware_id int not null unique, -- unique: each asset has its own hardware row.
    employee_id int not null,
    foreign key (employee_id) references employee(employee_id),
    foreign key (hardware_id) references hardware_details(hardware_id)
);

-- Load the five departments named by the client.
insert into department (department_name)
values ('Sales'), ('Human Resources'), ('Operations'), ('Information Technology'), ('Finance');

