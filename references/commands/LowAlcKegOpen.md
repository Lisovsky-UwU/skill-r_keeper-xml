# LowAlcKegOpen

Постановка кега со слабоалкогольным напитком на кран

Схемы: `schemas/qryLowAlcKegOpen.xsd`, `schemas/resLowAlcKegOpen.xsd`
Влияние: изменяет данные

## Практика

- Нужно свойство ресторана "Адрес службы для отправки документов в ЧЗ" - без него ошибка с этим текстом.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Keg>  - Кег
    @markingData!: base64Binary  - Марка кега в base64
    @bottleVolume!: positiveInteger  - Объем кега в миллилитрах
  <Author>? [refItem]  - Автор операции
  <Station> [refItem]  - Станция
  <Tap>? [refItem]  - Кран розлива. С версии 7.26.02
  @CMD: string = "LowAlcKegOpen"
  @resend: boolean
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

## Пример: LowAlcKegOpen

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="LowAlcKegOpen">
    <Keg markingData="{{markingData}}" bottleVolume="30000"/>
    <Author id="{{managerId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
