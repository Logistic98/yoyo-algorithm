## yoyo-algorithm

项目简介：通用开源算法的Flask封装集成

接口文档：可以用Flask-Doc来生成，但是我懒的写（逃~），test-code是代码的请求示例，每个接口都有，参考这个就行。

项目部署：直接上传docker-deploy到服务器即可，里面有部署脚本，可以单个部署，也可以批量部署。

### 1. FastTextRank

项目地址：[https://github.com/ArtistScript/FastTextRank](https://github.com/ArtistScript/FastTextRank)

项目描述：从中文文本中提取摘要及关键词，并对算法时间复杂度进行了修改，计算图最大权节点的时间复杂度由o（n^2）降低到了o（n）。在有限的测试文本上（10篇文章），其运行速度相比于textrank4zh这个包快了8倍。

### 2. Paddle

#### 2.1 PaddleOCR

项目地址：[https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

项目描述：百度飞桨开源的图片OCR识别算法，模型会在初次执行时自动下载。这是它的官方使用教程：[PaddleOCR使用教程](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_ch/quickstart.md)

#### 2.2 PaddleNLP

项目地址：[https://github.com/PaddlePaddle/PaddleNLP](https://github.com/PaddlePaddle/PaddleNLP)

项目描述：百度飞桨开源的自然语言处理开发库，模型会在初次执行时自动下载。这是它的官方使用教程：[PaddleNLP官方教程](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md)

### 3. py-googletrans

项目地址：[https://github.com/ssut/py-googletrans](https://github.com/ssut/py-googletrans)

项目描述：py-googletrans 是一个免费且不受限制的Python库，它实现了破解 Google翻译，使用这个库时需要挂代理。这是它的API文档：[py-googletrans API文档](https://py-googletrans.readthedocs.io/en/latest/)

### 4. gTTS

项目地址：[https://github.com/pndurette/gTTS](https://github.com/pndurette/gTTS)

项目描述：谷歌开源的用于文本转语音的 Python 库和 CLI 工具。可用于合成语音，使用这个库时需要挂代理。

### 5. GeoIP2

可以借助GeoIP2-python和GeoLite.mmdb两个开源项目来获取IP的地理位置信息。

GeoIP2-python：[https://github.com/maxmind/GeoIP2-python](https://github.com/maxmind/GeoIP2-python)（GeoIP2 web 服务客户端和数据库阅读器的 Python 代码）

GeoLite.mmdb：[https://github.com/P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb)（MaxMind 的 GeoIP2 GeoLite2 国家、城市和 ASN 数据库）