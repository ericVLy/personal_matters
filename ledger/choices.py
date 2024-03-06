transaction_category_choices = (
    ('Cultural Leisure ',' 文化休闲'),
    ('Investment and Wealth Management ','投资理财'),
    ('Catering Cuisine ','餐饮美食'),
    ('Recharge Payment ','充值缴费'),
    ('Revenue ','收入'),
    ('Home Furnishing ','家居家装'),
    ('Credit Borrowing and Repayment ','信用借还'),
    ('Transfer Red Envelope ','转账红包'),
    ('Refund ','退款'),
    ('Hotel tourism ','酒店旅游'),
    ('Dress up ','服饰装扮'),
    ('Life Services', '生活服务'),
    ('Public Service ','公共服务'),
    ('Medical Health ','医疗健康'),
    ('Account Access', '账户存取'),
    ('Beauty and hairdressing ','美容美发'),
    ('Transportation Travel ','交通出行'),
    ('Business Services', '商业服务'),
    ('Mother Infant Parent Child ','母婴亲子'),
    ('Sports Outdoor ','运动户外'),
    ('Pet ','宠物'),
    ('Daily necessities', '日用百货'),
    ('Digital Appliances', '数码电器'),
    ('Love car maintenance ','爱车养车'),
    ('Other ','其他'),
)



receipt_disbursement_choices = (
    ("receipt", "收入"),
    ("disbursement", "支出"),
    ("ignore", "不计收支"),
)

transaction_status_choices = (
    ('transaction_successful',  '交易成功'),
    ('transaction_closed',  '交易关闭'),
    ('thawing_successful',  '解冻成功'),
    ('refund_successful',  '退款成功'),
    ('payment_successful',  '支付成功'),
)