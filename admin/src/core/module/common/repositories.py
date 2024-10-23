from sqlalchemy import or_


def apply_filters(model, query, search_query, order_by):
    """
    Applies filters, search criteria, and ordering to a query.

    Args:
        model: The model class.
        query: The initial query.
        search_query: The search parameters.
        order_by: The fields to order by.

    Returns:
        The modified query.
    """
    if search_query:
        query = apply_filter_criteria(model, query, search_query)
        query = apply_search_criteria(model, query, search_query)
        query = apply_multiple_search_criteria(model, query, search_query)

    return order_query(model, query, order_by)


def order_query(model, query, order_by):
    """
    Orders the query based on specified fields and directions.

    Args:
        model: The model class.
        query: The query to modify.
        order_by: A list of (field, direction) tuples.

    Returns:
        The ordered query.
    """
    if order_by:
        for field, direction in order_by:
            if not hasattr(model, field):
                continue
            if direction == "asc":
                query = query.order_by(getattr(model, field).asc())
            elif direction == "desc":
                query = query.order_by(getattr(model, field).desc())

    return query


def apply_search_criteria(model, query, search_query):
    """
    Applies basic search criteria to the query.

    Args:
        model: The model class.
        query: The query to modify.
        search_query: The search parameters.

    Returns:
        The filtered query.
    """
    if "text" in search_query and "field" in search_query:
        if hasattr(model, search_query["field"]):
            field = getattr(model, search_query["field"])
            query = query.filter(field.ilike(f"%{search_query['text']}%"))

    return query


def apply_multiple_search_criteria(model, query, search_query):
    """
    Applies search criteria across multiple fields.

    Args:
        model: The model class.
        query: The query to modify.
        search_query: The search parameters.

    Returns:
        The filtered query.
    """
    if "text" in search_query and "fields" in search_query:
        search_text = search_query["text"]
        search_fields = search_query["fields"]

        conditions = []
        for field_name in search_fields:
            if hasattr(model, field_name):
                field = getattr(model, field_name)
                conditions.append(field.ilike(f"%{search_text}%"))

        if conditions:
            query = query.filter(or_(*conditions))

    return query


def apply_filter_criteria(model, query, search_query):
    """
    Applies field filters to the query.

    Args:
        model: The model class.
        query: The query to modify.
        search_query: The search parameters with filters.

    Returns:
        The filtered query.
    """
    if "filters" in search_query and search_query["filters"]:
        for field, value in search_query["filters"].items():
            if not hasattr(model, field):
                continue
            model_field = getattr(model, field)
            query = query.filter(model_field == value)
    return query
