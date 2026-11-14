---
id: apk-exported-components
soha: apk
xavf: yuqori
lesson: "Keep Android components exported=false unless required; disable allowBackup and cleartext traffic; validate deep link input."
agent: attacker-apk
---

# Himoyasiz ochiq komponentlar va xavfli manifest sozlamalari

## Nima qidiriladi
`AndroidManifest.xml` ichida:
- `android:exported="true"` va `permission` yo'q bo'lgan activity, service, receiver, provider.
- `android:debuggable="true"`, `android:allowBackup="true"`, `android:usesCleartextTraffic="true"`.
- Deep link (`intent-filter` + `data`) orqali kelgan qiymatni tekshirmasdan ishlatish.

## Nega xavfli
Telefondagi boshqa ilova ochiq komponentni to'g'ridan-to'g'ri chaqirib, login ekranini chetlab o'tishi yoki ichki ma'lumotni olishi mumkin. Backup orqali ilova ma'lumoti ko'chirib olinadi, shifrsiz trafik esa tarmoqda o'qiladi.

## Yomon misol
```xml
<activity android:name=".AdminActivity" android:exported="true" />
<application android:allowBackup="true" android:usesCleartextTraffic="true">
```

## Yaxshi misol
```xml
<activity android:name=".AdminActivity" android:exported="false" />
<application android:allowBackup="false" android:usesCleartextTraffic="false">
```

## Tuzatish
Tashqaridan chaqirilishi shart bo'lmagan komponentlarni `exported="false"` qil. Ochiq qolishi kerak bo'lganlarida kirish parametrlarini tekshir va sessiyani talab qil.

Claude Code uchun prompt: "AndroidManifest'dagi exported komponentlarni ko'rib chiq, keraksizlarini yop, allowBackup va cleartext trafikni o'chir, deep link parametrlarini tekshiruvdan o'tkaz."
