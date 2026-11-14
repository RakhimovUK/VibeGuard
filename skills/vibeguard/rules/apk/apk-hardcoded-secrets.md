---
id: apk-hardcoded-secrets
soha: apk
xavf: kritik
lesson: "Keep secret keys on the server, never inside the app bundle; the app talks only to our backend."
agent: attacker-apk
---

# Ilova ichida sirlar

## Nima qidiriladi
- `strings.xml`, `BuildConfig`, `gradle.properties`, `local.properties`, Kotlin/Java/Dart/JS kodida kalit, token, parol.
- `google-services.json` yoki Supabase sozlamasida `service_role` yoki admin kaliti.
- Imzolash kaliti (`.jks`, `.keystore`) va paroli repoda.

## Nega xavfli
APKni har kim ochib o'qiy oladi. Ilova ichidagi sir aslida ommaviy: u bilan serveringizga ilovadan tashqarida, cheklovsiz murojaat qilish mumkin.

## Yomon misol
```kotlin
const val API_SECRET = "sk-...a4f2"
```

## Yaxshi misol
```kotlin
// Ilova faqat foydalanuvchi sessiya tokenini biladi.
// Maxfiy kalit serverda turadi, ilova serverga murojaat qiladi.
api.post("/generate", body, headers = mapOf("Authorization" to "Bearer $sessionToken"))
```

## Tuzatish
Maxfiy kalitlarni serverga ko'chir, ilova faqat o'z serveringiz orqali ishlasin. Ilovada qolishi shart bo'lgan kalitlar (ommaviy/anon) huquqi minimal bo'lsin. Oshkor bo'lgan kalitni almashtir.

Claude Code uchun prompt: "Ilova kodidagi maxfiy kalitlarni top (qiymatini chiqarma), ular ishlatiladigan chaqiruvlarni backend orqali o'tadigan qil va ilovada faqat minimal huquqli kalit qolsin."
