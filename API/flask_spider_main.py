#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Time    : 2018-03-04 19:22
# @Author  : huifer
# @File    : flask_spider_main.py
# @Software: PyCharm
from flask import Flask, render_template, request
from db.SqliteClient import SqliteClient
from spider.IpSpider import IpSpider

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/getip/type/<type>/page/<page>")
def get_ip(type, page):
    print(type, page)
    ipspider = IpSpider(urltype=int(type))
    ip_list = ipspider.run_spider(page=int(page))
    res = ipspider.ip_insert_sql(ip_list)
    if res:
        return "插入数据成功"
    else:
        return "插入数据失败"


@app.route("/search", methods=['GET', 'POST'])
def search():
    a = SqliteClient().search_table_sqlite()
    ip = []
    port = []
    type = []
    downtime = []
    for x in a:
        ip.append(x[0])
        port.append(x[1])
        type.append(x[2])
        downtime.append(x[4])

    date = {
        'ip': ip,
        'port': port,
        'type': type,
        'downtime': downtime,
    }
    return render_template("search.html",
                           ip=ip,
                           port=port,
                           type=type,
                           downtime=downtime,
                           date=date)


@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        # port=8111,

    )
