import pyhdfs

fs = pyhdfs.HdfsClient(hosts='81.70.253.212:51070', user_name='root')

# 返回目录，路径，文件名
print(list(fs.walk('/')))
print(fs.listdir('/data'))
# 绝对路径
for i in fs.listdir("/data"):
    # HDFS下载到本地
    fs.copy_to_local("/data/"+i,"E:/研究生课程/大数据专题/movie_KGQA/data/"+i)

# 数据预处理
import pandas as pd
path="data/"
file = "movie.csv"
newpath="data/"
data = pd.read_csv(path+file,encoding='utf-8')
# 处理空值
data[u'introduction'] = data[u'introduction'].apply(lambda x: '无' if pd.isna(x)  else x)
data[u'releasedate'] = data[u'releasedate'].apply(lambda x: '2000/1/1' if pd.isna(x)  else x)
# 处理多余引号
data[u'introduction'] = data[u'introduction'].apply(lambda x: x.replace('"', ''))
data.to_csv(newpath+file,index=False, encoding='utf-8')


import os
print(os.listdir("data"))
# 新建目录
fs.mkdirs("/new_data")
for i in os.listdir("data"):
    # 上传到HDFS
    fs.copy_from_local("E:/研究生课程/大数据专题/movie_KGQA/data/"+i,"/new_data/"+i)


# print(fs.listdir('/input'))
# print(fs.get_home_directory())
#
# print(fs.get_active_namenode())
# print(fs.list_status('/input/README.txt'))
# 必须绝对路径
# fs.copy_to_local('/input/README.txt',"E:/研究生课程/大数据专题/movie_KGQA/README.txt")  # 从hadoop下载到本地
# fs.copy_from_local("E:\研究生课程\大数据专题\movie_KGQA\README.md", '/input/README.md')  # 从本地上传到hadoop上
# 追加内容
# fs.append("/input/README.txt","hello")
# res = fs.open('/input/README.txt')
# for r in res:
#     line=str(r,encoding='utf8')#open后是二进制,str()转换为字符串并转码
#     print(line)
# fs.mkdirs("/output")

# 查看文件是否存在
# print(fs.exists("/input/README.txt"))


# fs.delete("/output", recursive=True)  # 删除目录  recursive=True
# fs.delete("/input/README.md")  # 删除文件




