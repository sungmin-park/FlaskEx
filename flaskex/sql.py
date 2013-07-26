from math import ceil


class Paginate(list):
    def __init__(self, query, page=0, per_page=10, list_width=10):
        super(Paginate, self).__init__()
        self.query = query
        self.per_page = per_page
        self.list_width = list_width
        self.total = self.query.count()
        self.total_page = max(1, int(ceil(1. * self.total / self.per_page)))
        self.first_page = 0
        self.last_page = self.total_page - 1
        self.page = min(page, self.last_page)
        self.pages = tuple(
            i for i in xrange(
                self.page - self.page % self.list_width,
                min(
                    self.page - self.page % self.list_width + list_width,
                    self.total_page
                )
            )
        )
        self.previous_list = max(self.pages[0] - 1, 0)
        self.next_list = min(self.pages[-1] + 1, self.last_page)
        self += self.query[
            self.page * self.per_page:(self.page + 1) * self.per_page
        ]
