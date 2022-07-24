import math
import core.error as error

_default_page = 1
_default_per_page = 15


def pagination_metadata(result, prev, next, per_page, total_page, total_data):
    return {
        "data": result,
        "meta": {
            "prev": prev,
            "next": next,
            "per_page": per_page,
            "total_page": total_page,
            "total_data": total_data,
        },
    }


def _normalize_single_entity(data, keys):
    result = {}

    for el in keys:
        try:
            result[el] = data.__getattr__(el)
        except AttributeError as e:
            result[el] = data.__getattribute__(el)

    return result

def normalize_entity(data, keys):
    data = data if isinstance(data, list) else [data]
    result = []

    for el in data:
        result.append(_normalize_single_entity(el, keys))

    return result

def paginate_multiple(result, page=_default_page, per_page=_default_per_page):
    paginated = result.query.paginate(page, per_page)
    results = normalize_entity(paginated.items)

    return (
        pagination_metadata(
            results,
            1 if page == 1 else page - 1,
            page,
            per_page,
            math.floor(paginated.total / per_page),
            paginated.total,
        )
    )


def paginate_single(
    result, id, page=_default_page, per_page=_default_per_page
):
    data = result.query.get(id)

    if data == None:
        raise error.EntityNotFoundError(
            'Data from entity \'%s\' with id \'%s\' not found.'
            % (result.__name__, id)
        )

    return pagination_metadata(normalize_entity(data), 1, 1, 1, 1, 1)


def deserialize_entity(entity, maps):
    for el in maps.keys():
        entity.__setattr__(el, maps[el])

    return entity
