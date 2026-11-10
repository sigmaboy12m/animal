# Animal Rush Backend — نسخهٔ پایتون برای Railway

این سرور همان API سرور نود (`backend.mjs`) را با زبان **پایتون** و **بدون هیچ وابستگی**
(فقط کتابخانهٔ استاندارد پایتون) پیاده‌سازی می‌کند. برای اجرا روی Railway آماده است.

## فایل‌ها

| فایل | توضیح |
|---|---|
| `railway_server.py` | خود سرور (تمام روت‌ها) |
| `Procfile` | دستور اجرا برای Railway |
| `railway.json` | تنظیمات دیپلوی (Nixpacks) |
| `nixpacks.toml` | دستور اجرا جایگزین |
| `requirements.txt` | خالی (بدون وابستگی) |
| `runtime.txt` | نسخهٔ پایتون (3.12) |

## اجرای محلی (تست)

```
python railway_server.py
```
پیش‌فرض روی پورت `8899` بالا می‌آید. تست سلامت: `http://127.0.0.1:8899/health`

## دیپلوی روی Railway

روش ۱ — از روی گیت‌هاب:
1. این پوشه را در یک ریپازیتوری گیت‌هاب بگذارید.
2. در Railway → New Project → Deploy from GitHub repo.
3. Railway خودش پایتون را تشخیص می‌دهد و `railway_server.py` را اجرا می‌کند.

روش ۲ — با CLI:
```
npm i -g @railway/cli
railway login
railway init
railway up
```

## متغیرهای محیطی

- `PORT` — Railway خودش ست می‌کند (سرور از آن استفاده می‌کند).
- `DATA_DIR` — محل ذخیرهٔ `state.json`. اگر Volume دارید، آن را به `/data` ست کنید
  و یک Volume روی `/data` وصل کنید تا داده‌ها با ری‌استارت از دست نروند.

## URL نهایی

بعد از دیپلوی، Railway یک دامنه مثل `https://xxxx.up.railway.app` می‌دهد.
این آدرس را در کلاینت بازی (در `Autoload/Constants.gd`، متغیر `BACKEND_URL`) بگذارید
و از نو بیلد بگیرید. (یا با آرگومان `backend=https://xxxx.up.railway.app` اجرا کنید.)

## سلامت

```
GET /health   →   {"ok": true, "accounts": N, ...}
```
