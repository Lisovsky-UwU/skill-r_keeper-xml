# ETPC

xml-query to ETPC

Схемы: `schemas/qryETPC.xsd`, `schemas/resETPC.xsd`

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Row>+
    @index!: normalizedString  - Unique row identifier
    @itemCode!: normalizedString  - Code of the item
    @itemName: normalizedString  - Name of the item
    @groupCode: normalizedString  - Group code
    @ignore: boolean  - Exclude this item from discount calculation, the line won't have any discounts applied
    @pricePerUnitDto!: nonNegativeInteger  - Price of the unit in copeck (price * 100)
    @quantity!: nonNegativeInteger  - Quantity (Quantity * 1000)
    @cashAmountDto!: nonNegativeInteger  - Price of this item line in copeck (amount*100)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<RK7CMD>
  <Row>+
    @index!: normalizedString  - Index (the same as provided in the request)
    @itemCode!: normalizedString  - Item code (as provided in the request)
    @itemName: normalizedString  - Name of the item
    @groupCode: normalizedString  - Group code (as provided in the request)
    @ignore: boolean  - Exclude this item from discount calculation, the line won't have any discounts applied
    @pricePerUnitDto!: nonNegativeInteger  - Calculated price of the unit (price * 100)
    @quantity!: nonNegativeInteger  - Quantity (Quantity * 1000)
    @cashAmountDto!: nonNegativeInteger  - Cash amount for this item of the cart in copeck (amount*100)
    @discountDto!: integer  - Discount, applied on this item (discount amount *100)
    @points: nonNegativeInteger  - How much COUPON and/or MONETARY points should buyer receive for this item (points*100)
```
