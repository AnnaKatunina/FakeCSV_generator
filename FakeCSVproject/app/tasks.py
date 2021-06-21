import csv
from random import randint

from FakeCSVproject.app.fake_data import get_fake_data
from FakeCSVproject.app.models import Column, Schema, Dataset
from FakeCSVproject.celery import app


@app.task
def generate_csv_file(schema_id, number_rows, dataset_id):
    schema = Schema.objects.get(pk=schema_id)
    dataset = Dataset.objects.get(pk=dataset_id)
    columns = Column.objects.filter(schema=schema).order_by('order')
    columns_names = [column.name for column in columns]
    delimiter = schema.column_separator
    quotechar = schema.string_character
    dataset_number = randint(100000, 9999999)
    filename = f'Dataset_to_Schema_{schema}_{dataset_number}.csv'
    with open('media/' + filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC, delimiter=delimiter)
        writer.writerow(columns_names)
        for _ in range(number_rows):
            fake_data = []
            for column in columns:
                fake_data.append(get_fake_data(column.type, column.From, column.To))
            writer.writerow(fake_data)
        dataset.csv_file = filename
        dataset.status = Dataset.Status.READY

        dataset.save()
        print(dataset.created)
        print(dataset.status)
    return
