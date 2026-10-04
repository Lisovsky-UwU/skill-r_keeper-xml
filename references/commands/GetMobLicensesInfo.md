# GetMobLicensesInfo

[Касса,Кассовый сервер] Получение номера запроса по инстансу

Схемы: `schemas/qryGetMobLicensesInfo.xsd`, `schemas/resGetMobLicensesInfo.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetMobLicensesInfo"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<MobLicensesInfo> [MobLicensesInfoItem]  - Информация о лицензиях и инстансах для мобильного официанта
  <MobLicenseInfo>+ [ResMobLicenseKindInfo]
    <Instances>
      <Instance>+ [ResMobLicenseInstanceItem]
        @guid: guidString
        @name: normalizedString  - имя инстанса
        @slot: nonNegativeInteger  - номер слота лицензии
        @dateTime: dateTime  - ДатаВремя создания инстанса
    @kind: MobileLicenseKind {waiter | administrator}  - тип лицензии (официант/админ)
    @available: nonNegativeInteger  - максимальное количество инстансов
```

## Пример: GetMobLicensesInfo

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetMobLicensesInfo"/>
</RK7Query>
```
