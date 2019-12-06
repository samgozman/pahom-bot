# Что такое Пахом Бот
[![Пообщайся с Пахомом](https://img.shields.io/badge/Chat%20on-Telegram-blue.svg)](https://teleg.run/dp10_bot)  [![Да, мы тоже умеет использовать Shields.io](https://img.shields.io/badge/build-passing-brightgreen)](https://yopta.space)  [![Ага, ага](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://yopta.space)  [![Ага, ага](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://yopta.space) 
[![Ага, ага](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen)](https://yopta.space) 
[![МАНИ](https://img.shields.io/badge/price-%240-brightgreen)](https://yopta.space) 

[Бот](https://teleg.run/dp10_bot) Пахом это совершенно новое слово в Digital среде мира Data Since! Бот представляет из себя самый совершенный Artificial Intelligence в мире состоящий из огромных массивов Big Data, собранных с помощью кропотливой работы Computer Vision и Machine Learning, построенных на базе нашей собственной Neural Network. 

Благодаря современным подходам в Iterative Deepening Depth-First Search (IDDFS) обеспечена максимальная Big Data Veracity наших данных. 

Чтобы бот эволюционировал не только в знаниях, но и в умениях были применены последние Know-How в области AutoML.

Команда проекта работала строго по методологиям Scrub, Agile и Kanban используя такие современные сервисы как Mind Maps, Trello Boards, Daru Dar and Avito (we all want to eat, don’t we?).

When writing the code, we used the most modern methodologies, such as Neuro-Linguistic Programming, MVC, PEP8 and a complete rejection of camel-case and Stackoverflow. All this allowed us to implement the most perfect telegram-bot on the planet.

But unfortunately, like many ingenious inventions, our AI bot suffered a setback –  in the course of his Machine Learning, he acquired schizophrenia, autism and complete degradation of the personality. He began to speak incomprehensibly, watch My Little Pony, compose fan fiction and honor Vladimir Putin.

About Vladimir Putin he said: Lorem ipsum dolor sit amet, consectetur adipiscing elit. In semper rutrum augue, at consectetur metus. Quisque propaganda eget ligula a sem condimentum fermentum. Quisque eget sem consequat, molestie lectus nec, aliquam massa. Nunc semper turpis ligula, dignissim rutrum navalny felis ultrices eget. Nulla nec vehicula dolor, hendrerit scelerisque lorem. Nulla tristique urna non lacus tincidunt semper. Mauris pulvinar dignissim nisl quis tempor. Cras enim quam, imperdiet volutpat magna eget, ullamcorper efficitur libero. 

Nullam sit amet metus ut ipsum commodo facilisis sed sed est. Suspendisse potenti. No one will notice if I write the word "penis" here. Aliquam semper urna varius elit lacinia convallis. In fringilla vel erat a rutrum. Pellentesque habitant morbi tristique militarism senectus et netus et malesuada fames ac turpis egestas. Maecenas fermentum convallis erat, eu dictum leo rhoncus ac.


## Варианты применения
Как уже стало понятно из текста выше, текстовая база бота собрана из шизофренического фанфика. Текстовые данные прошли через Цепь Маркова.

К нашему удивлению, после генерации "марковки" исходный текст стал более понятным и осмысленным.

Бот может использоваться:

* для имитации общения реального человека
* для генерации "текста рыбы"
* для генерации пользовательских соглашений, которые всё равно никто не читает
* для откровенного спама и угара над друзьями

## Пример работы и история создания

Было проделано много работы, чтобы демонстрация была успешной.

Для примера мы спарсили открытую информацию (фанфики, истории, посты итд) человека с легкой шизофренией. Спросите почему именно его? Дело всё в том, что бот далеко не всегда попадает в ответ ввиду того, что при построении предложения не учитывает контекст, а лишь вероятность появления одного слова после другого.

Примерно в таком же стиле и общался наш объект исследования. Ни на один вопрос он никогда не отвечал по теме (что послужило для нас оправданием для прикрытия слабых сторон программы). Также он был известен тем, что придумал себе несколько десятков однотипных персонажей, которые жили у него в голове (ДП-10, ДП-13, Вельбодос, Димси, Тобзи и другие). От их имени он писал небольшие "рассказы", а иногда и общался.

Разговаривать с ним было крайне интересно и необычно, но вот не задача - ответа от него можно ждать месяц, год и более. А иногда он сам тебе пишет под сотню сообщений не в попад. Потому все кто с ним не был знаком называли его ботом. Хотелось сделать нечто похожее, но, чтобы ответ был моментальным - и у нас получилось! Бот отвечает 1 в 1 как оригинал, но за небольшим отличием - он хотябы пытается отвечать по теме!

Для того, чтобы ответы на вопросы стали более релевантными, пришлось разбить оригинальные тексты на тематики (всего мы насчитали 32 и сделали для них парсер), и для более удобного заполнения подходящих вопросов мы заюзали Google DialogFlow (однако в будущем он нам не сильно пригодится, потому подключение к нему является опциональным).

Результат вы можете оценить, пообщавшись с ботом в телеграмме: [@dp10_bot](https://teleg.run/dp10_bot).



### Подготовка текста
Стоит начать со сбора оригинального текста, на котором будет базироваться модель Маркова. В случае с человеком это могут быть личные диалоги, комментарии, посты итд. 

Вместо человека источником изначальных данных может послужить книга или заранее подготовленный файл с однотипными текстами (например база пользовательских соглашений для последующий генерации).

В итоге у вас должен получится .txt файл с текстом. Если в тексте присутсвуют личные обращения, то рекомендуется их заменить на ANONIM - тогда будет происходить подстановка имени пользователя при обращении бота к нему.

При старте скрипта производится генерация модели на основе цепей Маркова. Исходными данными выступает заранее подготовленный текст, на основе которого генерируется модель практически неограниченного размера.

Чем разнообразнее и больше исходные данные, тем лучше будет исходная модель. В нашем примере исходные данные находятся в файле **shiza.txt**. 
