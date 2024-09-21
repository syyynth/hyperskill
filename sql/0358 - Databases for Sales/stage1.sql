drop table customers, employees, manufacturers, products, inventory, sales;

create table if not exists customers (
    customer_id int primary key auto_increment,
    first_name varchar(45) not null,
    last_name varchar(45) not null,
    address varchar(45) not null,
    city varchar(45) not null,
    state varchar(45) not null
);

create table if not exists employees (
    employee_id int auto_increment,
    first_name varchar(45) not null,
    last_name varchar(45) not null,
    position varchar(45) not null,
    salary decimal not null,
    address varchar(45) not null,
    mobile varchar(45) not null,
    is_active tinyint not null,
    primary key (employee_id)
);

create table if not exists manufacturers (
    manufacturer_id int primary key auto_increment,
    name varchar(45) not null,
    country varchar(45) not null
);

create table if not exists products (
    product_id int primary key auto_increment,
    manufacturer_id int not null,
    model varchar(45) not null,
    price decimal not null,
    horsepower int not null,
    fuel_efficiency int not null,
    foreign key (manufacturer_id) references manufacturers (manufacturer_id)
);

create table if not exists inventory (
    product_id int primary key,
    quantity int not null,
    reorder_level int not null default 2,
    last_inventory_date date not null,
    foreign key (product_id) references products (product_id)
);

create table if not exists sales (
    sale_id int primary key auto_increment,
    sale_date date not null,
    customer_id int not null,
    product_id int not null,
    employee_id int not null,
    quantity int not null,
    total_price decimal not null,
    foreign key (customer_id) references customers (customer_id),
    foreign key (product_id) references products (product_id),
    foreign key (employee_id) references employees (employee_id)
);

insert into customers (first_name, last_name, address, city, state)
values
    ('John', 'Smith', '123 Main St', 'Anytown', 'CA'),
    ('Sarah', 'Chen', '456 Oak Ave', 'Sometown', 'NY'),
    ('Emma', 'Johnson', '789 Pine St', 'Sometown', 'CA'),
    ('Liam', 'Lee', '234 Oak Ave', 'Anytown', 'NY'),
    ('Ava', 'Garcia', '123 Main St', 'Sometown', 'TX'),
    ('Noah', 'Kim', '456 Maple St', 'Othertown', 'CA'),
    ('Olivia', 'Martinez', '789 Elm St', 'Othertown', 'NY'),
    ('Michael', 'Williams', '567 Elm St', 'Anytown', 'CA'),
    ('Emily', 'Chen', '789 Oak Ave', 'Sometown', 'NY'),
    ('Christopher', 'Gonzalez', '123 Pine St', 'Othertown', 'TX'),
    ('Avery', 'Robinson', '456 Main St', 'Anytown', 'CA'),
    ('Noah', 'Lopez', '789 Maple St', 'Sometown', 'NY'),
    ('Emma', 'Baker', '123 Oak Ave', 'Othertown', 'TX'),
    ('William', 'Garcia', '456 Pine St', 'Sometown', 'CA'),
    ('Sofia', 'Kim', '789 Main St', 'Anytown', 'NY'),
    ('Jacob', 'Nguyen', '123 Elm St', 'Othertown', 'TX'),
    ('Ella', 'Rodriguez', '456 Maple St', 'Sometown', 'CA');

insert into employees (first_name, last_name, position, salary, address, mobile, is_active)
values
    ('Emily', 'Dan', 'Sales Associate', 50000, '789 Maple St', '555-1234', 1),
    ('Janeth', 'Kane', 'Sales Manager', 75000, '321 Elm St', '555-5678', 1),
    ('Sophia', 'Nguyen', 'Sales Associate', 55000, '21 Oak Ave', '555-4321', 1);

insert into manufacturers (name, country)
values
    ('Toyoto', 'Japan'),
    ('General Motors', 'United States');

insert into products (manufacturer_id, model, price, horsepower, fuel_efficiency)
values
    (1, 'Camry', 28000, 203, 70),
    (1, 'Corrola', 22000, 175, 75),
    (2, 'Silverado', 41250, 285, 73),
    (2, 'Camaro', 30000, 340, 80);

insert into inventory (product_id, quantity, reorder_level, last_inventory_date)
values (1, 50, 2, '2023-04-30'),
       (2, 30, 2, '2023-04-30'),
       (3, 25, 2, '2023-04-30'),
       (4, 30, 2, '2023-04-30');
