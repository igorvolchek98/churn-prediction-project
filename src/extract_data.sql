SELECT 
    c.client_id,
    c.age,
    c.gender,
    c.credit_score,
    c.has_credit_card,
    -- Считаем, сколько месяцев клиент пользуется банком (на текущую дату в 2026 году)
    CAST((JULIANDAY('2026-10-13') - JULIANDAY(c.registration_date)) / 30.4 AS INT) AS tenure_months,
    
    b.current_balance,
    b.estimated_salary,
    b.products_count,
    
    -- Обрабатываем возможные пропуски в транзакциях (если транзакций не было, ставим 0)
    COALESCE(t.tx_count_3m, 0) AS tx_count_3m,
    COALESCE(t.tx_amount_3m, 0.0) AS tx_amount_3m,
    COALESCE(t.complaints_3m, 0) AS complaints_count_3m,
    
    -- Новая бизнес-метрика: средний чек одной транзакции
    CASE 
        WHEN COALESCE(t.tx_count_3m, 0) > 0 THEN ROUND(t.tx_amount_3m / t.tx_count_3m, 2)
        ELSE 0.0
    END AS avg_tx_amount,
    
    -- Целевая переменная (ушел / не ушел)
    c.is_churned

FROM clients c
LEFT JOIN balances b ON c.client_id = b.client_id
LEFT JOIN transactions_aggr t ON c.client_id = t.client_id;