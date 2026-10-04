# CallDeviceMenu

Пользовательское меню на конкретной кассе для конкретного логического устройства

Схемы: `schemas/qryCallDeviceMenu.xsd` (схемы ответа нет)
Влияние: изменяет данные

## Практика

- MENUOPERATION@operationId - из ответа ListDeviceMenu. Если меню у устройства пустое - "Menu ... is not found".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [CallDeviceMenu]
    <Station> [refItem]  - Станция, с которой надо запросить меню
    <Device> [refItem]  - Логическое устройство, для которого надо запросить меню
    <MENUOPERATION> [MENUOPERATION]
      <DIALOGINFO>?
        @from: string
        @to: string
      @operationId: string
    @CMD: string = "CallDeviceMenu"
  <RK7Command>+ [CallDeviceMenu] (структура - см. выше)
  <RK7Command2>+ [CallDeviceMenu] (структура - см. выше)
```

## Пример: CallDeviceMenu

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CallDeviceMenu">
    <Station id="{{stationId}}"/>
    <Device id="{{deviceId}}"/>
    <MENUOPERATION operationId="1"/>
  </RK7CMD>
</RK7Query>
```
