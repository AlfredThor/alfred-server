from datetime import datetime
from settings.tools.tool import tool_tool
from config.config import Base
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy import Column, Integer, String, DateTime, JSON, TEXT, Date, Boolean, Text


'''Postgres'''
class BaseModel(object):
    create_time = Column(DateTime, default=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self, exclude=[], reverse=True, time_=True):
        '''
        reverse=True: not in exclude：输出去除该列表里面的字段
        reverse=False: in exclude：输出只有该列表里面的字段
        '''
        if reverse:
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}
        else:
            if time_:
                exclude = exclude + ['create_time', 'update_time']
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in exclude}

        if time_:
            if 'create_time' in data:
                data['create_time'] = data['create_time'].strftime('%Y-%m-%d %H:%M:%S') if data['create_time'] else ''
            if 'update_time' in data:
                data['update_time'] = data['update_time'].strftime('%Y-%m-%d %H:%M:%S') if data['update_time'] else ''
        return data


class User(Base, BaseModel):
    """
    用户表：用于存储博客用户信息（如作者/管理员）
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    email = Column(String(100), unique=True, nullable=True, comment='电子邮件')
    password = Column(String(255), nullable=False, comment='密码（加密存储）')
    is_admin = Column(Boolean, default=False, comment='是否为管理员')
    create_time = Column(DateTime, default=datetime.now, comment='用户创建时间')


class Category(Base, BaseModel):
    """
    分类表：用于组织文章的类别（如技术、生活、随笔）
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='分类ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    name = Column(String(50), unique=True, nullable=False, comment='分类名称')
    description = Column(Text, nullable=True, comment='分类描述')


class Tag(Base, BaseModel):
    """
    标签表：文章标签（如Python、前端、数据库）
    """
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='标签ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    name = Column(String(30), unique=True, nullable=False, comment='标签名称')


class Article(Base, BaseModel):
    """
    文章表：存储博客文章内容
    """
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='文章ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    title = Column(String(200), nullable=False, comment='文章标题')
    content = Column(Text, nullable=False, comment='文章内容')
    summary = Column(Text, nullable=True, comment='文章摘要')
    author_id = Column(Integer, nullable=False, comment='作者ID（对应 user.id）')
    category_id = Column(Integer, nullable=True, comment='分类ID（对应 category.id）')
    tag_ids = Column(String(255), nullable=True, comment='文章标签ID列表（逗号分隔）')
    is_published = Column(Boolean, default=True, comment='是否发布')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class Comment(Base, BaseModel):
    """
    评论表：用户对文章的评论
    """
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='评论ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    article_id = Column(Integer, nullable=False, comment='文章ID（对应 article.id）')
    user_id = Column(Integer, nullable=True, comment='评论用户ID（对应 user.id，可匿名）')
    content = Column(Text, nullable=False, comment='评论内容')
    is_reviewed = Column(Boolean, default=False, comment='是否已审核')


class FriendLink(Base, BaseModel):
    """
    友情链接表：展示在页面底部的友链信息
    """
    __tablename__ = 'friend_link'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='友链ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    name = Column(String(50), nullable=False, comment='网站名称')
    url = Column(String(200), nullable=False, comment='网站链接')
    description = Column(String(255), nullable=True, comment='链接说明')
    is_visible = Column(Boolean, default=True, comment='是否显示')


class SiteSetting(Base, BaseModel):
    """
    网站配置表：保存网站标题、备案号等信息
    """
    __tablename__ = 'site_setting'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='设置项ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    key = Column(String(50), unique=True, nullable=False, comment='配置键名')
    value = Column(String(255), nullable=True, comment='配置值')
    description = Column(String(255), nullable=True, comment='配置项说明')


class VisitLog(Base, BaseModel):
    """
    访问日志表：记录用户访问情况
    """
    __tablename__ = 'visit_log'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='访问记录ID')
    uuid = Column(String(32), index=True,unique=True, default=tool_tool.generate_uuid)
    ip = Column(String(50), nullable=True, comment='访问者IP地址')
    path = Column(String(255), nullable=False, comment='访问路径')
    user_agent = Column(String(255), nullable=True, comment='User-Agent')
    access_time = Column(DateTime, default=datetime.now, comment='访问时间')


class Donation(Base, BaseModel):
    """
    打赏记录表：记录用户对文章或作者的打赏信息
    """
    __tablename__ = 'donation'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='打赏ID')
    amount = Column(Integer, nullable=False, comment='打赏金额（单位：分）')
    donor_name = Column(String(50), nullable=True, comment='打赏人昵称（可匿名）')
    message = Column(String(255), nullable=True, comment='留言信息')
    article_id = Column(Integer, nullable=True, comment='文章ID（为空表示打赏作者）')
    author_id = Column(Integer, nullable=False, comment='作者ID（收款人）')


class ArticleRecommend(Base, BaseModel):
    """
    推荐文章表：用于设置首页推荐、置顶等文章推荐信息
    """
    __tablename__ = 'article_recommend'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='推荐ID')
    article_id = Column(Integer, nullable=False, comment='文章ID')
    recommend_type = Column(String(30), nullable=False, comment='推荐类型（首页推荐 / 热门推荐 / 编辑精选）')
    order_index = Column(Integer, default=0, comment='排序权重（越大越靠前）')
    start_time = Column(DateTime, nullable=True, comment='推荐开始时间')
    end_time = Column(DateTime, nullable=True, comment='推荐结束时间')


class Feedback(Base, BaseModel):
    """
    意见反馈表：收集用户的建议、问题或吐槽
    """
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='反馈ID')
    content = Column(Text, nullable=False, comment='反馈内容')
    contact = Column(String(100), nullable=True, comment='联系方式（可填写邮箱、QQ 等）')
    is_handled = Column(Boolean, default=False, comment='是否已处理')
    handle_note = Column(String(255), nullable=True, comment='处理备注')


class ChatMessage(Base, BaseModel):
    """
    聊天消息记录
    """
    __tablename__ = 'chat_message'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='消息ID')
    room_id = Column(Integer, nullable=False, comment='聊天室ID，默认为1')
    user_id = Column(Integer, nullable=True, comment='发送者用户ID，可匿名')
    username = Column(String(50), nullable=True, comment='发送者名称（匿名/用户）')
    content = Column(Text, nullable=False, comment='消息内容')
    msg_type = Column(String(20), default='text', comment='消息类型：text/image')


class ChatUserOnline(Base, BaseModel):
    """
    聊天室在线用户（用于标记“已加入”）
    """
    __tablename__ = 'chat_user_online'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='记录ID')
    room_id = Column(Integer, nullable=False, comment='聊天室ID，默认为1')
    user_id = Column(Integer, nullable=True, comment='用户ID（可匿名）')
    username = Column(String(50), nullable=True, comment='昵称')
    ip = Column(String(50), nullable=True, comment='IP地址')
    join_time = Column(DateTime, default=datetime.now, comment='加入时间')
