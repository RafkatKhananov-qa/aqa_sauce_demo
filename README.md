# AQA Sauce Demo

UI-автотесты для [saucedemo.com](https://www.saucedemo.com) на базе Playwright + Pytest.

---

## Стек

| Инструмент | Версия |
|---|---|
| Python | 3.11 |
| Playwright | 1.58.0 |
| Pytest | 9.0.3 |
| pytest-xdist | 3.8.0 |
| Allure | 2.15.3 |

---

## Структура проекта

```
aqa_sauce_demo/
├── config/                  # Константы и тестовые данные
│   ├── base.py              # URL-адреса, таймауты
│   ├── users.py             # Учётные данные, сообщения об ошибках
│   ├── goods.py             # Данные товаров
│   └── mobile.py            # Параметры устройств и минимальные размеры
├── pages/                   # Page Object Model
│   ├── mixins/              # Миксины для BasePage
│   │   ├── accessibility_mixin.py   # WCAG-контраст, мёртвые зоны
│   │   ├── mobile_mixin.py          # DPR, UA, локаль, viewport
│   │   ├── performance_mixin.py     # FCP, CLS, память, 3G
│   │   └── storage_mixin.py         # Куки, localStorage
│   ├── base_page.py         # Базовый класс (навигация, UI, скриншоты)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout/
│       ├── checkout_step_one_page.py
│       ├── checkout_step_two_page.py
│       └── checkout_complete_page.py
├── tests/
│   ├── web/                 # Десктопные тесты
│   │   ├── test_auth.py
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   ├── test_checkout.py
│   │   ├── test_e2e.py
│   │   ├── test_cross_browser.py
│   │   └── test_performance.py
│   └── mobile/              # Мобильные тесты
│       ├── test_mobile_e2e.py
│       ├── test_mobile_responsive.py
│       ├── test_mobile_touch.py
│       ├── test_mobile_ux.py
│       ├── test_mobile_perf.py
│       ├── test_cross_device.py
│       ├── test_navigation_ui.py
│       └── test_l42_mobile.py
├── utils/
│   ├── logger.py
│   ├── helpers.py
│   └── artifacts.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

## Установка

```bash
git clone <repo-url>
cd aqa_sauce_demo

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install --with-deps
```

---

## Запуск тестов

### Все тесты
```bash
pytest tests/
```

### Только веб
```bash
pytest tests/web/
```

### Только мобильные
```bash
pytest tests/mobile/
```

### Параллельно (3 воркера)
```bash
pytest tests/ -m parallel -n 3
```

### С Allure-отчётом
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Конкретный файл
```bash
pytest tests/web/test_e2e.py -v
```

---

## Тестовые пользователи

| Пользователь | Поведение |
|---|---|
| `standard_user` | Стандартный сценарий |
| `problem_user` | Некорректное отображение товаров |
| `performance_glitch_user` | Замедленная загрузка страниц |
| `error_user` | Ошибки при добавлении в корзину |
| `visual_user` | Визуальные дефекты UI |

Пароль для всех: `secret_sauce`

---

## Поддерживаемые устройства (мобильные тесты)

| Устройство | Разрешение |
|---|---|
| iPhone 14 Pro | 393×660 |
| Pixel 7 | 412×839 |
| iPad Mini | 768×1024 |
| iPhone 8 Landscape | 667×375 |

---

## CI/CD

GitHub Actions запускает тесты:
- при пуше в `master` и `develop`
- при создании pull request в `master` и `develop`
- вручную через `workflow_dispatch`
- автоматически каждый день в 08:00 UTC

После прогона:
- Allure-отчёт публикуется на GitHub Pages
- В Telegram-канал приходит уведомление о результате
