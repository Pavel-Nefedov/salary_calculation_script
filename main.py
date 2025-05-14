import argparse

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        header = file.readline().strip().split(',')
        data = [line.strip().split(',') for line in file]
    return header, data

def find_hourly_rate_index(header):
    for index, column in enumerate(header):
        if column in ['hourly_rate', 'rate', 'salary']:
            return index
    return -1

def generate_departmental_payout_reports(file_paths):
    department_reports = {}

    for file_path in file_paths:
        header, data = read_csv(file_path)
        hourly_rate_index = find_hourly_rate_index(header)

        for row in data:
            department = row[header.index('department')]
            hours_worked = int(row[header.index('hours_worked')])
            hourly_rate = int(row[hourly_rate_index])
            total_payout = hours_worked * hourly_rate

            employee_report = f"Сотрудник: {row[header.index('name')]}, " \
                              f"Часы работы: {hours_worked}, " \
                              f"Ставка: {hourly_rate}, " \
                              f"Общий заработок: {total_payout}"

            if department not in department_reports:
                department_reports[department] = []
            department_reports[department].append(employee_report)

    return department_reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', help='Тип отчета, например payout', required=True)
    args = parser.parse_args()

    if args.report == 'payout':
        report = generate_departmental_payout_reports(args.files)
        for department, reports in report.items():
            print(f"Отдел: {department}\n" + "\n".join(reports) + "\n")
    else:
        print(f"Отчет типа '{args.report}' не поддерживается")

if __name__ == "__main__":
    main()
