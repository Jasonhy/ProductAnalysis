# 官方文档:https://doc.scrapy.org/en/master/topics/architecture.html

## 数据抓取流程
![](../screen/Scrapy流程.png)

### 各个组件的功能:

>   1.Engine:引擎,图中它是位于中间的位置,所以它的主要功能就是用来提供Spider,ItemPipelines,Scheduler,Downloader之间通信的渠道

>   2.Scheduler:调度器,负责接收Engine发送过来的Request,按照一定的形式进行排列,并将Request返回给引擎

>   3.Downloader:下载器,负责下载Engine里所有的Request,然后将获取到的Response交给Engine

>   4.Spider:负责发送Request和接收Response,对Response里的数据进行提取,分析,如果有需要跟进的URL,再次将这个Request交给Engine

>   5.Item Pipeline:管道,负责处理Spider中数据,并对这些数据进行处理,比如将数据存储到数据库

>   6.Middlewares:中间件,包括Downloader Middlewares 和 Spider Middewares,有的时候需要对一些请求进行处理,比如添加请求头,设置动态代理,那么这个任务就可以交给Downloader Middlewares来完成,同时,当Downloader下载
完成将Response返回给Engine的时候,这个时候Downloader Middlewares也可以对Response进行一定的处理;对于Spider Middlewares,如果需要在Spider和Engine之间的的Request和Response进行扩展的话,可以通过Spider Middewares来实现

### 流程
>   对于流程的话,就是按照上图那样进行的,我感觉需要解释的就是第八步,第八步那里为什么会有两个指向箭头呢?当一个Spider完成了第六步之后,也就是接收到了
Response,可以说,这个时候完成了一次请求,这个时候有两种情况就是,这个Response处理完的结果一种是需要Item Pipeline处理数据,一种还有就是里面有需要跟进的URL,比如分页,所以就把需要进行数据处理的交给Item Pipeline,需要跟进的URL交给Scheduler,由Scheduler将这个URL加入队列进行处理

### 项目的创建
>   scrapy startproject autohomeProduct
    进入spider所在的目录:

    如果创建的是Spider类:scrapy genspider autohome "autohome.com.cn",这样就创建了一个spider,如:
        import scrapy
        class AutohomeSpider(scrapy.Spider):
            name = 'autohome'
            allowed_domains = ['autohome.com.cn']
            start_urls = ['http://autohome.com.cn/']

            def parse(self, response):
                pass

    如果创建的是CrawlSpiders类:scrapy genspider -t crawl autohome2 autohome.com.cn,如:

        from scrapy.linkextractors import LinkExtractor
        from scrapy.spiders import CrawlSpider, Rule


        class Autohome2Spider(CrawlSpider):
            name = 'autohome2'
            allowed_domains = ['autohome.com.cn']
            start_urls = ['http://autohome.com.cn/']

            rules = (
                Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
            )

            def parse_item(self, response):
                i = {}
                #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
                #i['name'] = response.xpath('//div[@id="name"]').extract()
                #i['description'] = response.xpath('//div[@id="description"]').extract()
                return i

    这样项目就创建完成了

## 关于Item
先从Item讲起,就是因为,我们要抓取数据,必须清楚自己需要的是什么数据,比如现在我们需要的数据如下:

        import scrapy

        class AutohomeproductItem(scrapy.Item):
            # 车名
            title = scrapy.Field()
            # 车价
            price = scrapy.Field()
            # 车图片
            pic = scrapy.Field()
            # 车评分
            grade = scrapy.Field()
            # 油耗
            fuel_consumption = scrapy.Field()

    创建Item的方式,可以通过创建对象的方式,也可以通过字典的形式

        创建对象的方式:
        >>> from autohomeProduct.items import AutohomeproductItem
        >>> ahpitem = AutohomeproductItem()
        >>> ahpitem['title'] = '宝马'
        >>> ahpitem['price'] = '56万'
        >>> ahpitem['pic'] = '1.png'
        >>> ahpitem['grade'] = '8.6分'
        >>> ahpitem['fuel_consumption'] = '12.6L'
        >>> ahpitem
        {'fuel_consumption': '12.6L',
         'grade': '8.6分',
         'pic': '1.png',
         'price': '56万',
         'title': '宝马'}

        字典的方式:
        >>> autoinfo = {'fuel_consumption': '12.6L',
        ...          'grade': '8.6分',
        ...          'pic': '1.png',
        ...          'price': '56万',
        ...          'title': '宝马'}
        >>> item = AutohomeproductItem(autoinfo)
        >>> item
        {'fuel_consumption': '12.6L',
         'grade': '8.6分',
         'pic': '1.png',
         'price': '56万',
         'title': '宝马'}

## 关于Spider和CrawlSpider
主要就是用来定义需要爬取的网站,还有就是需要爬取的规则,并根据获取的网页内容提取需要的数据

    执行规则:先调用Spider的__init__方法,初始化name和start_urls,在不重写start_requests的情况下,又start_requests读取start_urls里面的内容,而start_requests实际调用的是make_requests_from_url将url交给Request去处
    理,以parse为回调函数返回,在parse里面就有我们需要的网页信息Response,然后通过选择器来提取需要的内容

    相关函数:
        start_requests():返回的是一个迭代器对象,所以一般情况将其实现生成器,如果我们我的请求需要提交参数,添加请求头或者进行数据的传递的时候,可以重写这个方法

        make_requests_from_url():接收一个url参数,并返回一个Request对象,未被重写的情况下,默认parse作为回调函数

        parse():处理返回的Response信息

        closed():当spider关闭的时候,该函数被调用

    >   CrawlSpider:除了具有Spider的功能外,还提供了一些规则来继续跟进

        rules:包含一个或多个Rule对象的元组,这个Rule对象定义的就是需要跟进的规则,还有就是对返回信息的处理,在Rule对象,有个参数需要值得要注意一下,就是,当我们在爬取数据的时候,有的网站可能需要跟进的链接进行变动,这个时候,
        可以通过process_links参数对提取的链接进行处理,一般情况下都是一个回调函数

    >   其他的Spider:
        XMLFeedSpider:主要是用来分析XML源的
        CSVFeedSpider:顾名思义也就是CSV源,和XMLFeedSpider有点相似,只不过它是按行遍历,XMLFeedSpider是按节点遍历
        SitemapSpider:通过Sitemaps来发现需要爬取的URL,比如(官网的示例):
            from scrapy.spiders import SitemapSpider

            class MySpider(SitemapSpider):
                sitemap_urls = ['http://www.example.com/sitemap.xml']
                sitemap_rules = [
                    ('/product/', 'parse_product'),
                    ('/category/', 'parse_category'),
                ]

                def parse_product(self, response):
                    pass # ... scrape product ...

                def parse_category(self, response):
                    pass # ... scrape category ...

## 关于选择器
除了常用的xpath之外,还有就css,同时还支持re和set匹配规则,用到的就去官网查看吧-----Selector

## 关于Item Pipeline
当我们在Spider的回调函数yield一个item的时候,数据就会传递到Item Pipeline,在这里对每个Item进行处理

    >   必须要实现的方法:
            process_item():如果需要pipeline继续处理item,必须将item返回,当抛出异常,这个item将会被丢弃
                参数:item-->被抓取的item
                    spider-->抓取该item的spider

    >   可以实现的方法:
            open_spider():当spider被开启的时候,就会调用,比如需要将数据保存到数据的时候,可以在这里进行数据库的初始化工作以及数据库的连接操作

            close_spider():当spider关闭的时候,会调用,比如,在进行数据保存完成之后,可以在这里执行数据库关闭操作

## 关于Downloader Middleware
介于request和response之间,主要用来全局修改request和response

    >   常用函数:
        process_request():每个request通过下载中间件时,该方法都会被调用

            关于返回值:
            1.如果返回的是None,将会继续处理该request
            2.如果返回的是Response对象,scrapy将不会调用其他的process_request或者process_exception方法,然后将返回该response
            3.如果返回Request对象,scrapy则停止调用process_request方法,并重新调度返回的request
            4.如果抛出异常,测process_exception会被调用

            关于参数:
                request:需要处理的request
                spider:request对应的spider

        process_response():
            关于返回值:
            1.如果返回的是一个Response,该response会被下一个中间件继续执行
            2.如果返回一个Request,中间件链会停止,返回的request会被重新调度下载
            3.如果抛出异常,则会调用request的errback

        关于内置的中间件可以查看文档,比如CookiesMiddleware,HttpProxyMiddleware等

## 关于Spider Middleware
可以在这里添加代码来处理发送给Spider的response及spider产生的item和request

    >   常用函数:
        process_spider_input():当response通过spider中间件时,这个方法会被调用,处理该response

        关于返回值:
        1.如果返回None,scrapy将继续处理该response
        2.如果抛出异常,则会调用request的errback,errback指向的是process_spider_output()来处理,如果这个方法也抛出异常,则会调用process_spider_exception()

        process_spider_output():处理response返回result时,该方法会被调用

        process_start_requests():以spider启动的request为参数被调用

## 关于Requests 和 Responses

    >   Request对象:
        有关参数:
            url:请求的url
            callback:请求返回的Response,由哪个函数处理
            method:指定请求方式
            headers:添加请求头信息
            meta:不同请求之间数据传递
            encoding:默认utf8
            cookies:请求的cookies
            dont_filter:表明该请求不由调度器过滤,默认就是False
            errback:指定处理错误函数

    >   Response对象:
        有关参数:
            url:响应的url
            status:响应状态码
            headers:响应头
            request:生成此响应的请求头

## 关于settings
关于settings的配置,可以查看官方文档












