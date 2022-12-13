# paperSearcher
一个搜索网络安全领域顶会论文的小工具
![img.png](img.png)
使用python3编写，数据库内容将不定期更新，目前收录了2016~2021，以及部分2022的文章，包含：

- Computer and Communications Security (CCS)
- IEEE Symposium on Security and Privacy (S&P)
  - International Security Protocols Workshop (SPW)（这个不是CCF A，是SP的Workshop）
- USENIX Security Symposium (USS)
  - CSET @ USENIX Security Symposium (CEST)（非CCF A, USENIX Workshop）
  - FOCI @ USENIX Security Symposium (FOCI)（非CCF A, USENIX Workshop）
  - SOUPS @ USENIX Security Symposium (SOUPS)（CCF C？, USENIX Workshop）
  - WOOT @ USENIX Security Symposium (WOOT)（非CCF A, USENIX Workshop）
- IEEE Transactions on Dependable and Secure Computing (TDSC)
- IEEE Transactions on Information Forensics and Security (TIFS)
- Network and Distributed System Security Symposium (NDSS) （CCF B，但是质量比较高，也收录了）
- Annual Computer Security Applications Conference (ACSAC)（CCF B，但是质量比较高，也收录了）
- ACM Computing Surveys (CSUR)（CCF None，但是质量比较高，也收录了）
- European Symposium on Research in Computer Security (ESORICS) (CCF B)
- IEEE Computer Security Foundations Symposium (CSFW) (CCF B)
- Dependable Systems and Networks (DSN) (CCF B)
- Computers & Security (COMPSEC) (CCF B)
- International Symposium on Recent Advances in Intrusion Detection (RAID) (CCF B)
- Journal of Computer Security (JCS) (CCF B)
- ACM Transactions on Privacy and Security (CCF 列表显示为 TOPS， DBLP显示为 TISSEC) (CCF B)
- IEEE International Symposium on Reliable Distributed Systems (SRDS) (CCF B)
- IEEE Communications Surveys and Tutorials (COMSUR) (CCF None, 但是质量比较高，也收录了)


使用Flask作为基础框架，写的比较简单，主要为实现功能，代码很丑（一下午撸完前后端，凑合看）

有些功能应该放后端做比较好，当时写的时候脑子有点抽，后面有时间再慢慢改吧

## 安装方法

安装完Python3之后，将本仓库clone到本地，使用pip安装flask即可。

```bash
git clone https://github.com/mactavishmeng/paperSearcher.git
cd paperSearcher
pip3 install -r requirements.txt
python3 website.py
```

## 使用方法

默认开放在`http://127.0.0.1:5000`，可以修改webpage.py中的最后一行，来指定监听的IP和端口：

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
```

建议仅在本地使用，不要开在0.0.0.0（因为查询接口可能有SQL注入，写的匆忙……没有做太多防护）

查询逻辑非常简单，通过 `+` 与 `|` 分割关键字。

比如：

- 关键字为`blockchain+security`，查询结果则在 title 和 abstract 中搜索同时包含`blockchain`和`security`的文章。
- 关键字为`security | internet of things | evaluation`，表示只要任意出现 `security`, `internet of things`, `evaluation`这三个关键词的任意一个，就会返回该条记录。

## 更新记录

2021.06.25

- 更新数据库：新增 ACM Computing Surveys Volume 54, Number 3, June 2021（共23篇）；
- 更新数据库：新增"BIB"列，用于存储`.bib`格式的引用文件；
- 更新UI界面，新增"Cite"按钮，用于下载`.bib`格式的引用文件；
- 更新UI界面，新增来源缩写的全名显示，将鼠标悬停在缩写标签上即可。

2021.09.06

- 更新数据库：新增 IEEE Communications Surveys and Tutorials, 2016 ~ 2021（共636篇）
- 更新数据库：新增 USENIX Security Symposium'21（共247篇）
- 更新UI界面：新增会议标签`comsur`（IEEE Communications Surveys and Tutorials）

2021.10.26
- 更新数据库：新增 IEEE Symposium on Security and Privacy, 2021（共115篇）
- 更新数据库：新增 IEEE Transactions on Dependable and Secure Computing, 2021, July ~ October（共70篇）
- 更新数据库：新增 ACM Computing Surveys, 2021, July ~ September（共87篇）
- 更新数据库：新增 IEEE Transactions on Information Forensics and Security, 2021（共92篇）

2021.12.13
- 更新数据库：新增 Annual Computer Security Applications Conference, 2021（共81篇）
- 更新数据库：新增 Computer and Communications Security, 2021（共226篇）
- 更新数据库：新增 CSET @ USENIX Security Symposium, 2021（共13篇）
- 更新数据库：新增 IEEE Transactions on Dependable and Secure Computing, 2021, November（共33篇）
- 更新数据库：新增 ACM Computing Surveys, 2021, November ~ December（共43篇）
- 更新数据库：新增 IEEE Communications Surveys and Tutorials, 2021, Fourthquarter（共24篇）
- 更新数据库：新增 IEEE Transactions on Information Forensics and Security, 2021（共46篇）

2022.02.28
- 更新数据库：新增 IEEE Transactions on Dependable and Secure Computing, 2022, January~February（共49篇）
- 更新数据库：新增 IEEE Transactions on Information Forensics and Security, Volume 17, 2022（共46篇）

2022.03.06
- 更新UI界面：使用 Bootstrap Table 组件重构前端，代码简洁高效
- 更新资源文件：将所需静态资源放在本地，方便无Internet以及本地运行，避免网络波动引起的载入缓慢、显示不正确等问题
- 更新UI界面：新增标签 `esorics`, `csfw`, `dsn`, `compsec`, `raid`, `jcs`, `tissec`, `srds`
- 更新数据库：新增 European Symposium on Research in Computer Security, 2016 ~ 2022 （共356篇）
- 更新数据库：新增 IEEE Computer Security Foundations Symposium, 2016 ~ 2022 （共162篇）
- 更新数据库：新增 Dependable Systems and Networks, 2016 ~ 2022 （共649篇）
- 更新数据库：新增 Computers & Security, 2016 ~ 2022 （共1368篇）
- 更新数据库：新增 International Symposium on Recent Advances in Intrusion Detection, 2016 ~ 2022 （共174篇）
- 更新数据库：新增 Journal of Computer Security, 2016 ~ 2022 （共136篇）
- 更新数据库：新增 ACM Transactions on Privacy and Security, 2016 ~ 2022 （共128篇）
- 更新数据库：新增 IEEE International Symposium on Reliable Distributed Systems, 2016 ~ 2022 （共222篇）

2022.03.07
- 更新UI界面：引入 Mathjax.js，支持 Abstract 内容中包含公式部分的解析。

2022.09.01
- 更新数据库：新增 CSET @ USENIX Security Symposium 2022 （共19篇）
- 更新数据库：新增 IEEE Symposium on Security and Privacy (S&P) 2022（共148篇）
- 更新数据库：新增 USENIX Security Symposium 2022 (Summer/Fall/Winter Accepted Papers)（共256篇）
- 更新数据库：新增 IEEE Communications Surveys and Tutorials Volume 24 (2022), Number 1~3（共56篇）
- 更新数据库：新增 ACM Computing Surveys (CSUR) Volume 55 (2022), Number 2（共21篇）
- 更新数据库：新增 Dependable Systems and Networks (DSN) 2022（共50篇）
- 更新数据库：新增 IEEE Transactions on Dependable and Secure Computing (TDSC) Volume 19 (2022), Number 2~4（共145篇）
- 更新数据库：新增 IEEE Transactions on Information Forensics and Security (TIFS) Volume 17 (2022)（共136篇）
- 更新数据库：新增 Computers & Security (COMPSEC) Volume 115~120 (2022)（共162篇）
- 更新数据库：新增 Journal of Computer Security (JCS) Volume 30 (2022), Number 2~3（共11篇）
- 更新数据库：新增 ACM Transactions on Privacy and Security (TISSEC/TOPS) Volume 25 (2022), Number 2~4（共27篇）

2022.12.13
- 更新数据库：新增 Annual Computer Security Applications Conference (ACSAC) 2022 (共73篇)
- 更新数据库：新增 Computer and Communications Security (CCS) 2022 (共286篇)
- 更新数据库：新增 IEEE Computer Security Foundations Symposium (CSFW) 2022 (共31篇)
- 更新数据库：新增 International Symposium on Recent Advances in Intrusion Detection (RAID) 2022 (共35篇)
- 更新数据库：新增 SOUPS @ USENIX Security Symposium (SOUPS) 2022 (共37篇)
- 更新数据库：新增 European Symposium on Research in Computer Security (ESORICS) 2022 (共110篇)
- 更新数据库：新增 Computers & Security (COMPSEC) Volume 121 ~ 123 (2022) (共85篇)
- 更新数据库：新增 IEEE Communications Surveys and Tutorials (COMSUR) Volume 24 (Fourthquarter 2022) (共20篇)
- 更新数据库：新增 ACM Computing Surveys (CSUR) Volume 55 (Number 1, Number 3) (共43篇)
- 更新数据库：新增 Journal of Computer Security (JCS) Volume 30 (2022), Number 4（共8篇）
- 更新数据库：新增 IEEE Transactions on Dependable and Secure Computing (TDSC) Volume 19 (2022), Number 5~6（共86篇）