# LowAlcKegList

Получить список поставленных на кран кег

Схемы: `schemas/qryLowAlcKegList.xsd`, `schemas/resLowAlcKegList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD!: string = "LowAlcKegList"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<KegsList>  - Список поставленных на кран кег
  <Keg>* [uKegItem]
    <SendInfo>  - Статус отправки в сервис DocsExchange / Честный знак
      @status!: HonestSignSendStatus {NotSended | DocumentCreated | DocumentError | Accepted | AcceptError}  - Статус отправки кега
      @hsDocumentGuid: token  - Гуид документа постановки на кран, который отправлен в Честный Знак
      @errorText: normalizedString  - Текст возникшей ошибки
      @errorCode: integer  - Код возникшей ошибки
      @errorSource: normalizedString  - Сервис, который вернул ошибку
    <Author> [refItem]  - Сотрудник, выполнивший постановку на кран
    <Station>? [refItem]  - Станция, на которой была выполнена постановка на кран
    <Tap>? [refItem]  - Кран, на который поставлен кег. С версии 7.26.02
    @markingData!: base64Binary  - Марка кега в формате base64
    @gtin!: normalizedString  - GTIN кега
    @name!: normalizedString  - Наименование товара
    @startDateTime: dateTime  - Дата и время постановки кега на кран
    @bottleVolume!: boolean  - Объем кега в миллилитрах
    @restVolume!: boolean  - Остаток в кеге, в миллилитрах
    @expireDate!: date  - Дата окончания срока годности кега
    @finished!: boolean  - Признак того, что кег отключен от крана. True - кег отключен.
    @finishTime: dateTime  - Дата и время отключения кега от крана
    @saleBeforeDate!: date  - Дата, до которой кег должен быть реализован
```

## Пример: LowAlcKegList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="LowAlcKegList"/>
</RK7Query>
```
