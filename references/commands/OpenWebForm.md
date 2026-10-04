# OpenWebForm

[Касса, Кассовый сервер] Показать на кассе окно с web-браузером

Схемы: `schemas/qryOpenWebForm.xsd`, `schemas/resOpenWebForm.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Ответ приходит только после закрытия окна на кассе; HTTP-запрос обычно обрывается по таймауту (~60 с). Окно закрывается CloseWebForm с тем же extguid.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station> [refItem]  - Касса
  <Waiter>? [refItem]  - Официант. Если задан, то сообщение получит только этот официант. Если не задан, то сообщение будет отправлено на станцию Station и его получит первый залогинившийся официант
  @CMD: string = "OpenWebForm"
  @url!: normalizedString  - URL который нужно открыть в браузере. Используются следующие подстановки: {waiter.code} заменяется на код текущего официанта {extguid} заменяется на значение атрибута extguid из данного запроса
  @extguid!: normalizedString  - Случайный guid, используется как идентификатор сеанса
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@openstatus: TOpenFormStatus {0 | 1 | 2}  - Статус открытия формы
@closetatus: TCloseFormStatus {1 | 2}  - Статус закрытия формы
```

## Пример: OpenWebForm

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="OpenWebForm" url="https://example.com/?w={waiter.code}" extguid="{{lockGuid}}">
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
