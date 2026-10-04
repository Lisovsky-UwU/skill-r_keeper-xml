# GetCardInfo

[Касса, Кассовый сервер] Получить инфо о карте ПДС

Схемы: `schemas/qryGetCardInfo.xsd`, `schemas/resGetCardInfo.xsd`
Влияние: только чтение

## Практика

- Status="Ok" не означает, что карта существует: для несуществующего кода сервер может вернуть такой же CardInfo с пустым holder и нулевыми суммами. Существование карты надежно проверяет ApplyPersonalCard (для неизвестной - "Пользователь не найден!").
- Interface - логический интерфейс к FarCards из DEVICES; запрос идет в карточную систему и занимает сотни миллисекунд.
- Если сервер FarCards недоступен - "Ошибка отправки данных на <имя интерфейса>".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Interface> [refItem]  - Интерфейс, к которому нужно обратиться для получения инфо о карте
  <Order>? [orderElement]  - Заказ
  <EXTDATA>? [extData]  - Настраиваемые свойства (в типе описаны только изветсные атрибуты, но в farcards передаются вообще все атрибуты из этого тэга)
    @clientinfoinput: normalizedString
    @tag: normalizedString
  <Station>? [refItem]  - Станция, от имени которой выполняется запрос
  <ExtCardProperties>? [extCardProperties]  - Список запрашиваемых свойств
    <Property>+ [extCardProperty]
      @name!: normalizedString
      @value: normalizedString
  @CMD: string = "GetCardInfo"
  @cardCode!: normalizedString  - Код карты
  @chMode: string {NotCheck | Sale | OrderEditing | OrderCalc} (по умолчанию "OrderEditing")  - chMode, который будет передаваться в farcards
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<CardInfo>
  <Discount> [resRefItem]  - Скидка
  <BonusType> [resRefItem]  - Тип бонуса
  <Defaulter> [resRefItem]  - Неплательщик
  <DopInfo> [normalizedString]  - Доп инфо по карте
  <Message> [normalizedString]  - Сообщение для экрана
  <PrintMessage> [normalizedString]  - Сообщение для печати
  <Image> [normalizedString]  - Фото клиента, в base64
  <OutBuf>  - Ответный буфер от сервера карт/фаркадс
    (текстовое содержимое: normalizedString)
    @kind: integer  - Тип данных в буфере
  <Currency>+  - Валюта
    (resRefItem: id | code | guid)
    @subacc: nonNegativeInteger  - Номер субсчета
    @maxAmount: nonNegativeInteger  - Максимальная сумма (в копейках)
    @amount: nonNegativeInteger  - Остаток (в копейках)
  <ExtCardProperties>? [extCardProperties]  - Список возвращенных расширенных свойств
    <Property>+ [extCardProperty]
      @name!: normalizedString
      @value: normalizedString
  @cardCode: normalizedString  - Код карты
  @holder: normalizedString  - Владелец карты
  @maxAmount: nonNegativeInteger  - Максимальная сумма (в копейках)
  @amount: nonNegativeInteger  - Остаток (в копейках)
  @maxDisc: nonNegativeInteger  - Максимальная сумма скидки (в копейках)
  @InternalCardCode: integer  - Числовой код карты
  @ManagerConfirmation: boolean  - Флаг - требуется менеджерское подтверждение
```

## Пример: GetCardInfo

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetCardInfo" cardCode="{{cardCode}}">
    <Interface id="{{pdsInterfaceId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
