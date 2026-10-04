# MakeCardDeposit

[Кассовый сервер] Пополнить/изъять средства с/на карту ПДС

Схемы: `schemas/qryMakeCardDeposit.xsd`, `schemas/resMakeCardDeposit.xsd`
Влияние: изменяет данные

## Практика

- Ответ - CardInfo после операции. Ok означает, что карточная система приняла операцию; изменился ли баланс, зависит от ее настройки - сверяйте через GetCardInfo.
- Списание сверх лимита - "Персональное ограничение для ... = ..." (RK7ErrorN 2142).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Interface> [refItem]  - Интерфейс, который будет обрабатывать карту
  <Station> [refItem]  - Станция
  <Cashier> [refItem]  - Кассир
  <Currency> [refItem]  - Валюта
  <Reason>? [refItem]  - Причина внесения/выдачи денег
  @CMD: string = "MakeCardDeposit"
  @cardCode!: normalizedString  - Код карты
  @amount!: int  - Сумма. Если сумма > 0, то будет оформлено пополнение баланса карты, если сумма < 0, то будет выполнено изъятие денег с карты
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<CardInfo>
  <Discount> [resRefItem]  - Скидка
  <BonusType> [resRefItem]  - Тип бонуса
  <Defaulter> [resRefItem]  - Неплательщик
  <Currency>+  - Валюта
    (resRefItem: id | code | guid)
    @subacc: nonNegativeInteger  - Номер субсчета
    @maxAmount: nonNegativeInteger  - Максимальная сумма (в копейках)
    @amount: nonNegativeInteger  - Остаток (в копейках)
  @cardCode: normalizedString  - Код карты
  @holder: normalizedString  - Владелец карты
  @maxAmount: nonNegativeInteger  - Максимальная сумма (в копейках)
  @amount: nonNegativeInteger  - Остаток (в копейках)
  @maxDisc: nonNegativeInteger  - Максимальная сумма скидки (в копейках)
```

## Пример: MakeCardDeposit

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="MakeCardDeposit" cardCode="{{cardCode}}" amount="100">
    <Interface id="{{pdsInterfaceId}}"/>
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
    <Currency id="{{currencyId}}"/>
  </RK7CMD>
</RK7Query>
```
