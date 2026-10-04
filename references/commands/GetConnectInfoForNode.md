# GetConnectInfoForNode

Получение низкоуровневой информации о подключенном узле

Схемы: `schemas/qryGetConnectInfoForNode.xsd`, `schemas/resGetConnectInfoForNode.xsd`
Влияние: только чтение

## Практика

- NetName - сетевое имя станции (атрибут NetName в справочнике CASHES). Для имени самого кассового сервера ответ "Node ... is not connected".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [GetConnectInfoForNode]
    @CMD: string = "GetConnectInfoForNode"
    @NetName: string  - Сетевое имя подключенного узла
  <RK7Command>+ [GetConnectInfoForNode] (структура - см. выше)
  <RK7Command2>+ [GetConnectInfoForNode] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ConnectInfo>?  - Информация о подключении
  @SelfIP: normalizedString  - IP узла, к которому был обращён XML запрос, в рамках подключения
  @SelfPort: integer  - Порт узла, к которому был обращён XML запрос, в рамках подключения
  @PeerIP: normalizedString  - IP интересующего узла в рамках подключения
  @PeerPort: integer  - Порт интересующего узла в рамках подключения
```

## Пример: GetConnectInfoForNode

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetConnectInfoForNode" NetName="{{stationNetName}}"/>
</RK7Query>
```
