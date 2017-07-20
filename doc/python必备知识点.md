## 常用的数据类型

### 字符串 列表 字典 集合
>   str:常用用到的函数有:

        > join():字符串拼接,一般情况是用来拼接list,tuple,比如将数据保存到mysql数据库的时候,mysql数据库是不支持list和tuple的类型的
                 用法:
                    >>> l = ['Jack','Jan','Jason']
                    >>> ','.join(l)
                    'Jack,Jan,Jason'
        > replace():替换,比如抓取一条新闻的时间部分,拿到的数据是:
                    res = '\n                2017-07-20 09:57:48\u3000来源: ',通过replace对数据进行处理
                    >>> res.replace(" ","").replace("\n","").replace("\u3000","")
                    '2017-07-2009:57:48来源:'
        > strip():去空格
                    res ='\n                    （原标题：中关村部分企业家到雄安新区调研）\n                '
                    >>> res.strip()
                    '（原标题：中关村部分企业家到雄安新区调研）'
        > split():切割,比如从数据库查到用户名为username = 'Jack,Jan,Jason',需要以列表的形式返回给前台
                    >>> username
                    'Jack,Jan,Jason'
                    >>> username.split(',')
                    ['Jack', 'Jan', 'Jason']

>   list:常用函数有:

        插入元素:分别有三个函数append,extend,insert,现在有一个列表l = ['A','B','C']
        > append():尾部追加元素
                    >>> l = ['A','B','C']
                    >>> l.append('D')
                    >>> l
                    ['A', 'B', 'C', 'D']

        > extend():以迭代的方式,添加元素
                    >>> l = ['A','B','C']
                    >>> l.extend('F')
                    >>> l
                    ['A', 'B', 'C', 'F']

        > insert():指定位置添加元素
                    >>> l = ['A','B','C']
                    >>> l.insert(1,'D')
                    >>> l
                    ['A', 'D', 'B', 'C']

        这三种插入的方式,我感觉最大的区别就是效率问题,就list来说,它在数据结构中属于顺序表,顺序表的插入元素特点是:尾部添加,时间复杂度为O(1),
                    而以其他形式添加,时间复杂度为O(n),所以append的效率相对来说要高,一般情况用到的也是append

        删除元素:也是有三个函数,clear,pop,remove,同样l = ['A','B','C']
        > clear():删除所有元素,一般很少用到
        > pop():默认删除最后一个元素,也可以通过索引来指定,返回的是被删除的元素
                    >>> l = ['A','B','C']
                    >>> l.pop()
                    'C'
        > remove():删除被选中的元素
                    >>> l = ['A','B','C']
                    >>> l.remove('B')
                    >>> l
                    ['A', 'C']

        以顺序表的特点来看,尾部删除元素时间复杂度为O(1),其他位置删除为O(n),所以通过pop()默认删除的话,效率要高

        > sort():排序,比如抓取到几条帖子的评论数分为comment = [400,23,89,100,55],默认排序是从小到大,如果加上reverse=True,则相反也可以
                 通过key来自己指定规则,
                    >>> comment = [400,23,89,100,55]
                    >>> comment.sort()
                    >>> comment
                    [23, 55, 89, 100, 400]

                 关于内置函数sorted(),与sort的区别就是,原函数并没有改变
                    >>> comment = [400,23,89,100,55]
                    >>> c = sorted(comment)
                    >>> c
                    [23, 55, 89, 100, 400]
                    >>> comment
                    [400, 23, 89, 100, 55]

> dict:感觉字典比较随意,创建,获取等都比较直观

        比如:
                    >>> p_info = {"p_id":1116725,"p_title":"联想小新"}
                    >>> type(p_info)
                    <class 'dict'>
                    >>> p_info["p_id"]         # 直接获取
                    1116725
                    >>> p_info.get("p_id")     # 通过get来获取
                    1116725
       一般情况用来做数据封装之后,进行数据传输

> set:最大的特点就是去重,一般情况,也是用来去重,比如,在获取的评论日期中,有可能一天有很多评论,但是我们的需求是只要知道这一天有没有评论就行了,并不需要
      知道评论数,dt = ['2015-06-12','2015-06-23','2015-03-22','2015-06-23']

                    >>> dt = ['2015-06-12','2015-06-23','2015-03-22','2015-06-23']
                    >>> set(dt)
                    {'2015-06-12', '2015-03-22', '2015-06-23'}
      还有一些情况,用来两个数据之间的运算
                    a = "手机便宜,性价比高",b='性价比高,像素也好'
                    >>> a = "手机便宜,性价比高"
                    >>> b='性价比高,像素也好'
                    >>> set(a) & set(b)             # 交集
                    {'价', '高', '性', '比', ','}
                    >>> set(a) | set(b)             # 并集
                    {'机', '也', '好', ',', '手', '宜', '像', '价', '便', '性', '高', '比', '素'}
                    >>> set(a) - set(b)             # 差集
                    {'手', '机', '宜', '便'}
                    >>> set(a) ^ set(b)             # 交叉补集
                    {'也', '机', '好', '手', '宜', '像', '便', '素'}

## 内置函数

>  map():主要用来修改列表里的元素,和列表解析差不多,在效率上也差不多,dt = ['2015-06-12','2015-06-23','2015-03-22','2015-06-23'],想把里面的字符串时期

          格式化成日期格式
                    >>> list(map(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d'),dt))
                    [datetime.datetime(2015, 6, 12, 0, 0), datetime.datetime(2015, 6, 23, 0, 0), datetime.datetime(2015, 3, 22, 0, 0), datetime.datetime(2015, 6, 23, 0, 0)]
                    >>> [datetime.datetime.strptime(d,'%Y-%m-%d') for d in dt]
                    [datetime.datetime(2015, 6, 12, 0, 0), datetime.datetime(2015, 6, 23, 0, 0), datetime.datetime(2015, 3, 22, 0, 0), datetime.datetime(2015, 6, 23, 0, 0)]
          就个人而言,我感觉,列表解析更加直观,简洁

> zip():合并列表,将对应的元素合并成一个元组,合并之后,通过*来解压

                    >>> mall = ["京东商城","天猫商城","zol商城"]
                    >>> price = ["1599","1499","1549"]
                    >>> z = zip(mall,price)
                    >>> list(z)
                    [('京东商城', '1599'), ('天猫商城', '1499'), ('zol商城', '1549')]

## 装饰器

> 一般情况都是用来做登录验证

                    >>> def auth(func):
                    ...     def wrapper(request,*args,**kwargs):
                    ...             if request.session.has_key('username'):
                    ...                     result = func(request,*args,**kwargs)
                    ...             else:
                    ...                     result = redirect('/login')
                    ...             return result
                    ...     return wrapper

                    >>> @auth
                    ... def cart(request):
                    ...     return render(reeuqet,'cart.html')


注:以上只是我常用到的,有的在项目中也会用到,需要知道更全面的,就去查看官方文档了




































