# CreaterkFriendsAnchor

Создание якоря лояльности на основе содержимого для конкретного заказа

Схемы: `schemas/qryCreateRkFriendsAnchor.xsd`, `schemas/resCreateRkFriendsAnchor.xsd`
Влияние: изменяет данные

## Практика

- Имя команды в запросе - CreaterkFriendsAnchor (так ее объявляет GetFunctions; схема лежит в qryCreateRkFriendsAnchor.xsd). Написание CreateRkFriendsAnchor сервер тоже принимает, хотя в остальном имена команд чувствительны к регистру.
- Без настроенной лояльности r_k Friends сервер отвечает Ok с пустым rkFriendsAnchor и пустым ClientInfo - проверяйте поля, а не только Status.
- В актуальном наборе XSD атрибут rkFriendsAnchor остался у CreateOrder и UpdateOrder, а из CalcOrder убран.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  @CMD: string = "CreaterkFriendsAnchor"
  @phone: normalizedString  - номер телефона участника лояльности
  @token: normalizedString  - токен идентификации участника лояльности
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ClientInfo> [rkFriendsClientInfo]  - Информация об участнике
  @Name!: normalizedString
  @HasVk!: boolean
  @HasMax!: boolean
  @HasTelegram!: boolean
  @BonusesAvailable!: positiveInteger
@rkFriendsAnchor: normalizedString  - Якорь лояльности (идентификатор заявки)
```

## Пример: CreaterkFriendsAnchor

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CreaterkFriendsAnchor" phone="{{loyaltyPhone}}">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
