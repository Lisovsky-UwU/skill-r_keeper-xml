# WaitWindow

[Касса] Ожидание появления опреденного окна

Схемы: `schemas/qryWaitWindow.xsd`, `schemas/resWaitWindow.xsd`
Влияние: изменяет данные

## Практика

- Выполняется XML-интерфейсом самой кассы: кассовый сервер отвечает "Unknown command WaitWindow".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "WaitWindow"
  @form!: positiveInteger  - Идентификатор типа формы
  @timeout: dateTime  - Таймаут ожидания
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@form!: int  - Идентификатор текущей активной формы
```

## Пример: WaitWindow

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="WaitWindow" form="1" timeout="2000-01-01T00:00:05"/>
</RK7Query>
```
