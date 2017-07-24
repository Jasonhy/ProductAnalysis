## NumPy基础

>   创建ndarray的常用函数:

        array():将输入数据(列表,元组,数组或其他序列类型)直接转换为ndarray
            >>> import numpy as np
            # 创建一维数组
            >>> np.array([2,4,5,9])
            array([2, 4, 5, 9])

            # 创建二维数组
            >>> np.array([[3,5],[8,9]])
            array([[3, 5],
                   [8, 9]])

        arange():类似range函数
            >>> np.arange(6)
            array([0, 1, 2, 3, 4, 5])

        reshape():改变数组的维度
            >>> n1 = np.arange(16)
            >>> n1
            array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])
            >>> n1.shape            # 查看数组的维度
            (16,)
            >>> n2 = n1.reshape(4,4)        # 四行四列
            >>> n2
            array([[ 0,  1,  2,  3],
                   [ 4,  5,  6,  7],
                   [ 8,  9, 10, 11],
                   [12, 13, 14, 15]])
            >>> n2.shape
            (4, 4)

>   索引:主要用来获取值

        一维数组的获取:
            >>> n3 = np.arange(16,step=2)
            >>> n3
            array([ 0,  2,  4,  6,  8, 10, 12, 14])
            >>> n3[3]           # 获取特定索引下的值
            6
            >>> n3[4:]          # 切片的形式,索引为4到最后
            array([ 8, 10, 12, 14])
            >>> n3[:4]
            array([0, 2, 4, 6])
            >>> n3[2:6]             # 索引2到6之间,不包含6
            array([ 4,  6,  8, 10])

        二维数组的获取:
            >>> n2
            array([[ 0,  1,  2,  3],
                   [ 4,  5,  6,  7],
                   [ 8,  9, 10, 11],
                   [12, 13, 14, 15]])
            >>> n2[1:2]             # 在没有逗号分隔的情况,默认按行
            array([[4, 5, 6, 7]])
            >>> n2[:,2:]            # 逗号分隔后面是按列取
            array([[ 2,  3],
                   [ 6,  7],
                   [10, 11],
                   [14, 15]])

        通过数组的形式获取值:
            >>> n2
            array([[ 0,  1,  2,  3],
                   [ 4,  5,  6,  7],
                   [ 8,  9, 10, 11],
                   [12, 13, 14, 15]])

            >>> n2[[1,3],[2,3]]
            array([ 6, 15])

        bool索引:
            >>> n4 = n2 >= 10
            >>> n4
            array([[False, False, False, False],
                   [False, False, False, False],
                   [False, False,  True,  True],
                   [ True,  True,  True,  True]], dtype=bool)

            >>> n2[n4]                      # 通过布尔索引来获取值
            array([10, 11, 12, 13, 14, 15])

## pandas

### 两大数据结构

>   Series:可以看成是一维数组加上索引组成的对象

            >>> import pandas as pd
            >>> from pandas import Series,DataFrame
            >>> s = Series(np.arange(5),index=['a','b','c','d','e'])        # 通过index来指定索引
            >>> s
            a    0
            b    1
            c    2
            d    3
            e    4
            dtype: int32
            >>> s.index
            Index(['a', 'b', 'c', 'd', 'e'], dtype='object')
            >>> s.values
            array([0, 1, 2, 3, 4])

            字典的形式创建Series,字典的key默认变成索引
            >>> p_info = {"p_id":120364,"p_title":"雷神","p_price":12800}
            >>> s_p = Series(p_info)
            >>> s_p
            p_id       120364
            p_price     12800
            p_title        雷神
            dtype: object



>   DataFrame:是一个表格型的数据结构对象,所以它既有列索引,也有行索引,也可以看成是由Series组成的字典

        创建方式一般是直接传入一个字典
            >>> p_infos = {"p_title":["雷神","机械师","战神"],
            ...            "p_price":[12288,13000,8999],
            ...            "p_score":[7.8,6.8,8.9]}
            >>> d_p = DataFrame(p_infos)
            >>> d_p
               p_price  p_score p_title
            0    12288      7.8      雷神
            1    13000      6.8     机械师
            2     8999      8.9      战神

        排序
           按照索引排序
            >>> d_p.sort_index(ascending=False)
               p_price  p_score p_title
            2     8999      8.9      战神
            1    13000      6.8     机械师
            0    12288      7.8      雷神
           按照某一列排序
            >>> d_p.sort_values(by="p_score")
               p_price  p_score p_title
            1    13000      6.8     机械师
            0    12288      7.8      雷神
            2     8999      8.9      战神


        数据的获取
            >>> d_p.iloc[1]
            p_price    13000
            p_score      6.8
            p_title      机械师
            Name: 1, dtype: object

            >>> d_p.loc[:,"p_title"]
            0     雷神
            1    机械师
            2     战神
            Name: p_title, dtype: object

>   关于数据丢失的处理

            >>> p_infos2 = {"p_title":["雷神","机械师","战神","飞行堡垒"],
            ...             "p_score":[7.8,6.8,8.9,6.7],
            ...             "p_price":[12288,13000,8999,6799]}
            >>> d_p2 = DataFrame(p_infos2)
            >>> d_p2
               p_price  p_score p_title
            0    12288      7.8      雷神
            1    13000      6.8     机械师
            2     8999      8.9      战神
            3     6799      6.7    飞行堡垒

            d_p2.loc[3,"p_score"] = np.nan
            >>> d_p2
               p_price  p_score p_title
            0    12288      7.8      雷神
            1    13000      6.8     机械师
            2     8999      8.9      战神
            3     6799      NaN    飞行堡垒

       直接将缺失数据丢掉
            >>> d_p2.dropna()
               p_price  p_score p_title
            0    12288      7.8      雷神
            1    13000      6.8     机械师
            2     8999      8.9      战神

       填充的方式
            >>> d_p2.fillna(10)
               p_price  p_score p_title
            0    12288      7.8      雷神
            1    13000      6.8     机械师
            2     8999      8.9      战神
            3     6799     10.0    飞行堡垒


>   统计

       求平均值:
            >>> d_p2.mean()
            p_price    10271.500000
            p_score        7.833333

       求和:
            >>> d_p2.sum()
            p_price          41086
            p_score           23.5
            p_title    雷神机械师战神飞行堡垒

>   函数的应用

        >>> d = d_p2.loc[:,"p_price"]
        >>> d
        0    12288
        1    13000
        2     8999
        3     6799
        Name: p_price, dtype: int64

        >>> d.apply(lambda x : float(x))
        0    12288.0
        1    13000.0
        2     8999.0
        3     6799.0
        Name: p_price, dtype: float64


更多应用查看官方文档:http://pandas.pydata.org/




























































