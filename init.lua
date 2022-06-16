box.cfg{
    listen=3301,
    work_dir = 'data',
}
box.schema.user.passwd('pass')

s = box.schema.create_space('products', {if_not_exists=true,temporary=true})
s:format({
    {name = 'id', type = 'unsigned'},
    {name = 'brand', type = 'string'},
    {name = 'name', type = 'string'},
    {name = 'price', type = 'unsigned'},
    {name = 'count', type = 'unsigned'}
})

s:create_index('primary', {
    parts = {'id'},
    if_not_exists = true,
})

s:insert{1, 'apple', 'iphone', 600, 12}
s:insert{2, 'samsung', 'galaxy', 500, 4}
s:insert{3, 'apple', 'macbook', 1200, 14}
