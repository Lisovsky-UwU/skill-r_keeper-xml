# ChangeDrawerBalance

[Кассовый сервер] Внести/изъять деньги из ящика

Схемы: `schemas/qryChangeDrawerBalance.xsd`, `schemas/resChangeDrawerBalance.xsd`
Влияние: изменяет данные

## Практика

- Drawer - кассовый ящик, логическое устройство из DEVICES. Если ящик нельзя определить по кассиру, ошибка "child element Drawer not found".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Cashier> [refItem]  - Кассир (работник выполняющий внесение/изъятие)
  <Currency> [refItem]  - Валюта
  <Reason>? [refItem]  - Причина внесения/выдачи денег
  <Drawer>? [refItem]  - Кассовый ящик. Если не задан, то ящик определяется по кассиру
  <Maket>? [refItem]  - Макет для печати документа о внесении/выдачи
  @CMD: string = "ChangeDrawerBalance"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @amount: long  - Сумма (в копейках). Если больше нуля, то внесение, иначе изъятие денег
```

## Пример: ChangeDrawerBalance

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ChangeDrawerBalance" amount="100">
    <Cashier id="{{cashierId}}"/>
    <Currency id="{{currencyId}}"/>
    <Reason id="{{depositReasonId}}"/>
  </RK7CMD>
</RK7Query>
```
