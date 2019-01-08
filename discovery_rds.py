#coding=UTF-8
#Auther：xwjr.com
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
import json

ID = 'ID'
Secret = 'Secret'
RegionId = 'cn-shenzhen'

clt = client.AcsClient(ID,Secret,RegionId)

DBInstanceIdList = []
DBInstanceIdDict = {}
ZabbixDataDict = {}
def GetRdsList():
    RdsRequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    RdsRequest.set_accept_format('json')
    RdsRequest.set_PageSize(100)   # 每页实例条数
    RdsRequest.set_PageNumber(1)    # 第几页
    #RdsInfo = clt.do_action(RdsRequest)
    RdsInfo = clt.do_action_with_exception(RdsRequest)
    for RdsInfoJson in (json.loads(RdsInfo))['Items']['DBInstance']:
        DBInstanceIdDict = {}
        try:
            if 'prod' in RdsInfoJson['DBInstanceDescription']: # 筛选别名里带 prod 字符的
                DBInstanceIdDict["{#DBINSTANCEID}"] = RdsInfoJson['DBInstanceId']
                DBInstanceIdDict["{#DBINSTANCEDESCRIPTION}"] = RdsInfoJson['DBInstanceDescription']
                DBInstanceIdList.append(DBInstanceIdDict)
        except Exception, e:
            print Exception, ":", e
            print "Please check the RDS alias !Alias must not be the same as DBInstanceId！！！"
            


GetRdsList()
ZabbixDataDict['data'] = DBInstanceIdList
print json.dumps(ZabbixDataDict)
