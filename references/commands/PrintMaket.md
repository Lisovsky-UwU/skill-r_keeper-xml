# PrintMaket

Печать пользовательского документа

Схемы: `schemas/qryPrintMaket.xsd`, `schemas/resPrintMaket.xsd`
Влияние: изменяет данные

## Практика

- Document 1 "Чек" так печатать нельзя ("Unsupported document type"); копия чека - Document 27 с <ReceiptNum>, отчеты - другие элементы DOCUMENTS.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [PrintMaket]
    <Station> [refItem]  - Станция
    <Employee>? [refItem]  - Работник
    (одно из:)
      <ReceiptNum> [int]  - Номер чека (чтобы напечатать макет по конкретному чеку)
      <Order> [orderElement]  - Заказ
      <ReprintReceipt> [ReprintReceiptData]
        <Data>?  - Данные для печати в формате нефискальной печати универсального драйвера, данные можно взять из PrintedDocuments.Data
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
        <JSONFiscalData>? [string]  - Фискальные данные в формать JSON, данные можно взять из PrintedDocuments.JSONFiscalData
    (одно из:)
      <Maket> [refItem]  - Представление документа (отчет, пользовательский макет или макет копии чека)
      <Document> [refItem]  - Тип документа для печати (отчет, пользовательский макет или копия чека)
    @CMD: string = "PrintMaket"
    @LayoutFilters: normalizedString  - Фильтр макета вида поле=значение;поле=значение
    @DataSourceParams: normalizedString  - Параметры кубов вида поле=значение;поле=значение
    @Comment: normalizedString  - Комментарий для макета. Доступен для печати в макете (предустановленная переменная MaketComment) С версии 7.6.4.379, 7.6.5.187
  <RK7Command>+ [PrintMaket] (структура - см. выше)
  <RK7Command2>+ [PrintMaket] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger  - Код ошибки RK7
    @Component!: errorArea {Printer | Authorization terminal | PDS | Rights}  - Компонент, в котором была сгенерирована ошибка
@ServerVersion!: normalizedString  - Версия кассовой программы
@XmlVersion!: positiveInteger  - Версия xml протокола
@NetName: token  - Сетевое имя программы (с 7.5.3.260)
@CMD: token  - Исходная xml-команда
@Status!: string {Ok | No changes | Execution Started | Query Parse Error | Bad Query Parameters | Query Executing Error | Result Writing Error}  - Статус выполнения запроса
@RK7ErrorN: positiveInteger  - Код ошибки RK7
@ErrorText!: normalizedString  - Текст ошибки
@WorkTime!: nonNegativeInteger  - Время обработки запроса (в миллисекундах)
@DateTime!: dateTime  - Дата и время генерации ответного xml (xmlver>=39)
@Processed!: nonNegativeInteger  - Количество обработанных команд
```

## Пример: PrintMaket

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="PrintMaket" Comment="example">
    <Station id="{{stationId}}"/>
    <Employee id="{{managerId}}"/>
    <ReceiptNum>{{receiptNum}}</ReceiptNum>
    <Document id="27"/>
  </RK7CMD>
</RK7Query>
```
