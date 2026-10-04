# GetBatchOfGoodsList

[Кассовый сервер] Список зарегистрированных партий маркированной продукции

Схемы в наборе UCS нет - страница собрана из проверки на сервере.
Влияние: только чтение

## Практика

- Схемы в наборе UCS нет, команда объявлена в GetFunctions и работает; партии добавляются AddBatchOfGoods, удаляются DeleteBatchOfGoods.

## Пример: GetBatchOfGoodsList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetBatchOfGoodsList"/>
</RK7Query>
```
