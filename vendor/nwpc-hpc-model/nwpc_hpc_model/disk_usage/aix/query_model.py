# coding: utf-8
import re

from nwpc_hpc_model.base.query_model import QueryModel
from . import QueryItem


class AixDiskUsageQueryModel(QueryModel):
    def __init__(self):
        QueryModel.__init__(self)

    @classmethod
    def build_from_category_list(cls, record, category_list):
        if len(record) == 0:
            return None
        category_line = record[0]
        title_line = record[1]
        lines = record[2:]
        model = AixDiskUsageQueryModel()

        detail_pattern = r'^(\w+) +(\w+) +(\d+) +(\d+) +(\d+) +(\d+) +(.+) \| +(\d+) +(\d+) +(\d+) +(\d+) +(\w+) +(.+)'
        detail_prog = re.compile(detail_pattern)

        for line in lines:
            if len(line) == 0:
                continue

            detail_re_result = detail_prog.match(line)
            if not detail_re_result:
                continue

            item = QueryItem.build_from_category_list(detail_re_result, category_list)
            model.items.append(item)

        return model
