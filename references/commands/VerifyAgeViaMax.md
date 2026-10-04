# VerifyAgeViaMax

Проверка возраста через MAX

Схемы: `schemas/qryVerifyAgeViaMax.xsd`, `schemas/resVerifyAgeViaMax.xsd`
Влияние: только чтение

## Практика

- sessionID берется из QR-кода, который покупатель открывает в мессенджере MAX; ответ - adult="1" / "0".
- Без настроенного адреса сервиса MAX - RK7ErrorN 7287 "Ошибка проверки возраста в MAX (EIdURIException): Protocol field is empty".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "VerifyAgeViaMax"
  @sessionID!: token  - id сессии из QR-кода в мессенджере MAX
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@adult!: boolean  - true - возраст подтверждён, false - не подтверждён
```

## Пример: VerifyAgeViaMax

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="VerifyAgeViaMax" sessionID="{{maxSessionId}}"/>
</RK7Query>
```
