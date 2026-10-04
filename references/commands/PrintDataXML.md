# PrintDataXML

Печать пользовательского документа

Схемы: `schemas/qryPrintDataXML.xsd` (схемы ответа нет)
Влияние: изменяет данные

## Практика

- Содержимое <Unfiscal> - разметка универсального драйвера из unifr.xsd (TextLine, TextBlock, BarCode, Logo, Pass, Beep...). Сервер не проверяет ее строго: на неизвестный тег тоже отвечает Ok.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [PrintDataXML]
    <Purpose> [refItem]  - Назначение печати, должно быть с галочкой "на ресторан" либо надо задать станцию
    <Station> [refItem]  - Станция принтера, если назначение печати не "на ресторан", то принтер будет определён через назначение для этой станции. Физически принтер может быть на другой станции"
    <Unfiscal> [uniUnfiscal]  - Данные для печати в формате нефискальной печати универсального драйвера
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
    @CMD: string = "PrintDataXML"
    @Timeout: nonNegativeInteger  - Таймаут ожидания готовности устройства, при 0 асинхронная отправка в очередь без ошибок
  <RK7Command>+ [PrintDataXML] (структура - см. выше)
  <RK7Command2>+ [PrintDataXML] (структура - см. выше)
```

## Пример: PrintDataXML

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="PrintDataXML" Timeout="0">
    <Purpose id="{{printPurposeId}}"/>
    <Station id="{{stationId}}"/>
    <Unfiscal>
      <TextLine Text="Тестовая печать"/>
    </Unfiscal>
  </RK7CMD>
</RK7Query>
```
