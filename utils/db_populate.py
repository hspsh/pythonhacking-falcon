from superweb import database

task_item = database.Task(title='Zrób PR na GitHubie',
                 description='Umieść pozdrowienia dla @upgrade i opisz jak bardzo chesz aby twój PR otrzymał merga. XOXO')
task_item.save()
