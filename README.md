爬取芒果TV网页版向往的生活第三季视频弹幕信息并保存为csv文件
    
弹幕信息url(例子):# https://galaxy.bz.mgtv.com/rdbarrage?version=2.0.0&vid=5767813&abroad=0&pid=&os=&uuid=&deviceid=&cid=328724&ticket=&time=120335&mac=&platform=0&callback=jsonp_1560062961556_97065

分析思路：
    在芒果TV网页版打开第7期节目，等待广告加载完毕，同时打开chrome开发者工具的network选项卡。由于请求很多，
    而且随着时间推移，会越来越多。所以我采取了先清空再等待的方式。发现前面大多加载的都是图片，自然这不是我们的目标。
    过了一会儿之后，发现一条可疑的请求，点击一看，真的出现了弹幕内容。interval是60，猜测可能是表示一个间隔，每60s会有一个新的请求。
    于是使用filter过滤了以“rdb”开头的请求，发现这些都是弹幕，而且next都是60000的倍数，猜测表示的是60000毫秒，也就是60秒。
    
    # https://www.mgtv.com/b/328724/5767813.html
    # https://www.mgtv.com/b/328724/5683459.html
    # https://www.mgtv.com/b/328724/5768900.html

    cid: 328724这个值是不变的， 爬取不同的视频只需要更改vid: 5767813(5768900/5683459)
    爬取同一视频不同时刻的弹幕只需修改时间参数
    

    