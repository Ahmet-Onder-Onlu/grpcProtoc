# gRPC Uygulama Geliştirme Ödevi Teslim Raporu

## 👤 Öğrenci Bilgileri
- **Ad Soyad**: Ahmet Önder ÖNLÜ
- **Öğrenci Numarası**: 170422030
- **Kullanılan Programlama Dili**: Python

---

## 📦 GitHub Repo

Lütfen projenizin tamamını bir GitHub reposuna yükleyiniz. `.proto` dosyasından üretilecek stub kodlar hariç!

### 🔗 GitHub Repo Linki
[GitHub projenizin linkini buraya yazınız]

---

## 📄 .proto Dosyası

- `.proto` dosyasının adı(ları):
- Tanımlanan servisler ve metod sayısı:
- Enum kullanımınız var mı? Hangi mesajda?
- Dili (Türkçe/İngilizce) nasıl kullandınız?

---

## 🧪 grpcurl Test Dokümantasyonu

Aşağıdaki bilgiler `grpcurl-tests.md` adlı ayrı bir markdown dosyasında detaylı olarak yer almalıdır:

- Her metot için kullanılan `grpcurl` komutu
- Dönen yanıtların ekran görüntüleri
- Hatalı durum senaryoları (404, boş yanıt vb.)

> Bu dosya, değerlendirmenin önemli bir parçasıdır.

---

## 🛠️ Derleme ve Çalıştırma Adımları

Projeyi `.proto` dosyasından derleyip sunucu/istemci uygulamasını çalıştırmak için gereken komutlar:

```bash
# Örnek:
protoc --go_out=. --go-grpc_out=. university.proto
go run server/main.go
go run client/main.go
```

---

## ⚠️ Kontrol Listesi

- [ ] Stub dosyaları GitHub reposuna eklenmedi  
- [ ] grpcurl komutları test belgesinde yer alıyor  
- [ ] Ekran görüntüleri test belgesine eklendi  
- [ ] Tüm servisler çalışır durumda  
- [ ] README.md içinde yeterli açıklama var  

---

## 📌 Ek Açıklamalar

Varsa ek notlarınızı veya yaşadığınız teknik zorlukları buraya yazabilirsiniz.

---

Teşekkürler!