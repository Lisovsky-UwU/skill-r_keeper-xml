# XSD-схемы r_keeper

Схемы XML-интерфейса r_keeper 7 от UCS - набор для версии 7.26 (файлы 2023-2026 годов), без
изменений. Права на схемы принадлежат UCS, лицензия Apache этого репозитория на них не
распространяется (см. `NOTICE`).

```
schemas/
  common.xsd, messages.xsd, unifr.xsd, ...   общие типы
  qry<Команда>.xsd, res<Команда>.xsd         запрос и ответ каждой команды
  Delivery/                                  доставка
  Hidden/                                    недокументированные команды
```

Известные огрехи набора (оставлены как есть, генератор их переживает):
- `qryOpenLowAlcKeg.xsd` - невалидный XML; это устаревший дубль `qryLowAlcKegOpen.xsd`.
- `qryAddBatchOfGoods.xsd` - атрибуты `Batch` записаны без `complexType`.
- `qryFindReceiptsForReturn.xsd` объявляет UTF-8, но сохранен в windows-1251.
- Ответ на `FarCardsAnyInfoXML` лежит в `resFarCardsAnyInfoXml.xsd` (другой регистр).
- `ITV_TITLE.xsd` - не команда XML-интерфейса; судя по полям (работник, станция, позиции чека),
  это формат титров для видеонаблюдения (интерфейсы ITV / UCS Видео).

## Обновление

Положите новый набор вместо этого, с той же структурой, и выполните из корня скилла:

```bash
python scripts/xsd_to_reference.py schemas .
python scripts/check.py
```

Генератор перепишет `references/commands/` и `references/commands.md`. Ручные заметки и примеры
он берет из `references/command_notes.json`, так что они не потеряются.
