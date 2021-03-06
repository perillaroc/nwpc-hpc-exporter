# coding: utf-8
from pathlib import Path
import yaml

from nwpc_hpc_model.disk_space.pi import PiDiskSpaceQueryModel, QueryCategory, \
    PiDiskSpaceCategoryList, record_parser, value_saver


class TestQuotaInfo(object):
    def check_build_model(self, test_case):
        record = test_case['record']
        category_list = test_case['category_list']
        records = test_case['records']

        model = PiDiskSpaceQueryModel.build_from_category_list(record, category_list)

        for record in records:
            index = record['index']
            properties = record['properties']
            item = model.items[index]

            for a_prop in properties:
                category_id = a_prop['category_id']
                data = a_prop['data']
                category_index = category_list.index_from_id(category_id)
                p = item.props[category_index]

                assert(p.map['data'] == data)

    def test_build_model_using_config_file(self):
        check_method = self.check_build_model

        config_file_path = Path(
            Path(__file__).parent,
            "../../../../nwpc_hpc_model/disk_space/pi/conf/disk_space.config.yml"
        )

        with open(config_file_path) as f:
            category_list_config = yaml.load(f)

        category_list = PiDiskSpaceCategoryList.build_from_config(category_list_config['category_list'])

        test_case_list = list()

        nwp_output = Path(
            Path(__file__).parent,
            "../../data/pi/df_m.txt"
        )

        with open(nwp_output) as nwp_output_file:
            record = nwp_output_file.readlines()
            test_case_list.append({
                'record': record,
                'category_list': category_list,
                'records': [
                    {
                        'index': 7,
                        'properties': [
                            {
                                'category_id': 'disk_space.mounted_on',
                                'data': '/g0'
                            },
                            {
                                'category_id': 'disk_space.blocks.total_size_mb',
                                'data': 563712000
                            },
                            {
                                'category_id': 'disk_space.blocks.used_size_mb',
                                'data': 78205224
                            },
                        ]
                    },
                    {
                        'index': 8,
                        'properties': [
                            {
                                'category_id': 'disk_space.mounted_on',
                                'data': '/g1'
                            },
                            {
                                'category_id': 'disk_space.blocks.total_size_mb',
                                'data': 1540096000
                            },
                            {
                                'category_id': 'disk_space.blocks.used_size_mb',
                                'data': 610587889
                            },
                        ]
                    }
                ]
            })

        for a_test_case in test_case_list:
            check_method(a_test_case)

