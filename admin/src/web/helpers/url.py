from flask import request, url_for

def url_for_other_page(page, *args, **kwargs):
    args = request.view_args.copy()
    args[""] = page

    if kwargs.items():
        args["per_page"] = request.args.get("per_page", type=int)
        args["sort_by"] = request.args.get("sort_by", "")
        args["order"] = request.args.get("order", "")
        args["search"] = request.args.get("search-text", "")
        args["search_fields"] = request.args.get("search-by", "")
        args["filter_fields"] = request.args.get("filter", "")

    return url_for(request.endpoint, **args)

