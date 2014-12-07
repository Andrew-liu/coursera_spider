#Coursera Spider

>  - coursera.py you can use it to get top 100 movie name which is listed by douban website


##1. Install

> `git clone git@github.com:Andrew-liu/Coursera_Spider.git`


##2. Use It simply

```
$ python coursera.py pkuco-001 #最后一个参数为课程地址
```


##3. Example Output


```python
Coursera git:(master) ✗ python coursera.py pkuco-001
Input your Email > User_name
Input your Password >
登陆成功...
读取网页成功...
正则匹配结束...
下载链接的长度 56
https://class.coursera.org/pkuco-001/lecture/download.mp4?lecture_id=17
...
https://class.coursera.org/pkuco-001/lecture/download.mp4?lecture_id=139
下载pdf的长度 56
抓取Coursera课程下载链接和pdf链接成功
```


##4. Download Script

下载脚本运行

```
$python downloadshell.py coursera.pdf #最后一个参数为连接保存文件
```


更多详细内容请查看[Python-Coursera抓站小结](http://www.jianshu.com/p/c3dbf8294c33)