# Recommender-System

1. В подсчете рекомендательной оценки для каждого фильма F среди всех потенциальных фильмов используются оценки всех других пользователей.
2. Для каждого фильма отдельно для будних дней и отдельно для выходных считаются следующие показатели:
   - Количество просмотров
   - Мат.ожидание (среднее) оценки
   - Среднеквадратичное отклонение оценки
   - Проверяем гипотезу: фильм F более интересен в будний день, чем в выходной - через критерий достоверности t (Небольшая справка из статистики). Ведем два списка: с фильмами, для которых зависимость подтверждена, и с фильмами, для которых гипотеза не доказана. Модифицируем вычисленную в задании 1 оценку, умножив ее на соотношение (средняя оценка в будний день/средняя оценка в выходной). Т.о. повышаются оценки для фильмов, которые "более интересны в будний день" и понижаются для фильмов, которые "менее интересны в будний день".
3. Затем, по очереди ищем максимальную оценку в следующих списках:
      1. В списках фильмов, которые достоверно "более интересны в будний день"
      2. В списках фильмов, для которых не доказана более высокая степень "интереса в будний день"
      3. Если оба предыдущих списка говорят о негативном влиянии контекста на прогнозируемые оценки пользователя (максимальное модифицированное значение будет ниже 3), ищется максимальная оценка без учета контекста.

В примере для 14 пользователя имеется только один фильм - 16-ый - для которого подтверждена гипотеза (почти вдвое более интересен в будние, чем в выходные), и для него прогнозируется высокая оценка, поэтому данный фильм мы можем порекомендовать пользователю.
