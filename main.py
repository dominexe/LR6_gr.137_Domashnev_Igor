from purchase_analyzer import *

if __name__ == "__main__":
    purch = read_purchases("purchases.txt")
    print("Запущена функция read_purchases")
    print("Исправленный файл purchases.txt:")
    print(f"{purch}\n")
    print("Запущена функция count_errors")
    print(f"Число пропущенных строк:{count_errors("purchases.txt")}\n")
    print("Запущена функция total_spent")
    print(f"Сумма трат:{total_spent(purch)}\n")
    print("Запущена функция spent_by_category")
    print(f"Суммы трат по всем категориям:{spent_by_category(purch)}\n")
    print("Запущена функция top_n_expensive")
    print(f"Топ-3 покупки по стоимости:{top_n_expensive(purch, 3)}\n")
    print("Запущена функция write_report")
    report_path = "report.txt"
    write_report(purch, count_errors("purchases.txt"), report_path)
    print("Файл report.txt готов")
