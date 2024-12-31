
UserRole = (
    ('ADMIN', 'admin'),
    ('MANAGER', 'manager'),
    ('CUSTOMER', 'customer'),
)

AddressLabelType = (
    ('HOME', 'home'),
    ('WORK', 'work'),
    ('OTHER', 'other'),
)

WeightUnit = (
    ('GRAM', 'gm'),
    ('KILOGRAM', 'kg'),
    ('LITRE', 'ltr'),
    ('MILLILITRE', 'ml'),
)

# StockStatus = (
#     ('IN_STOCK', 'in_stock'),
#     ('STOCK_OUT', 'stock_out'),
# )

VoucherType = (
    ('STARTER', 'starter'), 
    ('REGULAR', 'regular'),
    ('PREMIUM', 'premium'),
    ('GENERAL', 'general'),
)

OrderStatus = (
    ('PROCESSING', 'processing'),
    ('CONFIRMED', 'confirmed'),
    ('IN_TRANSIT', 'in_transit'),
    ('DELIVERED', 'delivered'),
    ('CANCELLED', 'cancelled'),
    ('RETURNED', 'returned'),
)

PaymentMethodType = (
    ('CASH', 'cash'),
    ('BKASH', 'bkash'),
    # ('BANK', 'bank'),
    # ('NAGAD', 'nagad'),
    # ('ROCKET', 'rocket'),
    # ('VISA', 'visa'),
    # ('MASTER_CARD', 'master_card'),
)

# CartStatus = (
#     ('PROCESSING', 'processing'),
#     ('ORDERED', 'ordered'),
# )