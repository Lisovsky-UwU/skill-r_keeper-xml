# KDSSetDishData3

[Кассовый сервер] Изменить статус готовности у блюда (КДС) ver 3

Схемы: `schemas/qryKDSSetDishData3.xsd`, `schemas/resKDSSetDishData3.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Employee>? [refItem]  - Работник, который изменяет статус
  <Station>? [refItem]  - Станция КДС, с которой вызывается запрос
  @CMD: string = "KDSSetDishData3"
  @line_guid!: normalizedString  - GUID строки блюда
  @kdsstate!: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed}  - Новый статус блюда
  @kdsrate!: int  - Коэффициент загруженности кухни. С версии 7.07.00.329
  @sendtovdu: boolean (по умолчанию "true")  - Флаг "Отправить заказ на VDU". Если включен, то заказ будет передан на VDU, иначе не будет. Версия 7.7.0.354+
  @kds_state_sender: normalizedString (по умолчанию "")  - Информация об отправителе запроса, пробрасывается на КДС/VDU (4-я версия протокола)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Station> [resRefItem]  - Станция КДС
<Manager> [resRefItem]  - Менеджер, изменивший статус КДС
@kdsstate!: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed}  - КДС статус блюда
@kdsrate!: int  - Коэффициент загруженности кухни. С версии 7.07.00.329
```

## Пример: KDSSetDishData3

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="KDSSetDishData3" line_guid="{{dishLineGuid}}" kdsstate="ready">
    <Employee id="{{waiterId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
