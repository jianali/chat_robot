# 访问数据库，实现对象和数据库的关系映射，这里使用对象关系映射模型SQLAalchemy
import asyncio
import asyncpg



if __name__ == '__main__':
    print(session.query(diagnostic_tree).all())
