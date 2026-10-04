# GotoOrder

[Касса] Открыть на кассе заказ на редактирование

Схемы: `schemas/qryGotoOrder.xsd`, `schemas/resGotoOrder.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- По наблюдениям интеграторов, команду убрали из r_keeper в версии 7.5.8; сервер 7.26 ее не объявляет в GetFunctions и отвечает "Unknown command".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  @closeFormURL: normalizedString (по умолчанию "")  - URL по которому нужно перейти в браузере после того, как форма с заказом будет закрыта. Используется только в том случае, если запрос выполняется в тот момент, когда на кассе открыта форма с браузером
  @CMD: string = "GotoOrder"
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

## Пример: GotoOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GotoOrder">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
