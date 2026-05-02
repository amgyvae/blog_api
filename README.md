
# README.md 

```md
# Blog API — Homework 1

REST API для блога на **Django + DRF + JWT + Redis**.

## Возможности

- Кастомная модель пользователя (email вместо username)
- JWT-аутентификация
- CRUD постов
- Комментарии к постам
- Права доступа владельца
- Redis:
  - кеш списка постов
  - rate-limit
  - pub/sub событий комментариев
- Логирование
- Разделённые settings (local / prod)
- Разделённые requirements

---

## Архитектура проекта
