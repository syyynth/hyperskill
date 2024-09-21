create index customer_sales_product on sales (customer_id, product_id);

create view sales_summary as (
    select
        model,
        count(model)
    from 
        sales
    join
        products using (product_id)
    group by
        model
);

select * from sales_summary;

insert into sales (sale_date, customer_id, product_id, employee_id, quantity, total_price)
values
    ('2023-05-04', 3, 1, 3, 1, 28000),
    ('2023-05-04', 4, 2, 3, 1, 22000),
    ('2023-05-04', 5, 3, 1, 1, 41250),
    ('2023-05-04', 6, 4, 3, 1, 30000),
    ('2023-05-05', 7, 1, 1, 1, 28000),
    ('2023-05-05', 8, 2, 3, 1, 22000),
    ('2023-05-05', 9, 3, 3, 1, 41250),
    ('2023-05-06', 10, 4, 2, 1, 30000),
    ('2023-05-06', 11, 1, 1, 1, 28000),
    ('2023-05-07', 12, 2, 3, 1, 22000),
    ('2023-05-07', 13, 1, 3, 1, 28000),
    ('2023-05-07', 14, 2, 1, 1, 22000),
    ('2023-05-08', 15, 3, 3, 1, 41250),
    ('2023-05-08', 16, 4, 3, 1, 30000),
    ('2023-05-08', 17, 1, 2, 1, 28000);