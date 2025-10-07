from flask import request
from database import Employee
from sqlalchemy import desc, asc

def sorting(query, model):
    """
    Сортировка по одному или нескольким GET-параметрам вида <?sort=sort_by:sort_order,sort_by:sort_order...>
    """

    sort_params=request.args.get('sort', '')
    if not sort_params:
        return query

    sort_list = sort_params.split(',')
    model_mapper = model.__mapper__
    allowed_columns = [column.key for column in model_mapper.attrs]

    for param in sort_list:
        if ':' in param:
            item, order = param.split(':', 1)
            if order != 'desc':
                order = 'asc'
        else:
            item, order = param, 'asc'
        if item in allowed_columns:
            sort_column = getattr(model, item)
            query = query.order_by(
                desc(sort_column) if order=='desc' else asc(sort_column)
            )
    return query

def full_searching(query, model):
    """
    Поиск по полному совпадению ФИО сотрудника вида <?fullsearch=...>
    """
    search_param = request.args.get('fullsearch', '')
    if not search_param:
        return query
    
    query = query.filter(model.fullname == search_param)
    return query

def partial_searching(query, model):
    """
    Поиск по частичному совпадению ФИО сотрудника вида <?partsearch=...>
    """   
    search_param = request.args.get('partsearch', '')
    if not search_param:
        return query
    
    query = query.filter(model.fullname.ilike('%'+search_param+'%'))
    return query
    
