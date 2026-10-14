import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. Настройка конфигурации страницы
st.set_page_config(
    page_title="AI Банковский Аналитик",
    page_icon="🏦",
    layout="centered"
)


# 2. Загружаем сохраненную модель
@st.cache_resource  # Кэшируем модель, чтобы она не перезагружалась при каждом клике
def load_model():
    return joblib.load('rf_model.pkl')


model = load_model()

# 3. Заголовок и описание интерфейса
st.title("🏦 Прогнозирование оттока клиентов банка")
st.write("""
Данный сервис позволяет оценить вероятность ухода клиента из банка на основе его демографических 
и поведенческих характеристик. Заполните анкету слева и по центру, чтобы получить прогноз ИИ.
""")

st.divider()

# 4. Формируем интерфейс ввода данных (2 колонки для компактности)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Профиль клиента")
    age = st.slider("Возраст клиента", min_value=18, max_value=90, value=35)
    gender = st.selectbox("Пол", ["Мужской", "Женский"])
    credit_score = st.slider("Кредитный рейтинг", min_value=300, max_value=850, value=650)
    tenure_months = st.number_input("Время жизни в банке (месяцев)", min_value=0, max_value=120, value=24)
    has_credit_card = st.radio("Есть ли кредитная карта?", ["Да", "Нет"])

with col2:
    st.subheader("📊 Финансы и активность")
    current_balance = st.number_input("Текущий баланс на счете (руб.)", min_value=0.0, value=150000.0, step=5000.0)
    estimated_salary = st.number_input("Предполагаемая зарплата (руб.)", min_value=0.0, value=85000.0, step=5000.0)
    products_count = st.slider("Количество используемых продуктов", min_value=1, max_value=4, value=2)
    tx_count_3m = st.number_input("Количество транзакций за 3 мес.", min_value=0, value=30)
    tx_amount_3m = st.number_input("Сумма транзакций за 3 мес. (руб.)", min_value=0.0, value=45000.0, step=1000.0)
    complaints_count_3m = st.selectbox("Были ли жалобы за последние 3 мес.?", ["Нет", "Да"])

st.divider()

# 5. Кнопка запуска предсказания
if st.button("🚀 Рассчитать риск оттока", type="primary"):

    # Переводим интерфейсные ответы в числовой формат для модели
    gender_M = 1 if gender == "Мужской" else 0
    has_card_bin = 1 if has_credit_card == "Да" else 0
    complaints_bin = 1 if complaints_count_3m == "Да" else 0

    # Считаем новую бизнес-метрику, которую мы использовали при обучении
    avg_tx_amount = round(tx_amount_3m / tx_count_3m, 2) if tx_count_3m > 0 else 0.0

    # Собираем словарь в точном соответствии с порядком колонок в X_train
    # ['age', 'credit_score', 'has_credit_card', 'tenure_months', 'current_balance',
    #  'estimated_salary', 'products_count', 'tx_count_3m', 'tx_amount_3m',
    #  'complaints_count_3m', 'avg_tx_amount', 'gender_M']

    input_data = pd.DataFrame([{
        'age': age,
        'credit_score': credit_score,
        'has_credit_card': has_card_bin,
        'tenure_months': tenure_months,
        'current_balance': current_balance,
        'estimated_salary': estimated_salary,
        'products_count': products_count,
        'tx_count_3m': tx_count_3m,
        'tx_amount_3m': tx_amount_3m,
        'complaints_count_3m': complaints_bin,
        'avg_tx_amount': avg_tx_amount,
        'gender_M': gender_M
    }])

    # Получаем вероятность класса 1 (отток)
    churn_probability = model.predict_proba(input_data)[0][1]

    # Отрисовываем красивый виджет результата в зависимости от уровня риска
    st.subheader("Результат анализа модели:")

    if churn_probability < 0.35:
        st.success(f"🟢 Низкий риск оттока. Вероятность: {churn_probability:.1%}")
        st.info("💡 Рекомендация: Стандартное обслуживание, клиент лоялен.")
    elif 0.35 <= churn_probability < 0.70:
        st.warning(f"🟡 Средний риск оттока. Вероятность: {churn_probability:.1%}")
        st.info("💡 Рекомендация: Стоит отправить профилактическое персональное предложение или кэшбек.")
    else:
        st.error(f"🔴 КРИТИЧЕСКИЙ РИСК ОТТОКА! Вероятность: {churn_probability:.1%}")
        st.info(
            "💡 Рекомендация: Требуется срочный звонок менеджера! Возможно начисление бонусов или скидка на обслуживание.")
