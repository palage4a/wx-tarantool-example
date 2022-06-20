box.cfg{
    listen=3301,
    work_dir = 'data',
}
box.schema.user.passwd('pass')

products = box.schema.create_space('products', {if_not_exists=true,temporary=true})
products:format({
    {name = 'id', type = 'unsigned'},
    {name = 'brand', type = 'string'},
    {name = 'name', type = 'string'},
    {name = 'price', type = 'unsigned'},
    {name = 'count', type = 'unsigned'}
})
products:create_index('primary', {
    parts = {'id'},
    if_not_exists = true,
})

customers = box.schema.create_space('customers', {if_not_exists=true,temporary=true})
customers:format({
    {name = 'id', type = 'unsigned'},
    {name = 'email', type = 'string'},
})
customers:create_index('primary', {
    parts = {'id'},
    if_not_exists = true,
})
customers:create_index('email', {
    parts = {'id'},
    if_not_exists = true,
    unique = true,
})

orders = box.schema.create_space('orders', {if_not_exists=true,temporary=true})
orders:format({
    {name = 'id', type = 'unsigned'},
    {name = 'customer_id', type = 'unsigned'},
})
orders:create_index('primary', {
    parts = {'id'},
    if_not_exists = true,
})
orders:create_index('customer_id', {
    parts = {'customer_id'},
    if_not_exists = true,
    unique = false,
})

positions = box.schema.create_space('positions', {if_not_exists=true,temporary=true})
positions:format({
    {name = 'product_id', type = 'unsigned'},
    {name = 'order_id', type = 'unsigned'},
})
positions:create_index('primary', {
    parts = {'product_id', 'order_id'},
    if_not_exists = true,
})

local function setup_db()
    products:truncate()
    positions:truncate()
    customers:truncate()
    orders:truncate()

    -- products
    brands = {'apple', 'samsung', 'huawei', 'xiomi'}
    models = {'galaxy', 'pro', 'max', 'redmi', 'note'}
    for i = 1, 100, 1 do
        brand_id = math.random(1,4)
        brand = brands[brand_id]

        model_id = math.random(1,4)
        model = models[model_id]

        products:insert{i, brand, model, math.random(1000), math.random(10)}
    end

    -- customers
    nicknames = {'ivan', 'nikit', 'dog', 'god', 'peter'}
    mail_providers = {'mail.ru', 'ya.ru', 'gmail.com'}
    for i, nick in ipairs(nicknames) do
        provider = mail_providers[math.random(#mail_providers)]
        customers:insert{i, nick .. '@' .. provider}
    end

    -- orders
    id_order = 1
    for _, customer in customers:pairs() do
        n_orders = math.random(10)
        for i=1, n_orders do
            orders:insert{id_order, customer.id}
            id_order = id_order+1 
        end
    end

    -- positions
    id_positions = 1
    for _, order in orders:pairs() do
        n_position = math.random(5)
        for i=1, n_position do
            id_product = math.random(products:count())
            positions:insert{id_product, id_positions}
            id_positions = id_positions + 1
        end
    end
end

setup_db()
