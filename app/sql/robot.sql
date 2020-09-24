-- 当前文件主要补充相关sql
-- 包括：新增的表、新增的表字段、相关sql等

-- notice文章、工具文章、引导文章相关的信息表
create table article_info(
'id' int not null primary key comment '文章的id',
'article_desc' varchar (220) not null comment '文章概述',
'problem_desc' varchar (220) not null comment '问题描述',
'problem_label' varchar (220) comment '问题标签',
'solution' varchar (220) comment '解决方案',
'version' varchar (220) comment '影响版本',
'component' varchar (220) comment '影响组件',
'article_typeid' varchar (20) comment '文章的类型，可以关联表t_articlle_type',
'author' varchar (20) comment '文章作者',
'last_reviser' varchar (20) comment '文章最后修改人',
'url' varchar (220) comment '文章的链接',
'publish_date' date comment '发布日期",
'modify_date date comment '最近修改日期'
)


-- 用于引导的深度多叉树
create table guidetree_info(
id int not null primary key comment '引导树自己的id',
parent_id int comment '文章的父id，用于拉出检索树，用父id的目的是当前id只会存在一个父id，但是却有若干个子id，便于数据插入',
guide_name varchar (220) comment '引导节点的简称',
level int comment '当前引导树处于多叉树的那个层级，用于(广度优先遍历)输出每一层的结果',
article_id int comment '关联表article_info，树节点对应的文章编号',
author varchar (20) comment '节点作者',
publish_date timestamp comment '发布日期',
modify_date timestamp comment '最近修改日期'
)
;



