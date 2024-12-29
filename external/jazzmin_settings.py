# from user_app.models import UserModel

JAZZMIN_SETTINGS = {
    'site_title': "Central Mart",
    'site_header': 'Central Mart',
    'site_brand': 'Central Mart',
    'site_logo': 'images/central_mart.jpg', 
    "site_logo_classes": "img-circle",

    # 'login_logo': 'images/central_mart.jpg', 
    "welcome_sign": "Welcome to Central Mart",
    'show_ui_builder': True,
    'copyright': 'central_mart',

    "search_model": [
        "user_app.UserModel",
        ],
    'recent_actions': {
        'enabled': True,  
        'limit': 10,      
        'show': True,    
    },
    # "user-avatar": None,

     'topmenu_links': [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["user_app.view_user"]},
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"app": "address_app"}, 
        {"app": "product_management_app"}, 
        {"app": "order_management_app"},
    ],
    "navigation_expanded": False,

    "hide_apps": ['token_blacklist', 'celery_results',  'django_celery_results', 'django_celery_beat', 'auth'],
    "hide_models": [],

    "order_with_respect_to": ['product_management_app', 'order_management_app', 'user_app', 'address_app', 'token_blacklist'],

     "custom_links": {
        "users": [{
            "name": "Groups", 
            "url": "admin:auth_group_changelist",
            "icon": "fas fa-user",        
            "permissions": ["auth.view_group"]  
        }]
    },


    "default_icon_parents": "fas fa-arrow-right",
    "default_icon_children": "fas fa-arrow-right",

    "icons": {
        "user_app": "fas fa-users",
         "address_app": "fas fa-home",
        "product_management_app": "fas fa-box-open",
        "order_management_app": "fas fa-shopping-cart",
        "token_blacklist": "fas fa-tag",
    },
}

JAZZMIN_UI_TWEAKS = {
    'theme': 'cerulean',  # A clean blue base theme
    'navbar': 'navbar-dark bg-blue',  # Blue navbar
    'accent': 'accent-pink',  # Pink accents for buttons and links
    'brand_colour': 'bg-purple',  # Purple brand color in the sidebar
    'sidebar': 'sidebar-dark-purple',  # Dark sidebar with primary blue
    'sidebar_nav_flat_style': True,  # Flat style for the sidebar
    'sidebar_nav_child_indent': True,  # No indentation for child links
    'button_classes': {
        'primary': 'btn-primary',  # Blue primary buttons
        'secondary': 'btn-outline-purple',  # Pink outline for secondary buttons
    },
    'actions_sticky_top': True,  # Sticky actions at the top
    'navbar_fixed': False,  # Fixed navbar
    'footer_fixed': False,  # Footer not fixed
    'actions_sticky_top': True,
}



