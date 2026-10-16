Проект: Интеллектуальная система прогнозирования оттока клиентов банка (End-to-End).

Что сделано: Спроектировал реляционную структуру БД (SQLite), заполнил ее данными и написал оптимизированный SQL-запрос для агрегации продуктовых метрик. Провел EDA, выявил ключевые триггеры оттока (жалобы, падение активности). Обучил модели Random Forest и Logistic Regression, применил техники борьбы с дисбалансом классов. Сбалансированная модель Random Forest достигла метрики ROC-AUC > 0.85.

Результат: Обернул модель в интерактивный веб-сервис на Streamlit и развернул в облаке.

Стек: Python, SQL, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Streamlit.

Ссылка на рабочий прототип: https://churn-prediction-project-qp5tnp8igcaqgf7vrr8blu.streamlit.app

Ссылка на код GitHub: https://github.com/igorvolchek98/churn-prediction-project

Скриншот работающего интерфейса:

<img width="548" height="857" alt="image" src="https://github.com/user-attachments/assets/63d54ecd-28dd-4031-bbdd-c502b5b21c91" />

Структура проекта:

<img width="676" height="284" alt="image" src="https://github.com/user-attachments/assets/1f7c7c86-916d-4ce9-859c-4e827d27dd1c" />


Как запустить приложение локально:
1. Загрузите репозиторий с github:  https://github.com/igorvolchek98/churn-prediction-project
2. Откройте ваш терминал (командную строку) и перейдите в папку проекта:
   cd путь_к_вашей_папке_с_проектом
3. Установите библиотеку Streamlit (если она еще не установлена):
   pip install streamlit
4. Запустите приложение командой:
   streamlit run app.py
5. После этого в терминале появится локальная ссылка, а в вашем браузере автоматически откроется вкладка с банковским интерфейсом. Попробуйте изменить значения (особенно количество транзакций, сумма транзакций, кредитный рейтинг) и посмотрите, как реагирует модель!

