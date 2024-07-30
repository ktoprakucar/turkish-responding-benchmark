# turkish-responding-benchmark

Bu repository, blog yazımda paylaştığım örneklerin kaynak kodlarını içermektedir.
- [notebooks](notebooks) klasöründeki [rephrasing.ipynb](notebooks/rephrasing.ipynb) dosyasını çalıştırarak modellerin talimatlara ne kadar uyup nasıl Türkçe cümleler oluşturduğunu inceleyebilirsiniz.
- [src](src) klasörünün altında ise [application.py](application.py) ile çalıştırabileceğiniz basit bir sohbet uygulamasına göz atabilirsiniz.

## Kurulum

Tüm uygulamalar `Python 3.12` ile geliştirilmiştir.

Paketleri yüklemeden önce uygulamalar için sanal bir Python ortamı oluşturmanızı tavsiye ederim.

```commandline
mkvirtualenv turkish-responding-benchmark
```

Sonrasında, gerekli olan paketleri indirmeniz gerekmektedir.

```commandline
pip install -r requirements.txt
```

Kodlarda yerel ayarları bulundurmamak için modellerin konumlarını harici bir yapılandırma dosyasında tutmak istedim. Bu nedenle, testte kullanmak istediğiniz modellerin konumunu [properties](properties) klasörünün altında `local.ini` olarak oluşturmanız gerekiyor. Referans olarak [test.ini](properties/test.ini) dosyasına göz atabilirsiniz.

Örneğin Qwen2-7B quantized modelini Hugging Face [reposundan](https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF) indirip, indirdiğiniz konumu `local.ini` dosyasında şu şekilde belirtebilirsiniz:

```ini
[REPHRASING_MODEL]
model_directory = ../../models/qwen2-7b-instruct-q8_0.gguf

[CHAT_MODEL]
model_directory = ../../models/qwen2-7b-instruct-q8_0.gguf
```

### Rephrasing

Gerekli paketleri kurduktan sonra, [notebooks](notebooks) klasörüne gelip, jupyter-notebook platformuna girmeniz gerekiyor.

```commandline
jupyter notebook
```

Sonrasında kodu baştan sona çalıştırıp modellerin performanslarını gözlemleyebilirsiniz.

P.S. Blog yazısında da bahsettiğim gibi, Llama modeli farklı spesifik token'lar kullandığı için, daha iyi performans için uyarlanan prompt'u kullanmanız gerekiyor.

Prompt'un farklı olan kısmı:
```commandline
<|begin_of_text|>user
{question}<|eot_id|>"
<|begin_of_text|>assistant
```

### Sohbet

Bu kısımda, uygulamayı başlatmak için streamlit'i de çalıştırmanız gerekiyor.

```commandline
streamlit run application.py
```

Makinenizdeki donanıma bağlı olarak, soruların cevaplarını almaya başlayabilirsiniz!

Streamlit ile ilgili tüm detaylara [application.py](application.py) dosyasından, onun dışındaki tüm servislere ise [service](src/service) klasörünün altından ulaşabilirsiniz.

Rephrasing uygulamasında da bahsettiğim gibi, LLama modellerini kullanırken [prompt](src/utils/constant.py)'ta ve mesajların birleştirildiği [kısımda](src/service/chat_service.py) (_combine_messages) özel token'ları değiştirmeniz gerekiyor.

```
<|im_start|> to <|begin_of_text|>
<|im_end|> to <|eot_id|>
```

### Pre-commit Hooks

Kodun standartlarını ve okunabilirliğini sağlamak için hem Jupyter hem de Python dosyalarını destekleyen pre-commit hookları da eklemek istedim.

Bunun için gerekli paketleri yüklemeniz gerekmektedir.

```commandline
pip install -r requirements_dev.txt
```

Sonrasında, herhangi bir commit oluşturduğunuzda aktif olarak tarama yapacak olan hookları aktive etmeniz için pre-commit paketini çalıştırmamız gerekiyor.

```commandline
pre-commit install
```

[.pre-commit-config.yaml](.pre-commit-config.yaml) dosyasında gerekli olan tüm ayarlara ulaşabilirsiniz.

Bonus:
Commit öncesinde de tüm taramaları yapmak için aşağıdaki komutu çalıştırabilirsiniz:

```commandline
pre-commit run --all-files
```

İyi Eğlenceler!