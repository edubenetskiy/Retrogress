from math import ceil

ITEMS_PER_PAGE = 3


class Page:
    items: list
    total_items: int
    num_items: int
    items_per_page: int
    ordinal: int
    index: int
    total_pages: int


def paginate(items, page_ordinal):
    page = Page()
    page.total_items = len(items)
    page.items_per_page = ITEMS_PER_PAGE
    page.total_pages = (page.total_items + ITEMS_PER_PAGE - 1) // page.items_per_page
    page.ordinal = page_ordinal
    page.index = page_ordinal - 1
    page.offset = ITEMS_PER_PAGE * page.index
    page.num_items = page.total_items - page.offset
    page.items = items[page.offset:(page.offset + ITEMS_PER_PAGE)]
    return page
