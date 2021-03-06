# AIOPS机器人

## 安装

```py
pip3 install sanic==20.3.0
pip3 install jinja2==2.10.3
```

## 运行

```shell
> python chat_server.py

[2020-05-21 22:17:23 +0800] [8764] [DEBUG]

                 Sanic
         Build Fast. Run Fast.


[2020-05-21 22:17:23 +0800] [8764] [INFO] Goin' Fast @ http://127.0.0.1:8000
[2020-05-21 22:17:23 +0800] [8764] [INFO] Starting worker [8764]
```
## 部署方式，使用docker的方式部署
1、编写dockerfile文件，见目录中；
2、运行命令docker build -t chat_robot . --network=host
生成镜像包，需要保证当前的的服务器环境是联网状态的
3、启动方式docker run -d --network=host chat_robot bash

注意：端口冲突，避免使用集群中已监听的端口


## 使用

通过浏览器访问：http://127.0.0.1:8000

# chat_robot

## 基本需求
1、基本界面分为两栏，左边是聊天机器人，右边是展示面板（包含Notice公告、产品分类选项、基本工具、快速入口、建议反馈等）

2、关于聊天记录，在打开的时候应该根据用户选择的组件推出“该组件的常见问题”“最近该组件的重大notice”“search中匹配出来的前五条解决方案”；

3、第二步如果都没有，可以继续让机器人走“引导流程”（之前运维的诊断树，按照层级和用户交互）

4、每一个层级最后新增“以上答案对您是否有帮助”，对于没有帮助的问题可以给出意见反馈，对于有帮助的问题可以加权上热搜；

5、整个机器人的功能参考大厂的一些“智能运维robot”，补足目前ops系统的一些短板。

6、增加自助工具的功能，目前有很多运维诊断工具，看看能不能集成到机器人的展示面板里面。
（包括Inceptor：GC判断工具、txsql备份数据校验工具、网络检测工具、运维诊断工具等等，最好也做一个分类）

7、展示中增加帮助一栏，主要是aiops的使用、问题报不上去等问题应该怎么处理等等说明文档。


## 目标
- 通过机器人解决过滤了多少sla问题，减少人工运维成本。
- 通过机器人系统，将整个sla从问题查询、引导、报备、复盘，形成一个完善的闭环。
- 能形成比较好的用户行为，并可以基于行为分析出产品相关改进点。
- 后期可推广给客户相关付费账号使用。


## 问题
基于以上需求产生的问题

1、目前notice相关信息没有形成模板，没有录入进aiops相关的数据库里？

- （1）、需要出notice模板。
- （2）、需要整理历史相关notice并录入进aiops。
- （3）、aiops上需要开发录入notice的弹窗页面。
- （4）、补充查看notice所有信息的相关页面。

2、基于第一点，notice相关的功能需要完善前后端。
- （1）、前端机器人右侧的展示栏中显示出相关组件最近的十条notice公告。（换页滚动显示）
- （2）、notice需要在aiops上补充一个“输入”+“显示”的界面。Form表单实现将notice录入系统中。

3、目前的“自助工具”需要集中起来，工具+使用文档的方式录入进aiops系统中，录入及查看方式同上。（可按照组件划分）

4、展示侧的“快速入口”比较简单，就是之前说的将“TU”、“手册”、“ownCloud”等链接加进来即可。（加上点好看的图标标）

5、关于展示侧的“组件分类”，aiops目前有个一级分类表t_diagnostic_tree,但是数据不全，另外有新组件的时候要保证aiops能完美加进去；

7、关于机器人的搜索功能，可以直接按照客户聊天记录中的搜索词，使用inceptor search对文章进行检索匹配，并返回值右侧展示栏中；

6、关于聊天机器人的“引导功能”，应该是一个和组件分类关联的多叉深度树。
每个节点应该是一个主题；
每个节点应该有若干个标签；
进入引导状态可以考虑给个地图的小图标，告诉用户当前在引导辅助问题解决；

7、关于机器人如何识别当前是引导状态还是搜索状态，可以参考sla机器人的做法。
使用命令标识，比如：引导：9     搜索：inceptor起不来  这种方式

8、对于每一个回合聊天记录、notice告示、自助工具，都开放点赞评论接口。

9、对于每个节点对应的文章，如何引导过去？或者说文章是以什么方式存储的？


当前的运维文档分类有问题，或者说是不是应该通过添加多个标签的方式来做引导。

引导的树是标签还是一层一层的分类？


