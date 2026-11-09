# 721–725 Python 测试标程

以下程序均使用 Python 3，并严格按照题目要求输出中文标点和两位小数。

## 721 进口成本与销售估算

```python
purchase_price = float(input())
exchange_rate = float(input())
tariff_rate, profit_rate = map(float, input().split())

purchase_cost = purchase_price * exchange_rate
total_cost = purchase_cost * (1 + tariff_rate)
selling_price = total_cost * (1 + profit_rate)

print(f"采购成本：{purchase_cost:.2f}元")
print(f"含税总成本：{total_cost:.2f}元")
print(f"建议销售价：{selling_price:.2f}元")
```

## 722 阶梯物流费用计算

```python
weight = float(input())

if weight <= 2:
    level = "2kg及以下档"
    fee = 50
elif weight <= 10:
    level = "2kg-10kg档"
    fee = 50 + (weight - 2) * 15
elif weight <= 30:
    level = "10kg-30kg档"
    fee = 170 + (weight - 10) * 12
else:
    level = "30kg以上档"
    fee = 410 + (weight - 30) * 10

print(f"计费档次：{level}")
print(f"物流总费用：{fee:.2f}元")
```

## 723 资产折旧计算

```python
value = float(input())
depreciation_rate = float(input())

for year in range(1, 9):
    value *= 1 - depreciation_rate
    print(f"第{year}年末设备余值：¥{value:.2f}")
```

注意：计算过程中不能把 `value` 手动舍入为两位小数，仅在输出时格式化。

## 724 每日客流量数据分析

```python
visitors = list(map(int, input().split()))

total = sum(visitors)
average = total // 7
maximum = max(visitors)
minimum = min(visitors)
max_day = visitors.index(maximum) + 1
min_day = visitors.index(minimum) + 1
below_average = [
    str(day)
    for day, count in enumerate(visitors, start=1)
    if count < average
]

print(f"总客流量：{total} 人次，日均：{average} 人次")
print(f"最高日期：第 {max_day} 天（{maximum} 人次）")
print(f"最低日期：第 {min_day} 天（{minimum} 人次）")
print("低于日均的日期：" + " ".join(below_average))
```

使用 `list.index()` 可以在最高值或最低值并列时得到最早出现的日期。

## 725 图书库存查询与管理

```python
inventory = {}

for _ in range(4):
    book_name, quantity = input().split()
    inventory[book_name] = int(quantity)

operation, book_name, quantity = input().split()
quantity = int(quantity)
inventory[book_name] = inventory.get(book_name, 0) + quantity
print("入库成功")

operation, book_name, quantity = input().split()
quantity = int(quantity)

if book_name not in inventory:
    print("图书不存在")
elif inventory[book_name] < quantity:
    print("库存不足")
else:
    inventory[book_name] -= quantity
    print("出库成功")

for book_name, quantity in inventory.items():
    print(f"{book_name}：{quantity}")
```

Python 3.7 及以上版本的字典会保持插入顺序，因此新入库的图书会输出在原有四本书之后。
