# LowAlcKegStatus

Проверка статуса отправки данных по кегу в Честный Знак

Схемы: `schemas/qryLowAlcKegStatus.xsd`, `schemas/resLowAlcKegStatus.xsd`
Влияние: только чтение

## Практика

- Для марки, которой нет среди поставленных кегов, - "Кег с маркировкой ... не найден".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Keg>  - Кег
    @markingData!: base64Binary  - Марка кега в base64
  @CMD: string = "LowAlcKegStatus"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Keg>  - Данные по кегу
  @markingData!: base64Binary  - Марка кега в base64
  @status!: HonestSignSendStatus {NotSended | DocumentCreated | DocumentError | Accepted | AcceptError}  - Статус кега
```

## Пример: LowAlcKegStatus

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="LowAlcKegStatus">
    <Keg markingData="{{markingData}}"/>
  </RK7CMD>
</RK7Query>
```
