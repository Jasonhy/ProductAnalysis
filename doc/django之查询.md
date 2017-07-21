## 开篇说明

个人感觉django是一个很大的框架,通过几篇文章就想把django搞清,这难度有点大,这里,我只挑我认为最重要的也就是经常用到的----模型层中的查询,中文文档我也上传了,需要的可以下载

## QuerySet
一个对象的集合,可以包含多个过滤器,过滤器等价于mysql中的where和limit,而queryset等价于select,一般情况下,都看到一个模型类.objects这个返回的就是一个queryset对
象,而这个objects就是一个Manager,Manager实际就是数据库查询操作的一个接口

特点:QuerySet是惰性的,QuerySet创建不涉及到任何数据库操作,除非这个QuerySet被调用

>   models类:

    class UserInfo(models.Model):
    """
    用户信息
    """
    username = models.CharField(max_length=32,verbose_name="用户名",unique=True)      # unique 设置字段唯一
    gender_type = (
        (0,"保密"),
        (1,"男"),
        (2,"女")
    )
    gender = models.IntegerField(choices=gender_type,verbose_name="性别",default=0,help_text="请选择您的性别")

    class Meta:
        db_table = "user_info"      # 设置数据库表名
        verbose_name_plural = "用户表"

    def __str__(self):

        return self.username

    class CardInfo(models.Model):
        """
        帖子信息
        """
        title = models.CharField(max_length=32,verbose_name="帖子标题")
        content = models.TextField()
        ui_id = models.ForeignKey("UserInfo",verbose_name="用户")
        ci_id = models.ForeignKey("CircleInfo",verbose_name="圈子")
        create_time = models.DateTimeField(verbose_name="帖子创建日期",auto_now_add=True)

        def __str__(self):

            return "%s/%s" % (self.title,self.create_time)

        class Meta:
            db_table = "card_info"
            verbose_name_plural = "帖子信息表"
            ordering = ["create_time"]          # 根据创建日期来排序


    class CircleInfo(models.Model):
        """
        圈子信息
        """
        circle_name = models.CharField(max_length=32,verbose_name="圈子标题")
        ui_id = models.ManyToManyField("UserInfo",verbose_name="用户")

        class Meta:
            db_table = "circle_info"
            verbose_name_plural = "圈子信息表"

        def __str__(self):

            return "id=%s,circle_name=%s" % (self.id,self.circle_name)


>   粗看objects

        >>> from app.models import *
        >>> obj = CircleInfo.objects
        >>> obj
        <django.db.models.manager.Manager object at 0x0339B150>         # 这里可以看出objects实际就是一个Manager

        通过dir(obj)就可以查看里面的属性了,比如:
        ['aggregate', 'all', 'annotate', 'auto_created', 'bulk_create', 'check', 'complex_filter', 'contribute_to_class', 'count', 'create',
         'creation_counter', 'dates', 'datetimes','db', 'db_manager', 'deconstruct', 'defer', 'distinct', 'earliest', 'exclude', 'exists', 'extra',
         'filter', 'first', 'from_queryset', 'get', 'get_or_create', 'get_queryset', 'in_bulk', 'iterator', 'last', 'latest', 'model', 'name',
         'none', 'only', 'order_by', 'prefetch_related', 'raw', 'reverse', 'select_for_update', 'select_related', 'update', 'update_or_create', 'use_in_migrations',
         'using', 'values', 'values_list']

>   常用属性

        > all():获取一个表中所有的对象,返回的是一个QuerySet对象
            >>> obj.all()
            <QuerySet [<CircleInfo: 时尚潮流>, <CircleInfo: 造型>, <CircleInfo: 爱美剪发>]>
        > filter():过滤器,通过条件来删选自己想要的
            >>> obj.filter(circle_name="爱美剪发")      # 过滤出circle_name为爱美剪发的圈子
            <QuerySet [<CircleInfo: 爱美剪发>]>

        > order_by():默认是升序,如果想要降序的话,加上负号
            >>> obj.order_by("id")
            <QuerySet [<CircleInfo: id=1,circle_name=时尚潮流>, <CircleInfo: id=2,circle_name=造型>, <CircleInfo: id=3,circle_name=爱美剪发>]>
            >>> obj.order_by("-id")
            <QuerySet [<CircleInfo: id=3,circle_name=爱美剪发>, <CircleInfo: id=2,circle_name=造型>, <CircleInfo: id=1,circle_name=时尚潮流>]>

>   关于双下划线

        __gt:大于
        __gte:大于等于
        __lt:小于
        __lte:小于等于
        __in:在...内
        __isnull:是否null
        __contains:包含,大小写敏感
        __icontains:包含,大小写不敏感
        __range:范围
        __startswith:以什么开头
        __endswith:以什么结尾

        __字段名:用来反向查询

            >>> obj.all()
            <QuerySet [<CircleInfo: id=1,circle_name=时尚潮流>, <CircleInfo: id=2,circle_name=造型视觉>, <CircleInfo: id=3,circle_name=爱美剪发>, <CircleInfo: id=4,circle_name=销售管理>, <CircleInfo: id=5,circle_name=染发色彩>]>
            >>> obj.filter(id__lt=3)
            <QuerySet [<CircleInfo: id=1,circle_name=时尚潮流>, <CircleInfo: id=2,circle_name=造型视觉>]>
            >>> obj.filter(id__in=[2,3,5])
            <QuerySet [<CircleInfo: id=2,circle_name=造型视觉>, <CircleInfo: id=3,circle_name=爱美剪发>, <CircleInfo: id=5,circle_name=染发色彩>]>

            反向查询的使用
            比如现在想知道当前圈子有哪些帖子:
            >>> CircleInfo.objects.filter(id=2).values("cardinfo__title")
            <QuerySet [{'cardinfo__title': '杀马特'}, {'cardinfo__title': '脸型是圆'}]>
            查看帖子数:
            >>> CircleInfo.objects.filter(id=2).values("cardinfo__title").count()
            2

>   Q对象:主要是用来构造搜索条件的,对于filter来说,条件都是AND,如果想实现OR关系,这个时候,就可以通过Q来实现,多个Q对象可以通过|和&来连接,如果想取反,就在Q前面加~

        比如现在想查询圈子名为"爱美剪发"或者"造型视觉"下的帖子:
            >>> obj.filter(Q(circle_name="爱美剪发") | Q(circle_name="造型视觉")).values("cardinfo__title")
            <QuerySet [{'cardinfo__title': '杀马特'}, {'cardinfo__title': '脸型是圆'}, {'cardinfo__title': '什么发型好看'}]>
        如果多个Q之间用","隔开就变成了AND关系,比如现在查询名字为Lily的并且并且在造型视觉发的帖子
            >>> CardInfo.objects.filter(Q(ui_id__username="Lily"))
            <QuerySet [<CardInfo: 锅盖头/2017-07-21 01:19:43.964961+00:00>, <CardInfo: 超卷发好看吗/2017-07-21 06:19:17.451754+00:00>]>
            >>> CardInfo.objects.filter(Q(ui_id__username="Lily"),Q(ci_id__circle_name="造型视觉"))
            <QuerySet [<CardInfo: 超卷发好看吗/2017-07-21 06:19:17.451754+00:00>]>

>   反向关联:*_set,_set前面关联的models类名小写,而这个_set是属于被关联models类的属性,比如,现在每个CardInfo都要关联到一个CircleInfo,那么现在通过反向关联,说着有点绕,简单的说就是,ForeignKey或者ManyToManyField字段
            在那个models下,那么_set前面就是这个models的小写,通过这个这段指向的那个models对象来调用

            比如:
            >>> circle_info = CircleInfo.objects.get(id=2)
            >>> circle_info.cardinfo_set.all()
            <QuerySet [<CardInfo: 杀马特/2017-07-21 01:18:12.834748+00:00>, <CardInfo: 脸型是圆/2017-07-21 05:29:43.799671+00:00>, <CardInfo: 超卷发好看吗/2017-07-21 06:19:17.451754+00:00>]>
            >>> user_info = UserInfo.objects.get(id=1)
            >>> user_info.circleinfo_set.all()
            <QuerySet [<CircleInfo: id=1,circle_name=时尚潮流>, <CircleInfo: id=4,circle_name=销售管理>]>


>   其他常用API:

        values():迭代返回的是一个字典

            如:
            >>> obj.values()
            <QuerySet [{'id': 1, 'circle_name': '时尚潮流'}, {'id': 2, 'circle_name': '造型视觉'}, {'id': 3, 'circle_name': '爱美剪发'}, {'id': 4, 'circle_name': '销售管理'}, {'id': 5, 'circle_name': '染发色彩'}]>
            >>> for o in obj.values():
            ...     type(o)
            ...
            <class 'dict'>
            <class 'dict'>
            <class 'dict'>
            <class 'dict'>
            <class 'dict'>

        select_related():有的时候在查询数据的时候,会用到关联表数据,而这些数据在后面的也会用到,这个时候就可以通过这个函数进行关联查询,这种查询虽然会影响到性能的损耗,但是在接下来的应用都将不会操作数据库

            如:
            >>> cardinfo = CardInfo.objects.select_related("ci_id").get(id=2)
            >>> cardinfo.ci_id
            <CircleInfo: id=1,circle_name=时尚潮流>

        aggregate():聚合查询,返回的是一个字典

            如:
            >>> CircleInfo.objects.filter(id=2).aggregate(Count("cardinfo"))
            {'cardinfo__count': 3}


















