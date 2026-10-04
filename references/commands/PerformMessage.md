# PerformMessage

[Касса] Выполнить операцию с ожиданием завершения

Схемы: `schemas/qryPerformMessage.xsd`, `schemas/resPerformMessage.xsd`
Влияние: изменяет данные

## Практика

- Выполняется XML-интерфейсом самой кассы: кассовый сервер отвечает "Unknown command PerformMessage".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "PerformMessage"
  @message!: positiveInteger  - Сообщение
  @wparam: positiveInteger  - Параметр wParam сообщения
  @lparam: positiveInteger  - Параметр lParam сообщения
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@Result!: int  - Результат выполнения
```

## Пример: PerformMessage

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="PerformMessage" message="1024" wparam="1" lparam="1"/>
</RK7Query>
```
