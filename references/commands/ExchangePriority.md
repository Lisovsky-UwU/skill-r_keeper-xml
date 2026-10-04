# ExchangePriority

Команда ExchangePriority - переставить местами элементы по приоритету

Схемы: `schemas/qryExchangePriority.xsd` (схемы ответа нет)
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Команда справочного сервера, как и SetRefData; кассовый сервер отвечает "Unknown command".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [RK7CommandExchangePriority]
    <Item1> [referentItem]  - Элемент справочника (идентификатор элемента)
      @Ident: nonNegativeInteger
      @GUIDString: normalizedString
      @* - допускаются любые другие атрибуты
    <Item2> [referentItem]  - Элемент справочника (идентификатор элемента) (структура - см. выше)
    @CMD!: string = "ExchangePriority"
    @RefName!: refName {PriceFormulas | ModiSchemeDetails | Filters | SelectorDetails | Taxes | TaxDishRules | TaxPayRules | TaxDishTypes | Kurses | ServiceChecks | DiscountDetails | DiscountCompositions | TariffDetails | PRICEFORMULAS | MODISCHEMEDETAILS | FILTERS | SELECTORDETAILS | TAXES | TAXDISHRULES | TAXPAYRULES | TAXDISHTYPES | KURSES | SERVICECHECKS | DISCOUNTDETAILS | DISCOUNTCOMPOSITIONS | TARIFFDETAILS}
  <RK7Command>+ [RK7CommandExchangePriority] (структура - см. выше)
  <RK7Command2>+ [RK7CommandExchangePriority] (структура - см. выше)
```

## Пример: ExchangePriority

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7Command CMD="ExchangePriority" RefName="MENUITEMS">
    <Item1 Ident="{{dishId}}"/>
    <Item2 Ident="{{dishId}}"/>
  </RK7Command>
</RK7Query>
```
