"""Manual-ledger summaries. Savings and investments are transfers, not expenses."""
from calendar import monthrange
from datetime import date

CATEGORY_BUDGETS={'Essentials':'needs','Enjoyment':'joy','Move / glasses / irregular':'buffer','Learning':'learning'}


def previous_month(month):
    day=date.fromisoformat(month+'-01')
    return f'{day.year-1}-12' if day.month==1 else f'{day.year}-{day.month-1:02d}'


def month_totals(transactions, month, through=None):
    rows=[t for t in transactions if t['date'].startswith(month) and (not through or t['date']<=through)]
    income=sum(float(t['amount']) for t in rows if t['type']=='Income')
    expense=sum(float(t['amount']) for t in rows if t['type']=='Expense')
    savings=sum(float(t['amount']) for t in rows if t['type']=='Savings transfer')
    investing=sum(float(t['amount']) for t in rows if t['type']=='Investment transfer')
    return {'rows':rows,'income':round(income,2),'expense':round(expense,2),
            'savings':round(savings,2),'investing':round(investing,2),
            'transfers':round(savings+investing,2),'net':round(income-expense-savings-investing,2)}


def money_dashboard(transactions, month, budget, today):
    # Future-dated entries are never presented as money already received or spent.
    actual=[t for t in transactions if t['date']<=today.isoformat()]
    totals=month_totals(actual,month)
    previous=previous_month(month)
    elapsed=today.day if month==today.strftime('%Y-%m') else monthrange(int(month[:4]),int(month[5:]))[1]
    previous_length=monthrange(int(previous[:4]),int(previous[5:]))[1]
    cutoff_day=min(elapsed,previous_length) if month==today.strftime('%Y-%m') else previous_length
    cutoff=f'{previous}-{cutoff_day:02d}'
    prior=month_totals(actual,previous,cutoff)
    expenses=[t for t in totals['rows'] if t['type']=='Expense']
    categories={}
    daily={}
    for t in expenses:
        categories[t['category']]=round(categories.get(t['category'],0)+float(t['amount']),2)
        daily[t['date']]=round(daily.get(t['date'],0)+float(t['amount']),2)
    comparison=[]
    for category,key in CATEGORY_BUDGETS.items():
        planned=float(budget.get(key,0)); spent=categories.get(category,0)
        comparison.append({'Priority':category,'Planned (₱)':planned,'Actual (₱)':spent,'Remaining (₱)':round(planned-spent,2)})
    other=sum(v for k,v in categories.items() if k not in CATEGORY_BUDGETS)
    if other: comparison.append({'Priority':'Other spending','Planned (₱)':0.,'Actual (₱)':other,'Remaining (₱)':-other})
    for title,key,actual_key in [('Savings contributions','emergency','savings'),('Investment contributions','investing','investing')]:
        planned=float(budget.get(key,0)); amount=totals[actual_key]
        comparison.append({'Priority':title,'Planned (₱)':planned,'Actual (₱)':amount,'Remaining (₱)':round(planned-amount,2)})
    months=[month]
    for _ in range(5): months.insert(0,previous_month(months[0]))
    trend=[{'Month':m,'Income':(t:=month_totals(actual,m))['income'],'Expenses':t['expense'],'Transfers':t['transfers']} for m in months]
    return {**totals,'categories':categories,'daily':daily,'comparison':comparison,'trend':trend,
            'expense_count':len(expenses),'daily_average':round(totals['expense']/elapsed,2),
            'previous':prior,'previous_cutoff':cutoff,'elapsed':elapsed}
