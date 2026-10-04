# PostMessage

[Касса] Поместить сообщение в очередь сообщений

Схемы: `schemas/qryPostMessage.xsd`, `schemas/resPostMessage.xsd`
Влияние: изменяет данные

## Практика

- Выполняется XML-интерфейсом самой кассы: кассовый сервер отвечает "Unknown command PostMessage".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "PostMessage"
  @message!: positiveInteger  - Сообщение
  @wparam: positiveInteger  - Параметр wParam сообщения
  @lparam: positiveInteger  - Параметр lParam сообщения
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@Result!: int  - Результат выполнения
```

## Пример: PostMessage

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="PostMessage" message="1024" wparam="1" lparam="1"/>
</RK7Query>
```
