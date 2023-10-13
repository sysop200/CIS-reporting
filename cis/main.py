import os
import pathlib
import json

from jinja2 import Environment, FileSystemLoader

reports = os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')

reports = list(filter(lambda x: pathlib.Path(x).suffix == '.json', os.listdir(REPORTS_DIR)))


env = Environment(loader = FileSystemLoader(TEMPLATES_DIR))
template = env.get_template('base.html')


class CisParser:

    report_dir = REPORTS_DIR
    benchmark_exclude_list = ['benchmark_type', 'benchmark_version', 'host_automation_group', 'host_epoch']

    def __init__(self, report_name) -> None:
        self.report_name = report_name
    
    def array_to_string(self, array):
        return ' '.join(array)

    def get_test_found(self, test_item):
        found = test_item['found']

        if type(found) is list:
            found = self.array_to_string(found)
        
        return found
    
    def get_test_expected(self, test_item):
        
        expected = test_item['expected']
        if type(expected) is list:
            expected = self.array_to_string(expected)

        return expected
    
    @property
    def translate_map(self):
        return {
            'benchmark_os': 'Операционная система',
            'benchmark_type': 'Операционная система',
            'host_hostname': 'Имя хоста',
            'host_machine_uuid': 'Идентификатор uuid',
            'host_os_distribution': 'Дистрибутив',
            'host_os_locale': 'Таймзона',
            'host_os_release': 'Версия',
            'host_system_type': 'Тип актива'
        }
    
    @property
    def cis_sections(self):
        return {
            '1': '01 Inventory and Control of Enterprise Assets',
            '2': '02 Inventory and Control of Software Assets',
            '3': '03 Data Protection',
            '4': '04 Secure Configuration of Enterprise Assets and Software',
            '5': '05 Account Management',
            '6': '06 Access Control Management',
            '7': '07 Continuous Vulnerability Management',
            '8': '08 Audit Log Management',
            '9': '09 Email and Web Browser Protections',
            '10': '10 Malware Defenses',
            '11': '11 Data Recovery',
            '12': '12 Network Infrastructure Management',
            '13': '13 Network Monitoring and Defense',
            '14': '14 Security Awareness and Skills Training',
            '15': '15 Service Provider Management',
            '16': '16 Application Software Security',
            '17': '17 Incident Response Management',
            '18': '18 Penetration Testing'
        }

    def translate_keys(self, item):
        for k, v in self.translate_map.items():
            if k in item:
                item[v] = item[k]
                del item[k]
        return item

    def get_summary(self, test_item):
        section = self.get_section(test_item)
        section_id = None
        section_name = None
        if section:
            section_id, section_name = section
        return {
            'test_name': test_item['title'],
            'test_description': test_item['summary-line'],
            'test_passed': test_item['successful'],
            'test_expected': self.get_test_expected(test_item),
            'test_found': self.get_test_found(test_item),
            'section_id': section_id,
            'section_name': section_name,
        }
    
    def get_section(self, test_item):
        meta = test_item['meta']

        if 'CIS_ID' in test_item['meta']:
            section = str(meta['CIS_ID'][0]).split('.')[0]
            if section in self.cis_sections:
                return [section, self.cis_sections[section]]

        return []

    def get_table_meta(self, test_item):
        meta = test_item['meta']

        if 'CIS_ID' in meta:
            del meta['CIS_ID']
        return meta

    def get_benchmark_meta(self, benchmark):
        meta = benchmark['meta']

        for excl in self.benchmark_exclude_list:
            if excl in meta:
                del meta[excl]

        meta = self.translate_keys(meta)

        return meta


    def parse(self):
        with open(os.path.join(self.report_dir, self.report_name)) as file:

            filename = os.path.join(RESULTS_DIR, f'{self.file_name}.html')

            with open(filename, 'w') as fh:
                tests = json.load(file)['results']
                benchmark = list(filter(lambda x: x['title'] == "Benchmark MetaData", tests))[0]
                tests_without_benchmark = list(filter(lambda x: x['title'] != "Benchmark MetaData", tests))
                sorted_tests = sorted(tests_without_benchmark, key=lambda d: d['title'])
                data = []

                for test in sorted_tests:
                    data.append(
                        {
                            'summary': self.get_summary(test),
                            'table': self.get_table_meta(test),
                        }
                    )

                fh.write(template.render(
                    data = data,
                    benchmark = self.get_benchmark_meta(benchmark),
                    sections = self.cis_sections,
                ))

    @property
    def file_name(self):
        return pathlib.Path(self.report_name).stem


if __name__ == '__main__':

    for i in reports:
        report = CisParser(i)
        report.parse()
