# GetPrintedData

Печать пользовательского документа

Схемы: `schemas/qryGetPrintedData.xsd`, `schemas/resGetPrintedData.xsd`
Влияние: только чтение

## Практика

- Возвращает <PrintedDocuments>; если по заказу ничего не печаталось, список пустой. С пустым guid заказа сервер отвечает невнятной ошибкой про справочник причин внесения денег.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [GetPrintedData]
    <OperationType>? [refItem]  - Тип операции к которой привязан распечатанный документ
    <Station>? [refItem]  - Станция принтера, через которую печатался документ
    <Device>? [refItem]  - Логический принтер, на котором был распечатан документ
    <Document>? [refItem]  - Тип распечатанного документа
    <Order>? [orderElement]  - Заказ, к которому относится распечатанный документ
    @operationId: positiveInteger  - ID операции, ссылка на OperationLog.Sifr, по которой печатался документ
    @objUNI: positiveInteger  - UNI объекта, по которому печатался документ, для чека UNI чека
    @CMD: string = "GetPrintedData"
    @Timeout: nonNegativeInteger  - Таймаут ожидания готовности устройства, при 0 асинхронная отправка в очередь без ошибок
  <RK7Command>+ [GetPrintedData] (структура - см. выше)
  <RK7Command2>+ [GetPrintedData] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<PrintedDocuments>  - Список сохранённых распечатанных документов
  <PrintedDocument>* [uPrintedDocument]
    <Operation> [resOperationItem]  - операция, к которой привязан распечатанный документ
      <Station>? [resRefItem]  - Станция операции
      <OperationType> [resRefItem]  - Тип операции
      <Operator> [resEmployeeItem]  - Оператор - основной зарегистрированный работник
        (resRefItem: id | code | guid)
        <Role>? [resRefItem]  - Роль работника
      <Manager> [resEmployeeItem]  - Менеджер - работник, подтвердивший операцию (структура - см. выше)
      <Order>? [resOrderElement]  - заказ операции
        (orderElement: id | code | guid)
        @url: normalizedString  - URL заказа для code.ucs.ru
      <MenuItem>? [resRefItem]  - Элемент меню, заполнен для операций над блюдом
      <Maket>? [refItem]  - Представление печати документа для операции печати
      <Reason>? [resEmployeeItem]  - причина (внесения-выдачи, удаления,...) (структура - см. выше)
      @id: positiveInteger  - id операции (уникальный в рамках кассового сервера)
      @commonShiftNum: positiveInteger
      @dateTime: dateTime  - ДатаВремя операции в формате ISO
      @parameter: int  - целочисленный параметр операции
      @quantity: int  - Количество блюда в тысячных долях, если операция не относится к блюду, то 0 или отсутствует
      @orderSumBefore!: nonNegativeInteger  - Сумма заказа (в копейках) до выполнения операции
      @orderSumAfter!: nonNegativeInteger  - Сумма заказа (в копейках) после выполнения операции
    <Device> [resRefItem]  - Логический принтер, на котором был распечатан документ
    <Document> [resRefItem]  - Тип распечатанного документа
    <Maket>? [refItem]  - Представление печати документа
    <Data>?  - Данные для печати в формате нефискальной печати универсального драйвера
      <Unfiscal>* [uniUnfiscal]
        @Slip: boolean (по умолчанию "0")  - Печать на бланке
        @CutAfter: boolean (по умолчанию "0")  - Надо ли отрезать (завершить оформление документа) в конце
        @* - допускаются любые другие атрибуты
        (одно из - повторяется:)
          <TextBlock> [uniTextBlock]
            (текстовое содержимое: string)
            @FontNum: nonNegativeInteger (по умолчанию "0")
            @Bold: boolean (по умолчанию "0")
            @BigHeight: boolean (по умолчанию "0")
            @BigWidth: boolean (по умолчанию "0")
            @Inverted: boolean (по умолчанию "0")
            @AltLang: boolean (по умолчанию "0")
            @Tapes: string {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} (по умолчанию "8")
          <TextPart> [uniTextPart]
            @FontNum: nonNegativeInteger (по умолчанию "0")
            @Bold: boolean (по умолчанию "0")
            @BigHeight: boolean (по умолчанию "0")
            @BigWidth: boolean (по умолчанию "0")
            @Inverted: boolean (по умолчанию "0")
            @AltLang: boolean (по умолчанию "0")
            @Tapes: string {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} (по умолчанию "8")
            @Text!: normalizedString
          <TextLine> [uniTextLine]
            @FontNum: nonNegativeInteger (по умолчанию "0")
            @Bold: boolean (по умолчанию "0")
            @BigHeight: boolean (по умолчанию "0")
            @BigWidth: boolean (по умолчанию "0")
            @Inverted: boolean (по умолчанию "0")
            @AltLang: boolean (по умолчанию "0")
            @Tapes: string {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} (по умолчанию "8")
            @Text!: normalizedString
          <RawBlock> [uniRawBlock]
            (текстовое содержимое: string)
            @Encoding!: string {No | Base64}
          <BarCode> [uniBarCode]
            @Type: string {EAN-13 | Code-39} (по умолчанию "EAN-13")
            @TextPosition: string {No | Top | Bottom | Top&Bottom} (по умолчанию "No")
            @Value!: normalizedString
          <Beep> [uniBeep]
          <Drawer> [uniDrawer]
            @Number: string {0 | 1} (по умолчанию "0")
          <Logo> [uniLogo]
            @Number!: int
          <Pass> [uniPass]
            @Lines!: int
          <Wait> [uniWait]
            @MSecs!: int
    <JSONFiscalData>? [string]  - Данные фискального документа
    @objUNI: positiveInteger  - UNI объекта, по которому печатался документ, для чека UNI чека
    @printedTime: dateTime  - ДатаВремя окончания печати в формате ISO
```

## Пример: GetPrintedData

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetPrintedData">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
