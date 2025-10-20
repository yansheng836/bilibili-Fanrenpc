#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 爬取B站《凡人修仙传》数据
@author: yansheng
@file: main.py
@time: 2025/10/20
"""
from spider import SpiderUtil

if __name__ == '__main__':
    print('程序开始了……')
    photoType = "21"
    photoType = "22"
    pageIndex = "1"

    blogList = [];
    categoryList = SpiderUtil.getCategoryList(photoType, pageIndex)
    for category in categoryList:
        print(category)
        # 获取该分类的所有博客列表
        blogs = SpiderUtil.getCategoryBlogs(category)
        # blogList.append(blogs)
        blogList = blogList + blogs
        print("blogList：" + str(len(blogList)))
        # if m == None:
        # for blog in blogs:
        #     print(blog)
        # break;

        # 下载图片
        num = len(blogs)
        for i in range(num):
            # print(i)
            blog = blogs[i]
            # print(blog)
            imgUrl = blog.url
            title = blog.title
            # dir = "./w2/xiannen00hou/" + title + "/"
            dir = "./w2/meituisiwa/" + title + "/"
            # 只有新的列表才创建目录
            if (i + 1 < num) and (blogs[i].title == blogs[i + 1].title):
                SpiderUtil.mkdirs(dir)
            pathname = title + "-" + str(i + 1)

            # SpiderImageUtil.downloadImage(imgUrl, dir, pathname)
            # 测试用的
            break

    print("for 循环外面-blogList：" + str(len(blogList)))



    print('\n**爬取数据成功！**')
