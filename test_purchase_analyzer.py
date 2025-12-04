import os
from purchase_analyzer import *
import pytest

def test_read_valid_purchases():
    purchases = """2025-09-01;food;Milk 2.5%;1.20;2
2025-09-01;food;Bread;0.85;1
2025-09-14;food;Chocolate bar;;2
2025-09-12;home;Towel set;10.00;1;extra"""
    with open("test_file.txt", 'w', encoding='utf-8') as file:
        file.write(purchases)
    purchases = read_purchases("test_file.txt")
    try:
        assert len(purchases) == 2
        assert purchases[0]['date'] == '2025-09-01'
        assert purchases[1]['category'] == 'food'
        assert purchases[0]['name'] == 'Milk 2.5%'
        assert purchases[1]['price'] == 0.85
        assert purchases[0]['qty'] == 2
    finally:
        os.unlink("test_file.txt")


def test_count_errors():
    purchases = """2025-09-01;food;Milk 2.5%;1.20;2
    2025-09-01;food;Bread;0.85;1
    2025-09-14;food;Chocolate bar;;2
    2025-09-12;home;Towel set;10.00;1;extra"""
    with open("test_file.txt", 'w', encoding='utf-8') as file:
        file.write(purchases)
    errors = count_errors("test_file.txt")
    try:
        assert errors == 2
    finally:
        os.unlink("test_file.txt")

def test_total_spent():
    purchases = [
        {'date': '2025-09-01', 'category': 'food', 'name': 'Milk 2.5%', 'price': 1.20, 'qty': 2},
        {'date': '2025-09-01', 'category': 'food', 'name': 'Bread', 'price': 0.85, 'qty': 1},
        {'date': '2025-09-02', 'category': 'transport', 'name': 'Bus ticket', 'price': 1.50, 'qty': 4}
    ]
    total = total_spent(purchases)
    assert total == 1.20*2+0.85*1+1.50*4

def test_spent_by_category():
    purchases = [
        {'date': '2025-09-01', 'category': 'food', 'name': 'Milk 2.5%', 'price': 1.20, 'qty': 2},
        {'date': '2025-09-01', 'category': 'food', 'name': 'Bread', 'price': 0.85, 'qty': 1},
        {'date': '2025-09-02', 'category': 'transport', 'name': 'Bus ticket', 'price': 1.50, 'qty': 4}
    ]
    totals = spent_by_category(purchases)
    assert len(totals) == 2
    assert totals['food'] == 1.20*2+0.85*1
    assert totals['transport'] == 1.50*4

def test_top_n_expensive():
    purchases = [
        {'date': '2025-09-01', 'category': 'food', 'name': 'Milk 2.5%', 'price': 1.20, 'qty': 2},
        {'date': '2025-09-02', 'category': 'transport', 'name': 'Taxi ride', 'price': 15.40, 'qty': 1},
        {'date': '2025-09-03', 'category': 'food', 'name': 'Cheese', 'price': 3.75, 'qty': 2},
        {'date': '2025-09-02', 'category': 'transport', 'name': 'Bus ticket', 'price': 1.50, 'qty': 4},
        {'date': '2025-09-01', 'category': 'food', 'name': 'Bread', 'price': 0.85, 'qty': 1},
    ]
    top = top_n_expensive(purchases,3)
    assert len(top)==3
    assert top[0]['name'] == 'Taxi ride'
    assert top[1]['total'] == 3.75*2

def test_date_format():
    purchases = """2025-09-01;food;Milk 2.5%;1.20;2
    2025/09/01;food;Bread;0.85;1
    2025_09_14;food;Chocolate bar;;2"""
    with open("test_file.txt", 'w', encoding='utf-8') as file:
        file.write(purchases)
    purchases = read_purchases("test_file.txt")
    try:
        assert purchases[0]['date'] == '2025-09-01'
        assert purchases[0]['name'] == 'Milk 2.5%'
    finally:
        os.unlink("test_file.txt")
