# DeviceStatuses

Пользовательское меню на конкретной кассе для конкретного логического устройства

Схемы: `schemas/qryDeviceStatuses.xsd`, `schemas/resDeviceStatuses.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [DeviceStatuses]
    @CMD: string = "DeviceStatuses"
  <RK7Command>+ [DeviceStatuses] (структура - см. выше)
  <RK7Command2>+ [DeviceStatuses] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Devices> [Devices]
  <Device>*
    <DeviceState>? [deviceState]
      <PaperStatus>?
        @PaperOut: boolean  - Флаг - в принтере закончилась бумага
        @PaperLow: boolean  - Флаг - бумага близка к окончанию
        @DoorOpen: boolean  - Флаг - у принтера открыта крышка
        @PaperOther: boolean  - Флаг - неизвестная проблема с бумагой
      <LogicStatus>?
        @Fisc24Out: boolean  - Флаг - прошло 24 часа с момента закрытия общей смены, продолжение работы невозможно
        @EKLZNearEnd: boolean  - Флаг - ЭКЛЗ близок к заполнению
      <ExtDeviceState>? [extDeviceState]
        <любой XML>
      @Online: boolean  - Флаг - устройство подключено и работает
    @Ident!: positiveInteger  - Идентификатор логического устройства (принтера/терминала авторизации)
    @code!: positiveInteger  - Код логического устройства
    @name!: string  - Наименование логического устройства
    @guid: guidString  - GUID логического устройства
    @loaded: boolean  - Флаг - драйвер устройста загружен
```

## Пример: DeviceStatuses

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeviceStatuses"/>
</RK7Query>
```
