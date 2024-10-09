def apply_filters(model, query, search_query, order_by):
    if search_query:
        if "filters" in search_query and search_query["filters"]:
            for field, value in search_query["filters"].items():
                if not hasattr(model, field):
                    continue
                model_field = getattr(model, field)
                query = query.filter(model_field == value)

        if "text" in search_query and "field" in search_query:
            if hasattr(model, search_query["field"]):
                field = getattr(model, search_query["field"])
                query = query.filter(field.contains(search_query["text"], autoescape=True))

    if order_by:
        for field, direction in order_by:
            if not hasattr(model, field):
                continue
            if direction == "asc":
                query = query.order_by(getattr(model, field).asc())
            elif direction == "desc":
                query = query.order_by(getattr(model, field).desc())

    return query
