# parser
2 варианта скрипта для обнаружения и структурирования данных о видеозаписях на хостинге kinexcope.io:

[python3](./main.py) и [powershell](./parser.ps1)

Оба скрипта выполняют отдно и то же:
- Находит страницу с видео на хостинге kinescope.io.
- Сохраняет ссылку на страницу, название видео, дату загрузки на хостинг в файл csv.
- В случае соответствия имени видео с опредленным шаблоном предполагается, что автор этого видео - онлайн школа Netology.
