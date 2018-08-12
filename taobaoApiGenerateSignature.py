import time
import mysqlOperating
import configparser
import hashlib


class taobaoApiGenerateSignature(object):
    #===========================================================================
    # '''
    # 阿里API签名生成
    # '''
    #===========================================================================
    def __init__(self):
        # 阿里api调用公共参数定义
        # method: API接口名称, app_key: 应用AppKey, timestamp: 时间戳, format: 响应格式, v: API协议版本, sign_method : 签名的摘要算法, sign: API签名， secret: 应用Secret
        # dep_city_code: 出发城市, arr_city_code: 到达城市, dep_date: 航班日期, search_type: 搜索类型
        conf = configparser.ConfigParser()
        conf.read("/Users/wangjiacan/Desktop/sourceCode/configurationFile/localConfiguration.ini")

        self.method = conf.get("fliggyTicketMonitoring", "method")
        self.app_key = conf.get("fliggyTicketMonitoring", "app_key")
        self.timestamp = ''
        self.format = 'json'
        self.v = '2.0'
        self.sign_method = 'md5'
        self.sign = ''
        self.secret = conf.get("fliggyTicketMonitoring", "secret")


        self.ticketSearchUrl = 'http://gw.api.taobao.com/router/rest?method={method}&app_key={app_key}&timestamp={timestamp}&' \
                               'format={format}&v={v}&sign_method={sign_method}&sign={sign}&dep_city_code={dep_city_code}&' \
                               'arr_city_code={arr_city_code}&dep_date={dep_date}&search_type={search_type}'

    def generateSignature(self):
        # 阿里api调用业务参数定义
        # dep_city_code: 出发城市, arr_city_code: 到达城市, dep_date: 航班日期, search_type: 搜索类型
        dep_city_code = 'HGH'
        arr_city_code = 'KMG'
        dep_date = '2018-03-10'
        search_type = 'outbound'

        splicingParameters = ''

        # 获取当前时间戳
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 签名参数字典
        parameterData = {'method':self.method, 'app_key':self.app_key, 'timestamp':self.timestamp, 'format':self.format,
                         'v':self.v, 'sign_method':self.sign_method, 'dep_city_code':dep_city_code, 'arr_city_code':arr_city_code,
                         'dep_date':dep_date, 'search_type':search_type}

        # 按ASCII顺序排序参数
        sortParameters = sorted(["method", "app_key", "timestamp", "format", "v", "sign_method", "dep_city_code", "arr_city_code", "dep_date", "search_type"])

        # 拼接参数与参数值
        for parameter in sortParameters:
            splicingParameters = splicingParameters + parameter + parameterData[parameter]

        # 拼接原始签名
        originalSignature = self.secret + splicingParameters + self.secret

        # md5加密签名并生成写的十六进制
        # .swapcase():把签名中的小写字母转化成大写字母
        self.sign = hashlib.md5(originalSignature.encode(encoding='UTF-8')).hexdigest().swapcase()


if __name__ == '__main__':
    run = taobaoApiGenerateSignature()
    run.generateSignature()