import random

import faker

from superweb import database

fake = faker.Faker()

for x in range(50):
    is_completed = random.random() < 0.25
    task_item = database.Task(
        title=fake.bs(),
        description=' '.join(fake.sentences(3)),
        is_completed=is_completed,
        created_at=fake.date_time_this_year(),
        completed_at= fake.date_time_this_year() if is_completed else None,
        deadline_at=fake.date_time_this_year(before_now=True, after_now=True) if random.random() < 0.75 else None
    )
    task_item.save()
