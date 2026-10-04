# RegisterLogs

Зарегистрировать маски файлов логов

Схемы: `schemas/qryRegisterLogs.xsd` (схемы ответа нет)
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [RegisterLogs]
    <Logs>
      <Log>+
        (текстовое содержимое: string)
        @Module!: string
        @Labels: string
    @CMD: string = "RegisterLogs"
  <RK7Command>+ [RegisterLogs] (структура - см. выше)
  <RK7Command2>+ [RegisterLogs] (структура - см. выше)
```

## Пример: RegisterLogs

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="RegisterLogs">
    <Logs>
      <Log Module="xmlinterface" Labels="">*.log</Log>
    </Logs>
  </RK7CMD>
</RK7Query>
```
