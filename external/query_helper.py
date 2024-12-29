def get_query_data(param, queryset):
    if param:
        for key, value in param.items():
            queryset = queryset.filter(**{key: value})
    print("Working!")
    return queryset