from multiprocessing.sharedctypes import Value

from sentry_sdk import continue_trace



def read_purchases(path):
    list=[]
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(';')
            if len(parts) != 5:
                continue
            date, category, name, price, qty = (part.strip() for part in parts)
            if not date or not category or not name or not price or not qty:
                continue
            if len(date) != 10 or date[4] != '-' or date[7] != '-':
                continue
            try:
                if ',' in str(price) or float(price)<0:
                    continue
                if int(qty) < 0:
                    continue
            except(ValueError, TypeError):
                continue
            price = float(price)
            qty = int(qty)
            purchase = {
                'date': date,
                'category': category,
                'name': name,
                'price': price,
                'qty': qty
            }
            list.append(purchase)
    return list


def count_errors(path):
    error_count = 0
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                error_count+=1
                continue
            parts = line.split(';')
            if len(parts) != 5:
                error_count += 1
                continue
            date, category, name, price, qty = (part.strip() for part in parts)
            if not date or not category or not name or not price or not qty:
                error_count += 1
                continue

            try:
                if ',' in str(price) or float(price)<0:
                    error_count += 1
                    continue
                if int(qty) < 0:
                    error_count += 1
                    continue
            except(ValueError, TypeError):
                error_count += 1
                continue
    return error_count



def total_spent(purchases):
    total = 0.0
    for purchase in purchases:
        total += purchase['price'] * purchase['qty']
    return total


def spent_by_category(purchases):
    list = {}
    for purchase in purchases:
        category = purchase['category']
        count = purchase['price'] * purchase['qty']
        if category in list:
            list[category] += count
        else:
            list[category] = count
    return list


def top_n_expensive(purchases, n):
    list = []
    for purchase in purchases:
        purchase_copy = purchase.copy()
        purchase_copy['total'] = purchase['price'] * purchase['qty']
        list.append(purchase_copy)
    sorted_list = sorted(list, key=lambda item: item['total'], reverse=True)
    return sorted_list[:n]

def write_report(purchases, errors, out_path):
    sorted_list2 = []
    with open(out_path, 'w', encoding='utf-8') as file:
        file.write(f"Валидных записей: {len(purchases)}\n")
        file.write(f"Некорректных строк: {errors}\n")
        total = total_spent(purchases)
        file.write(f"Всего потрачено: {total}\n\n")
        file.write(f"Траты по категориям:\n")
        sorted_list = spent_by_category(purchases)
        for category in sorted_list:
            file.write(f"{category}: {sorted_list[category]}\n")
            sorted_list2.append(f"{category}: {sorted_list[category]}")
        file.write(f"\n")
        file.write(f"Топ 3 самых дорогих категорий:\n")
        for category in sorted_list2[:3]:
            file.write(f"{category}\n")





