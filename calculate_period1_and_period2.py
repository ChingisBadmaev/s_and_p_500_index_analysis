import csv

# period_1 - period_2 = 7862400


def calculate_periods():
    period_1 = 1656633600
    period_2 = 1664496000
    diff = 7862400
    periods = []
    i = int(0)
    while i < 10:
        periods.append({'period_1': period_2, 'period_2': period_2})
        period_2 = period_1
        period_1 = period_2 - diff
        i += 1
    return periods


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([
            'period_1', 'period_2'])
        for item in items:
            writer.writerow([item['period_1'], item['period_2']])


print(calculate_periods())
