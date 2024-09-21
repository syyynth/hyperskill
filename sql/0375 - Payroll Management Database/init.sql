drop table if exists employees, departments, insurance_benefits, jobs;

create table departments (
    id int primary key,
    name varchar(45) not null
);

insert into departments (id, name)
values
    (100, 'City Ethics Commission'),
    (200, 'Emergency Management'),
    (300, 'Office of Finance');

create table jobs (
    id int unsigned primary key,
    title varchar(45) not null,
    type varchar(45) not null,
    hourly_rate double not null
);

insert into jobs (id, title, type, hourly_rate)
values
    (10, 'Tax Renewal Assistant I', 'Part Time', 15.05),
    (20, 'Administrative Intern', 'Part Time', 18.88),
    (30, 'Project Assistant', 'Part Time', 22.01),
    (40, 'Management Assistant', 'Full Time', 32.18),
    (50, 'Management Analyst I', 'Full Time', 35.37),
    (60, 'Senior Accountant II', 'Full Time', 42.29),
    (70, 'Management Analyst II', 'Full Time', 42.87),
    (80, 'Senior Management Analyst I', 'Full Time', 49.29),
    (90, 'Ethics Officer I', 'Full Time', 50.85),
    (100, 'Investment Officer II', 'Full Time', 61.76),
    (110, 'Ethics Officer II', 'Full Time', 63.06);

create table employees (
    id int primary key,
    first_name varchar(45) not null,
    last_name varchar(45) not null,
    department_id int not null,
    job_id int unsigned not null,
    date_employed date not null,
    foreign key (department_id) references departments (id),
    foreign key (job_id) references jobs (id)
);

insert into employees (id, first_name, last_name, department_id, job_id, date_employed)
values
    (1, 'Elbert', 'Rich', 300, 100, '2019-10-01'),
    (2, 'Ray', 'Shipley', 300, 70, '2018-02-10'),
    (3, 'Daisy', 'Diamond', 300, 60, '2019-03-20'),
    (4, 'Lee', 'Durrett', 300, 50, '2018-04-15'),
    (5, 'Carol', 'Brown', 300, 10, '2020-05-09'),
    (6, 'Cheryl', 'Roman', 200, 80, '2018-01-15'),
    (7, 'Kevin', 'Byars', 200, 70, '2018-06-07'),
    (8, 'Andrew', 'Leake', 200, 70, '2019-05-05'),
    (9, 'Shaun', 'Thompson', 200, 40, '2020-02-17'),
    (10, 'Brandon', 'Hoffman', 200, 20, '2020-06-20'),
    (11, 'Philip', 'Wilson', 100, 110, '2020-08-09'),
    (12, 'Dixie', 'Herda', 100, 90, '2018-05-31'),
    (13, 'Stephen', 'West', 100, 90, '2019-09-15'),
    (14, 'Courtney', 'Walker', 100, 70, '2020-07-13'),
    (15, 'Robin', 'Walker', 100, 50, '2019-11-11'),
    (16, 'Antoinette', 'Matava', 100, 50, '2019-06-29'),
    (17, 'Gladys', 'Bosch', 100, 30, '2020-08-16');

create table insurance_benefits (
    id int auto_increment primary key,
    job_id int unsigned not null,
    annual_insurance double not null,
    foreign key (job_id) references jobs (id)
);

insert into insurance_benefits (job_id, annual_insurance)
values
    (10, 0.0),
    (20, 0.0),
    (30, 0.0),
    (40, 9135.28),
    (50, 10385.29),
    (60, 10998.64),
    (70, 11197.39),
    (80, 11357.65),
    (90, 11689.54),
    (100, 12368.28),
    (110, 12368.28);
