## Initial Prompt

@engine.py scriptini aşağıdaki adımları göz önünde bulundurarak yaz: 

İçerisinde bir fonksiyon olacak, "download_single_video_from_youtube" olarak isimlendir.
Bu fonksiyon, @yt-dlp kütüphanesini kullanarak video id'si girilen Youtube videosunu download edecek. Bu scripti yazarken @example-download.py scriptini örnek alabilirsin. Özellikle de cookie kullanarak download etmek için. @backend-rules.mdc ye sadık kalarak bu fonksiyonu oluşturacaksın. Bu script çalışırken, @logs.mdc ye sadık kalarak ekrana log yazdırmalı. Ayrıca try-except yapılarıyla videonun indirilip indirilmediğini kontrol etmeli ve gelen hata mesajlarını ekrana yazdırmalısın. 

İkinci script, @copy_to_bucket.py içerisinde olmalı ve "copy_to_gcp" isminde bir fonksiyon içermeli. Bu fonksiyon, indirilen videoyu GCP CLI toollarını kullanarak bucketa kopyalayacak, kopyaladığına emin olduktan sonra ise lokal dizinden silecek. Detaylar için @gcp-rules.mdc u referans al. try-except yapılarıyla sürecin sağlıklı işlediğine emin ol.

Bunların ardından bir "main.py" dosyası oluştur. @engine.py ve @copy_to_bucket.py scriptlerini import et. 

Bir dizi içerisinde "ids.txt" dosyasını satır satır oku ve her bir satırdaki video id'sini listeye eleman olarak ekle. Ardından bu listenin elemanlarını teker teker bir for loopunda download_single_video_from_youtube ve copy_to_gcp scriptlerini çalıştır. 

Bu prosesler sorunsuz tamamlanırsa "downloaded.txt" adında yeni bir txt file oluştur ve download edilen videoların log bilgisini buraya yaz,@logs.mdc kurallarına sadık kal. Ardından download edilen videoların id'sini "ids.txt" içerisinden sil.

## Öncesinde Yapmanız Gerekenler

Cursor'un ayarlarında yt-dlp kütüphanesinin orijinal dokümanını eklemelisiniz, çünkü direkt olarak bu dokümanı refere ederek kod yazdırıyor olacağız: https://github.com/yt-dlp/yt-dlp

"@" sembolü ile refere ettiğimiz Python scriptlerini önceden oluşturmalısınız(engine.py ve copy_to_bucket.py)

Toollar: Chat için Deepseek-R1, Agent için Claude Sonnet 3.7