# design

## 表项

### 地图

| 属性      | 描述                     | 类型     |
| --------- | ------------------------ | -------- |
| id        | 主键                     | INT      |
| user_id   | 所属用户的外键           | INT      |
| zoom      | 地图信息，缩放等级       | INT      |
| view_mode | 地图信息，2d/3d模式      | TINYINT  |
| center_x  | 地图信息，中心点坐标 x值 | DOUBLE   |
| center_y  | 地图信息，中心点坐标 y值 | DOUBLE   |
| style     | 风格信息                 | LONGBLOB |

### marker

| 属性       | 描述           | 类型   |
| ---------- | -------------- | ------ |
| id         | 主键           | INT    |
| graph_id   | 所属地图外键   | INT    |
| position_x | 位置信息 x坐标 | DOUBLE |
| position_y | 位置信息 y坐标 | DOUBLE |
| account    | 账目           | DOUBLE |

### 日记

| 属性      | 描述             | 类型         |
| --------- | ---------------- | ------------ |
| id        | 主键             | INT          |
| marker_id | 锚定的marker外键 | INT          |
| title     | 标题             | VARCHAR(255) |
| abstract  | 摘要             | TEXT         |
| content   | 内容             | LONGBLOB     |

### Path

| 属性          | 描述         | 类型   |
| ------------- | ------------ | ------ |
| id            | 主键         | INT    |
| graph_id      | 所属地图外键 | INT    |
| origin_x      | 起点x        | DOUBLE |
| origin_y      | 起点y        | DOUBLE |
| destination_x | 起点x        | DOUBLE |
| destination_y | 起点y        | DOUBLE |

## api

### 地图api

#### 获取

- 行为：根据用户id返回ta的全部地图信息
- 请求方式：GET
- 地址：/getGraphes
- 参数：userId（一串数字），**如果有鉴权手段就不用传参数**
- 返回: data中装对象数组如下，长度为0表示没有地图

  ```json
    {
        "success": true,
        "msg": "地图获取成功",
        "data": {
            "graphes": [
                {
                    "id": <string>,//地图id
                    "zoom": <number>,//地图缩放等级
                    "viewMode": <number>,//视图模式2D还是3D
                    "center": [<number>, <number>],//中心点坐标
                    "style": <string>//地图风格数据，未设计部分，确定后原样返回，暂时字符串
                },
                {
                    ...
                },
                ...
            ]
        }
    }
    //失败
    {
        "success": false,
        "msg": "找不到用户",
        "data": {}
    }

    {
        "success": false,
        "msg": "未知异常",
        "data": {}
    }
  ```

#### 修改仅地图信息

- 行为：根据地图id修改地图数据，出于效率考虑，没有对应地图id会直接新建（但是不建议用这个直接新建）
- 请求方式：POST
- 地址：/modifyGraphy
- 请求体：

  ```json
    {
        "data": {
            //"userId": <string>,//用户id，能通过其它方式鉴权区分用户则省去此条目
            "id": <string>,//地图id
            "zoom": <number>,//地图缩放等级
            "viewMode": <number>,//视图模式2D(0)还是3D(1)
            "center": [<number>, <number>],//中心点坐标
            "style": <string>//地图风格数据，未设计部分，确定后原样返回，暂时字符串
        }
    }
  ```
- 返回:

  ```json
  {
      "succes": true,
      "msg": "地图修改成功",
      "data": {}
  }
  //失败
  {
      "success": false,
      "msg": "没有这个地图，已经新建",
      "data": {
          "id": <string>,//新建的地图id
      }
  }

  {
      "success": false,
      "msg": "找不到用户",
      "data": {}
  }

  {
      "success": false,
      "msg": "用户权限错误",//无法修改别人的id
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

#### 添加新地图

- 行为：添加新地图，并返回新建地图的id
- 请求方式：POST
- 地址：/addGraphy
- 请求体：

  ```json
    {
        "data": {
            //"userId": <string>,//用户id，能通过其它方式鉴权区分用户则省去此条目
            "zoom": <number>,//地图缩放等级
            "viewMode": <number>,//视图模式2D(0)还是3D(1)
            "center": [<number>, <number>],//中心点坐标
            "style": <string>,//地图风格数据，未设计部分，确定后原样返回，暂时字符串
        }
    }
  ```
- 返回:

  ```json
  {
      "succes": true,
      "msg": "地图修改成功",
      "data": {
          "id": <string>//新建的地图id
      }
  }

  //失败
  {
      "success": false,
      "msg": "找不到用户",
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

#### 删除地图

- 行为：根据地图id删除对应地图
- 请求方式：GET
- 地址：/deleteGraph
- 参数：graphId, userId(有鉴权就不要userId)
- 返回：

  ```json
  {
      "succes": true,
      "msg": "地图删除成功",
      "data": {}
  }
  //失败
  {
      "success": false,
      "msg": "没有这个地图，删除失败",
      "data": {}
  }

  {
      "success": false,
      "msg": "找不到用户",
      "data": {}
  }

  {
      "success": false,
      "msg": "用户权限错误",//无法删除别人的地图
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

### marker api

#### 获取地图上所有marker

- 行为：根据地图id获取所有marker信息
- 请求方式：GET
- 地址：/getMarkers
- 参数：graphId
- 返回：markers长度为0就是没有

  ```json
  {
      "success": true,
      "msg": "marker获取成功",
      "data": {
          "markers": [
              {
                  "id": <string>,//marker id
                  "position": [<number>, <number>],//中心点坐标
                  "account": <number>//没记录就是0
              },
              {
                  ...
              },
              ...
          ]
      }
  }

  //失败
  {
      "success": false,
      "msg": "没有对应的地图",
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

#### 修改marker位置，账目

- 行为：根据graph id, marker id修改marker信息，没有则新建并返回marker id
- 请求方式：POST
- 地址：/modifyMarker
- 请求体：

  ```json
  {
      "data": {
          "id": <string>,//marker id
          "graphId": <string>,//地图id
          "position": [<number>, <number>],//中心点坐标
          "account": <number>//没记录就是0
      }  
  }
  ```
- 返回：

  ```json
  {
      "success": true,
      "meg": "修改marker信息成功",
      "data": {}
  }
  //失败
  {
      "success": false,
      "msg": "没有对应的marker，已经新建",
      "data": {
          "id": <string>//marker id
      }
  }

  {
      "success": false,
      "msg": "没有对应的地图",
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

#### 添加marker

- 行为：根据graph id添加新marker，并返回新marker id
- 请求方式：POST
- 地址：/addMarker
- 请求体：

  ```json
  {
      "data": {
          "graphId": <string>,//地图id
          "position": [<number>, <number>],//中心点坐标
          "account": <number>//没记录就是0
      }  
  }
  ```
- 返回：

  ```json
  {
      "success": true,
      "meg": "添加marker信息成功",
      "data": {
          "id": <string>//marker id
      }
  }
  //失败
  {
      "success": false,
      "msg": "没有对应的地图",
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

#### 删除marker

- 行为：根据graph id, marker id删除marker
- 请求方式：GET
- 参数：graphId, markerId
- 返回：

  ```json
  {
      "success": true,
      "meg": "删除marker信息成功",
      "data": {}
  }
  //失败
  {
      "success": false,
      "msg": "没有对应的marker",
      "data": {}
  }

  {
      "success": false,
      "msg": "没有对应的地图",
      "data": {}
  }

  {
      "success": false,
      "msg": "未知异常",
      "data": {}
  }
  ```

### 日记api

socket
