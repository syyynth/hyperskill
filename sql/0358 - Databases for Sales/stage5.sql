select 
    model,
    price,
    sum(total_price) as total_sale_per_model,
    i.quantity as inventory_per_model,
    sum(total_price) / i.quantity as sales_inventory_ratio
from
    sales
join
    products using (product_id)
join
    inventory i using (product_id)
group by
    model, price, i.quantity
order by
    sales_inventory_ratio desc;
