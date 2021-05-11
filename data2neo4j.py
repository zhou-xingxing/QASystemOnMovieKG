# -*- coding: utf-8 -*-
"""
将csv文件导入neo4j数据库
import文件夹是neo4j默认的数据导入文件夹
所以首先要将data文件夹下所有csv文件拷贝到neo4j数据库的根目录import文件夹下，没有则先创建import文件夹
然后运行此程序
"""

from py2neo import Graph

graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="123456"
)
# 清空数据库
graph.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')
print("清空成功")

# 导入节点 电影类型  == 注意类型转换
cql = '''
LOAD CSV WITH HEADERS  FROM "file:///genre.csv" AS line
MERGE (p:Genre{gid:toInteger(line.gid),name:line.gname})
'''
graph.run(cql)
print("电影类别 存储成功")
#
# 导入节点 演员信息
cql = '''
LOAD CSV WITH HEADERS FROM 'file:///person.csv' AS line
MERGE (p:Person { pid:toInteger(line.pid),birth:line.birth,
death:line.death,name:line.name,
biography:line.biography,
birthplace:line.birthplace})
'''
graph.run(cql)
print("演员信息 存储成功")

# 导入节点 电影信息
cql = '''
LOAD CSV WITH HEADERS  FROM "file:///movie.csv" AS line
MERGE (p:Movie{mid:toInteger(line.mid),title:line.title,introduction:line.introduction,
rating:toFloat(line.rating),releasedate:line.releasedate})
'''
graph.run(cql)
print("电影信息 存储成功")

# 导入关系 actedin  电影是谁参演的 1对多
cql = '''
LOAD CSV WITH HEADERS FROM "file:///person_to_movie.csv" AS line
match (from:Person{pid:toInteger(line.pid)}),(to:Movie{mid:toInteger(line.mid)})
merge (from)-[r:actedin{pid:toInteger(line.pid),mid:toInteger(line.mid)}]->(to)
'''
graph.run(cql)
print("参演关系 存储成功")

# 导入关系 is 电影是什么类型 == 1对多
cql = '''
LOAD CSV WITH HEADERS FROM "file:///movie_to_genre.csv" AS line
match (from:Movie{mid:toInteger(line.mid)}),(to:Genre{gid:toInteger(line.gid)})
merge (from)-[r:is{mid:toInteger(line.mid),gid:toInteger(line.gid)}]->(to)
'''
graph.run(cql)
print("所属类别关系 存储成功")

