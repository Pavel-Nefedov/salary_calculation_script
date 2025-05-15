import pytest
import os
import main

# Тестовые данные
csv_data_1 = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40"""

csv_data_2 = """id,email,name,department,hours_worked,rate
3,carol@example.com,Carol Williams,Design,170,60
4,dave@example.com,Dave Wilson,Marketing,180,55"""


# Создаем временные CSV файлы для тестирования
@pytest.fixture(scope='module', autouse=True)
def setup_files():
    with open('test1.csv', 'w', encoding='utf-8') as f:
        f.write(csv_data_1)
    with open('test2.csv', 'w', encoding='utf-8') as f:
        f.write(csv_data_2)
    yield

    # Удаляем файлы после тестов
    os.remove('test1.csv')
    os.remove('test2.csv')


def test_read_csv():
    header, data = main.read_csv('test1.csv')
    assert header == ['id', 'email', 'name', 'department', 'hours_worked', 'hourly_rate']
    assert len(data) == 2
    assert data[0] == ['1', 'alice@example.com', 'Alice Johnson', 'Marketing', '160', '50']


def test_find_hourly_rate_index():
    header1 = ['id', 'email', 'name', 'department', 'hours_worked', 'hourly_rate']
    header2 = ['rate', 'email', 'name', 'department', 'hours_worked', 'id']
    header3 = ['id', 'email', 'name', 'salary', 'hours_worked', 'departament']
    assert main.find_hourly_rate_index(header1) == 5
    assert main.find_hourly_rate_index(header2) == 0
    assert main.find_hourly_rate_index(header3) == 3


def test_generate_departmental_payout_reports():
    reports = main.generate_departmental_payout_reports(['test1.csv', 'test2.csv'])

    assert 'Marketing' in reports
    assert len(reports['Marketing']) == 2  # количество сотрудников в отделе Marketing
    assert 'Общий заработок:' in reports['Marketing'][0]
    assert 'Design' in reports
    assert len(reports['Design']) == 2  # количество сотрудников в отделе Design
    assert 'Общий заработок:' in reports['Design'][0]
