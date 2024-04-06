### 已经实现的API

|          名称          |                                                              api                                                              | 方法类型 |     参数      | 返回值data段 |
|:--------------------:|:-----------------------------------------------------------------------------------------------------------------------------:|:----:|:-----------:|:--------:|
|          注册          |                                            http://127.0.0.1:8000/api/user/sign_up/                                            | POST |             | user_id  |
|          登录          |                                             http://127.0.0.1:8000/api/user/login/                                             | POST |             | user_id  |
|          依据邮箱获取用户信息         |                                             http://127.0.0.1:8000/api/user/get_user_by_email/?email=1@1.com                                             | GET |      **需要Header中 Mytoken 设置为对应的token**       | user_id  |
|      查询当前账户的所有订单       |                                http://127.0.0.1:8000/api/user/get_tickets/?email=1                                 | GET  |      **需要Header中 Mytoken 设置为对应的token**       | user_id  |
|          退票          |                                    http://127.0.0.1:8000/api/ticket/refund/?ticket_code=1                                     | POST | ticket_code | user_id  |
|          购票          |                                            http://127.0.0.1:8000/api/ticket/book/                                             | POST |             | user_id  |
|          改签         |                                            http://127.0.0.1:8000/api/ticket/change/                                             | POST |             | user_id  |
|         添加乘客         |                                         http://127.0.0.1:8000/api/user/add_passenger/                                         | POST |             | user_id  |
| 依据起飞机场，降落机场，起飞日期查询航班 | http://127.0.0.1:8000/api/flight/get_available_flights_date/?departure_airport_id=11&arrival_airport_id=1&departure_time=2023-12-10  | GET  |  时间格式：`YYYY-MM-DD`      | user_id  |
| 依据起飞机场，降落机场，起飞**时间**查询航班 | http://127.0.0.1:8000/api/flight/get_available_flights_time/?departure_airport_id=1&arrival_airport_id=11&departure_time=2023-12-11T00:00:00+08:00  | GET  |  时间格式ISO 8601 ：`2023-12-19T16:51:00+08:00` -> `YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]`      | user_id  |
|      根据flight_id 和 cabin_class 进行票价查询      |                                http://127.0.0.1:8000/api/ticket/search/                               | POST  |             | user_id  |
|      filter 查询       |                                http://127.0.0.1:8000/api/search/select/                                | POST  |      包含查询：机场名、机型、机场地址、乘客姓名       | user_id  |
|      获取可选起飞机场       |                                http://127.0.0.1:8000/api/flight/get_airports_with_departures/                                | GET  |             | user_id  |
|      获取可选到达机场       |                                http://127.0.0.1:8000/api/flight/get_airports_with_arrivals/                              | GET  |             | user_id  |
|      用户可以管理的对象       |                                http://127.0.0.1:8000/api/validation/get_items/                            | GET  |       **需要Header中 Mytoken 设置为对应的token**      | user_id  |
|      得到当前用户提交过的申请/待审批的审核       |                                http://127.0.0.1:8000/api/validation/get_validation_list/                           | GET  |       **需要Header中 Mytoken 设置为对应的token**      | user_id  |
|          增加航班申请          |                                            http://127.0.0.1:8000/api/validation/add_flight/                                           | POST |             | user_id  |
|          增加飞机申请          |                                            http://127.0.0.1:8000/api/validation/add_aircraft/                                          | POST |             | user_id  |
|          同意申请        |                                            http://127.0.0.1:8000/api/validation/accept/                                          | POST |             | user_id  |
|          拒绝申请        |                                            http://127.0.0.1:8000/api/validation/reject/                                         | POST |             | user_id  |
|          移除机场/飞机/航班        |                                            http://127.0.0.1:8000/api/validation/remove/                                         | POST |             | user_id  |
|          获取所有乘客         |                                             http://127.0.0.1:8000/api/user/get_passengers/                                             | GET |      **需要Header中 Mytoken 设置为对应的token**       | user_id  |
|          Excel上传机场信息        |                                            http://127.0.0.1:8000/api/excel/upload_airport_data/                                        | POST |      `multipart/form-data`文件格式见示例文件       | user_id  |
|          Excel上传飞机信息        |                                            http://127.0.0.1:8000/api/excel/upload_aircraft_data/                                     | POST |      `multipart/form-data`文件格式见示例文件       | user_id  |
|          Excel上传乘客信息        |                                            http://127.0.0.1:8000/api/excel/upload_passenger_data/                                     | POST |      `multipart/form-data`文件格式见示例文件       | user_id  |
|          Excel上传航班信息        |                                            http://127.0.0.1:8000/api/excel/upload_flight_data/                                     | POST |      `multipart/form-data`文件格式见示例文件       | user_id  |
|          Excel上传机票信息        |                                            http://127.0.0.1:8000/api/excel/upload_ticket_data/                                  | POST |      `multipart/form-data`文件格式见示例文件       | user_id  |
|          得到数据统计        |                                            http://127.0.0.1:8000/api/statistics/generate_statistics/                                  | GET |      **需要携带Mytoken**，返回的为pdf文件的二进制数据流       | user_id  |




有待实现的API功能
- 无

有误的API：
- 无

注：所有 json文件请保持与 models 中的属性命名一致

示例： 
- 注册：
```json
{
   "user_password":"1",
   "user_nickname":"testt",
   "user_email":"1",
   "user_auth":"admin"
}
//返回数据示例
{
    "myStatus": true,
    "msg": "注册成功",
    "data": {
        "user_email": "1",
        "user_nickname": "testt",
        "user_auth": "admin",
        "user_tel": null,
        "user_address": null,
        "user_icon_url": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201911%2F21%2F20191121195046_fktqa.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1704274170&t=c7fb5dc3ffce688757ddfb7a3c422a1c",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMjQ5NjYzLCJpYXQiOjE3MDIyMzE2NjMsImp0aSI6IjIyZTFmNWQyMDM3NTRjNWFiMzE0NGM4YWU3MjViZTJkIiwidXNlcl9pZCI6IjEifQ.erOnFjxqq5TvPXVDwY_vaF7HNJQGAppF1EZ9sNfM6G8",
        "airport_affiliation": null,
        "airline_affiliation": null
    }
}
```

- 登录
```json
{
   "user_password":"1",
   "user_email":"1"
}
//返回数据示例
{
    "myStatus": true,
    "msg": "登录成功",
    "data": {
        "user_email": "1",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMjUwMjI2LCJpYXQiOjE3MDIyMzIyMjYsImp0aSI6IjJjNjM0NDVkZjAzNjRmNDY5OTU3ZjA2N2ExNjQwNjFjIiwidXNlcl9pZCI6IjEifQ.y6EUdItEQ6j9eHCeqnfUEMMTULiIMZLPITDs5Lu_sBE"
    }
}
```
- 依据邮箱获取用户信息(GET)
```json
{
    "myStatus": true,
    "msg": "用户信息获取成功",
    "data": {
        "user_email": "1",
        "user_nickname": "testt",
        "user_auth": "admin",
        "user_tel": null,
        "user_address": null,
        "user_icon_url": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201911%2F21%2F20191121195046_fktqa.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1704274170&t=c7fb5dc3ffce688757ddfb7a3c422a1c",
        "airport_affiliation": null,
        "airline_affiliation": null
    }
}
```
- 查询当前账户的订单（GET）
```json
{
    "myStatus": true,
    "msg": "用户信息获取成功",
    "data": [
        {
            "ticket_code": 1, // 订单编号
            "flight": {
                "flight_id": 1,
                "departure_airport": { // 起飞机场
                    "code": "1",
                    "name": "成都天府国际机场",
                    "address": "balabala",
                    "phone": null,
                    "lounge_count": 100,
                    "parking_spaces": 100,
                    "terminal_num": 3
                },
                "arrival_airport": { // 降落机场
                    "code": "11",
                    "name": "北京首都国际机场",
                    "address": "北京",
                    "phone": "1",
                    "lounge_count": 111,
                    "parking_spaces": 111,
                    "terminal_num": 11
                },
                "flight_code": "1", // 航班号
                "departure_time": "2023-12-11T09:37:43+08:00", // 起飞时间
                "arrival_time": "2023-12-11T09:37:49+08:00",
                "status": "scheduled",
                "operating_aircraft": 1
            },
            "seat_num": "1", // 座位号
            "cabin_class": "F", // 舱位
            "ticket_price": 1200, // 购票价格
            "status": "refunded",
            "passenger": "123456789"
        }
    ]
}
```

- 退票
```json
{
    "myStatus": true,
    "msg": "退票成功",
    "data": {
        "ticket_code": 1,
        "seat_num": "100",
        "cabin_class": "F",
        "ticket_price": 1200,
        "status": "refunded",
        "passenger": "1234567890",
        "flight": 1
    }
}
// -----------------------
{
    "myStatus": false,
    "msg": "订单已退票，重复退票操作",
    "data": {
        "ticket_code": "1"
    }
}
```
- 改签
```json
{
   "tar_seat_num":1,
   "tar_cabin_class":"F",
   "ori_ticket_id":"1",
   "tar_flight_id":"2"
}
// -----------------------
{
    "myStatus": true,
    "msg": "改签成功",
    "data": {
        "ticket_code": 2,
        "seat_num": "1",
        "cabin_class": "F",
        "ticket_price": 2000,
        "status": "booked",
        "passenger": "123456789",
        "flight": "2"
    }
}
```
- 购票
```json
{
   "seat_num":1,
   "cabin_class":"F",
   "ticket_price":"1200",
   "passenger_id":"1234567890",
   "flight_id":"1"
}
//返回数据示例
{
    "myStatus": true,
    "msg": "购票成功",
    "data": {
        "ticket_code": 3,
        "seat_num": "1",
        "cabin_class": "F",
        "ticket_price": 1200,
        "status": "booked",
        "passenger": "1234567890",
        "flight": "1"
    }
}
// ------------------------
{
    "myStatus": false,
    "msg": "该座位已售出，购票失败",
    "data": {
        "flight_id": "1"
    }
}
```
- 添加乘客
```json
{
  "name": "乘客姓名",
  "id_number": "123456789",
  "gender": "male",
  "age": 25,
  "phone_number": "乘客电话号码",
  "email": "乘客邮箱（可选）",
  "id_type": "身份证"
}
//返回数据示例
{
    "myStatus": true,
    "msg": "乘客添加成功",
    "data": {
        "id_number": "123456789",
        "name": "乘客姓名",
        "gender": "male",
        "age": 25,
        "phone_number": "乘客电话号码",
        "email": "乘客邮箱（可选）",
        "id_type": "身份证",
        "affiliate_user": null
    }
}
```
- 依据起飞机场，降落机场，起飞日期查询航班
```json
{
    "myStatus": true,
    "msg": "可选航班获取成功",
    "data": [
        {
            "flight_id": 1,
            "flight_code": "CA1111",
            "departure_time": "2023-12-10T08:00:00+08:00",
            "arrival_time": "2023-12-10T08:00:00+08:00",
            "status": "scheduled",
            "departure_airport": "11",
            "arrival_airport": "1",
            "operating_aircraft": 1,
            "prices": [
                {
                    "ticket_type_id": 1,
                    "ori_price": 1200,
                    "total_num": 100,
                    "available_num": 99,
                    "discount_percentage": 0,
                    "cabin_class": "F",
                    "purchased_seats": "1",
                    "flight": 1
                }
            ]
        }
    ]
}
```
- 根据flight_id 和 cabin_class 进行票价查询
```json
{
   "flight_id":1,
   "cabin_class":"F"
}
// ---------------------------
{
    "myStatus": true,
    "msg": "成功获取余票信息",
    "data": [
        {
            "ticket_type_id": 1,
            "ori_price": 1200,
            "total_num": 100,
            "available_num": 100,
            "discount_percentage": 0,
            "cabin_class": "F",
            "purchased_seats": null,
            "flight": 1
        }
    ]
}
```
- filter 查询
- flight
```json
{
   "queryObject":"flight",
   "filterObject": [
       {
           "filterLabel" : "起飞机场",
           "filterVal" : "成都"
       }
   ]
}
// ---------------------------------------
{
    "myStatus": true,
    "msg": "成功获取 flight 相关数据",
    "data": [
        {
            "flight_id": 1,
            "flight_code": "1",
            "departure_time": "2023-12-11T09:37:43+08:00",
            "arrival_time": "2023-12-11T09:37:49+08:00",
            "status": "scheduled",
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        },
        {
            "flight_id": 2,
            "flight_code": "2222",
            "departure_time": "2023-12-11T10:18:56+08:00",
            "arrival_time": "2023-12-11T10:19:00+08:00",
            "status": "scheduled",
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        }
    ]
}
```
- ticket
```json
{
   "queryObject":"ticket",
   "filterObject": [
       {
           "filterLabel" : "乘客名",
           "filterVal" : "乘客"
       }
   ]
}
// -----------------------------------
{
    "myStatus": true,
    "msg": "成功获取 ticket 相关数据",
    "data": [
        {
            "ticket_code": 1,
            "flight": {
                "flight_id": 1,
                "departure_airport": {
                    "code": "1",
                    "name": "成都天府国际机场",
                    "address": "balabala",
                    "phone": null,
                    "lounge_count": 100,
                    "parking_spaces": 100,
                    "terminal_num": 3
                },
                "arrival_airport": {
                    "code": "11",
                    "name": "北京首都国际机场",
                    "address": "北京",
                    "phone": "1",
                    "lounge_count": 111,
                    "parking_spaces": 111,
                    "terminal_num": 11
                },
                "flight_code": "1",
                "departure_time": "2023-12-11T09:37:43+08:00",
                "arrival_time": "2023-12-11T09:37:49+08:00",
                "status": "scheduled",
                "operating_aircraft": 1
            },
            "seat_num": "1",
            "cabin_class": "F",
            "ticket_price": 1200,
            "status": "refunded",
            "passenger": "123456789"
        }
    ]
}
```
- passenger
```json
{
   "queryObject":"passenger",
   "filterObject": [
       {
           "filterLabel" : "性别",
           "filterVal" : "male"
       }
   ]
}
// ---------------------------------
{
    "myStatus": true,
    "msg": "成功获取 passenger 相关数据",
    "data": [
        {
            "id_number": "123456789",
            "name": "乘客姓名A1",
            "gender": "male",
            "age": 25,
            "phone_number": "乘客电话号码",
            "email": "乘客邮箱（可选）",
            "id_type": "身份证",
            "affiliate_user": "1"
        }
    ]
}
```
- plane
```json
{
   "queryObject":"plane",
   "filterObject": [
       {
           "filterLabel" : "编号",
           "filterVal" : "1"
       }
   ]
}
// --------------------------------------
{
    "myStatus": true,
    "msg": "成功获取 plane 相关数据",
    "data": [
        {
            "aircraft_id": 1,
            "seats_num": 111,
            "age": 111,
            "aircraft_model": "111",
            "aircraft_mileage": 111,
            "WIFI_availability": true,
            "status": "1",
            "airline": 1
        }
    ]
}
```
- airport
```json
{
   "queryObject":"airport",
   "filterObject": [
       {
           "filterLabel" : "机场名",
           "filterVal" : "北京"
       }
   ]
}
// ---------------------------------
{
    "myStatus": true,
    "msg": "成功获取 airport 相关数据",
    "data": [
        {
            "code": "11",
            "name": "北京首都国际机场",
            "address": "北京",
            "phone": "1",
            "lounge_count": 111,
            "parking_spaces": 111,
            "terminal_num": 11
        }
    ]
}
```
- 获取可选起飞机场（GET）
```json
{
    "myStatus": true,
    "msg": "获取可选起飞机场成功",
    "data": [
        {
            "code": "1",
            "name": "成都天府国际机场",
            "address": "balabala",
            "phone": null,
            "lounge_count": 100,
            "parking_spaces": 100,
            "terminal_num": 3
        }
    ]
}
```
- 获取可选到达机场（GET）
```json
{
    "myStatus": true,
    "msg": "获取可选到达机场成功",
    "data": [
        {
            "code": "11",
            "name": "北京首都国际机场",
            "address": "北京",
            "phone": "1",
            "lounge_count": 111,
            "parking_spaces": 111,
            "terminal_num": 11
        }
    ]
}
```
- 用户可以管理的对象
```json
{
    "myStatus": true,
    "msg": "航空公司人员获取飞机表成功",
    "data": [
        {
            "aircraft_id": 1,
            "seats_num": 111,
            "age": 111,
            "aircraft_model": "111",
            "aircraft_mileage": 111,
            "WIFI_availability": true,
            "status": "1",
            "airline": 1
        }
    ]
}
// -------------------------------------
{
    "myStatus": true,
    "msg": "机场人员获取航班表成功",
    "data": [
        {
            "flight_id": 1,
            "flight_code": "1",
            "departure_time": "2023-12-11T09:37:43+08:00",
            "arrival_time": "2023-12-11T09:37:49+08:00",
            "status": "scheduled",
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        },
        {
            "flight_id": 2,
            "flight_code": "2222",
            "departure_time": "2023-12-11T10:18:56+08:00",
            "arrival_time": "2023-12-11T10:19:00+08:00",
            "status": "scheduled",
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        }
    ]
}
// --------------------------------
{
    "myStatus": true,
    "msg": "管理员获取机场表成功",
    "data": [
        {
            "code": "1",
            "name": "成都天府国际机场",
            "address": "balabala",
            "phone": null,
            "lounge_count": 100,
            "parking_spaces": 100,
            "terminal_num": 3
        },
        {
            "code": "11",
            "name": "北京首都国际机场",
            "address": "北京",
            "phone": "1",
            "lounge_count": 111,
            "parking_spaces": 111,
            "terminal_num": 11
        }
    ]
}
// ----------------------------------
{
    "myStatus": false,
    "msg": "无管理权限"
}
```
- 得到当前用户提交过的申请/待审批的审核
```json
{
    "myStatus": true,
    "msg": "航空公司人员获取飞机历史审核申请成功",
    "data": [
        {
            "id": 1,
            "progress": "pending",
            "seats_num": 150,
            "age": 5,
            "aircraft_model": "Boeing 737",
            "aircraft_mileage": 10000,
            "WIFI_availability": true,
            "status": "1",
            "initiator_user": "1111",
            "reviewing_user": null,
            "airline": 1
        }
    ]
}
// -----------------------------------------
{
    "myStatus": true,
    "msg": "机场人员获取航班历史审核申请成功",
    "data": [
        {
            "id": 1,
            "progress": "pending",
            "flight_code": "ABC123",
            "departure_time": "2023-01-01T12:00:00+08:00",
            "arrival_time": "2023-01-01T15:00:00+08:00",
            "status": "scheduled",
            "initiator_user": "111",
            "reviewing_user": null,
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        },
        {
            "id": 2,
            "progress": "pending",
            "flight_code": "ABC123",
            "departure_time": "2023-01-01T12:00:00+08:00",
            "arrival_time": "2023-01-01T15:00:00+08:00",
            "status": "scheduled",
            "initiator_user": "111",
            "reviewing_user": null,
            "departure_airport": "1",
            "arrival_airport": "11",
            "operating_aircraft": 1
        }
    ]
}
// ----------------------------------
{
    "myStatus": true,
    "msg": "管理员获取待审核表成功",
    "data": {
        "flight_validation_data": [
            {
                "id": 1,
                "progress": "pending",
                "flight_code": "ABC123",
                "departure_time": "2023-01-01T12:00:00+08:00",
                "arrival_time": "2023-01-01T15:00:00+08:00",
                "status": "scheduled",
                "initiator_user": "111",
                "reviewing_user": null,
                "departure_airport": "1",
                "arrival_airport": "11",
                "operating_aircraft": 1
            },
            {
                "id": 2,
                "progress": "pending",
                "flight_code": "ABC123",
                "departure_time": "2023-01-01T12:00:00+08:00",
                "arrival_time": "2023-01-01T15:00:00+08:00",
                "status": "scheduled",
                "initiator_user": "111",
                "reviewing_user": null,
                "departure_airport": "1",
                "arrival_airport": "11",
                "operating_aircraft": 1
            }
        ],
        "aircraft_validation_data": [
            {
                "id": 1,
                "progress": "pending",
                "seats_num": 150,
                "age": 5,
                "aircraft_model": "Boeing 737",
                "aircraft_mileage": 10000,
                "WIFI_availability": true,
                "status": "1",
                "initiator_user": "1111",
                "reviewing_user": null,
                "airline": 1
            }
        ]
    }
}
```
- 增加航班申请 
```json
{
  "flight_code": "ABC123",
  "departure_airport": 1,
  "departure_time": "2023-01-01T12:00:00",
  "arrival_airport": 11,
  "arrival_time": "2023-01-01T15:00:00",
  "operating_aircraft": 1
}
//------------------------------
{
    "myStatus": true,
    "msg": "航班申请数据添加成功"
}
```
- 增加飞机申请
```json
{
  "airline": 1,
  "seats_num": 150,
  "age": 5,
  "aircraft_model": "Boeing 737",
  "aircraft_mileage": 10000,
  "WIFI_availability": true
}
// --------------------------------
{
    "myStatus": true,
    "msg": "飞机申请数据添加成功"
}
```
- 同意申请
```json
{
   "object":"flight", //或者是aircraft
   "validation_id":1
}
//-------------------------------------
{
    "myStatus": true,
    "msg": "同意申请成功"
}
```
- 拒绝申请
```json
{
   "object":"flight", //或者是aircraft
   "validation_id":1
}
// -------------------------------
{
    "myStatus": true,
    "msg": "拒绝申请成功"
}
```
- 移除机场/飞机/航班
```json
{
   "removeObject":"flight",
   "num":3
}
// --------------------------------
{
    "myStatus": true,
    "msg": "删除成功"
}
```
- 获取所有乘客（GET）
```json
{
    "myStatus": true,
    "msg": "乘客表获取成功",
    "data": [
        {
            "id_number": "123456789",
            "name": "乘客姓名A1",
            "gender": "male",
            "age": 25,
            "phone_number": "乘客电话号码",
            "email": "乘客邮箱（可选）",
            "id_type": "身份证",
            "affiliate_user": "1"
        },
        {
            "id_number": "2222",
            "name": "2222",
            "gender": "female",
            "age": 22,
            "phone_number": "2222",
            "email": "2222",
            "id_type": "身份证",
            "affiliate_user": "1"
        }
    ]
}
```