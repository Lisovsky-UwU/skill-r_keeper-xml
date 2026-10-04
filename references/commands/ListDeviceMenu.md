# ListDeviceMenu

Пользовательское меню на конкретной кассе для конкретного логического устройства

Схемы: `schemas/qryListDeviceMenu.xsd`, `schemas/resListDeviceMenu.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [ListDeviceMenu]
    <Station> [refItem]  - Станция, с которой надо запросить меню
    <Device> [refItem]  - Логическое устройство, для которого надо запросить меню
    @CMD: string = "ListDeviceMenu"
  <RK7Command>+ [ListDeviceMenu] (структура - см. выше)
  <RK7Command2>+ [ListDeviceMenu] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<DeviceMenu> [DeviceMenuGroup]
  (одно из:)
    <DeviceMenu>* [DeviceMenuGroup] (структура - см. выше)
    <DIALOGINFO>?
      @dialogType!: string {DateInterval | NumberInterval | OneDate | OneNumber}
      @caption: string
  @caption!: string
  @operationId: string
```

## Пример: ListDeviceMenu

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ListDeviceMenu">
    <Station id="{{stationId}}"/>
    <Device id="{{deviceId}}"/>
  </RK7CMD>
</RK7Query>
```
