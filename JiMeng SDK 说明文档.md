<span id="3c8515dd"></span>
# 前置说明（必读）
> **注：接口类型分为三类：同步接口，异步接口，同步转异步接口**

以下内容为调用SDK的通用说明，以 [通用2.1-文生图](https://www.volcengine.com/docs/86081/1804467) 为例：
**Step1:**  查看接口文档`请求参数-Query参数`中的`Action`及对应`Version`，根据Action全局检索SDK，找到对应的example或参考本文档中的调用示例<span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_4f209918c5ea3e5c6312f5113cba2036.png) </span>
**Step2:**  查看接口文档`请求参数-Body参数、请求示例`，将`请求示例`内容复制到`调用示例的body入参部分`<span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_0ac5676947a573b0e1f8c617bf584589.png) </span>
&nbsp;
**Step3:**  更新其他关键信息，比如AK/SK，然后运行程序进行调试即可
<span>![图片](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/77225aa9da5b464a8bcd79dc942cf1a6~tplv-goo7wpa0wc-image.image =1378x) </span>
**Step4:**  调通SDK示例后，再正式集成到工程中
<span id="d35c0a07"></span>
# Golang
> SDK地址：[https://github.com/volcengine/volc-sdk-golang](https://github.com/volcengine/volc-sdk-golang)

<span id="8fd5cac5"></span>
## 同步接口(直接返回结果) Action=CVProcess
<span id="fc20b3cc"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVProcess.go](https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVProcess.go)

```Go
package main

import (
        "encoding/json"
        "fmt"

        "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
        testAk := "your ak"
        testSk := "your sk"

        visual.DefaultInstance.Client.SetAccessKey(testAk)
        visual.DefaultInstance.Client.SetSecretKey(testSk)
        //visual.DefaultInstance.SetRegion("region")
        //visual.DefaultInstance.SetHost("host")

        //请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
        reqBody := map[string]interface{}{
                "req_key": ""
                // ...
        }
        
        resp, status, err := visual.DefaultInstance.CVProcess(reqBody)
        fmt.Println(status, err)
        b, _ := json.Marshal(resp)
        fmt.Println(string(b))
}
```

<span id="92c6a7a2"></span>
## 异步提交任务(返回taskId) Action=CVSubmitTask
<span id="1a1bc71b"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSubmitTask.go](https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSubmitTask.go)

```Go
package main

import (
        "encoding/json"
        "fmt"

        "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
        testAk := "your ak"
        testSk := "your sk"

        visual.DefaultInstance.Client.SetAccessKey(testAk)
        visual.DefaultInstance.Client.SetSecretKey(testSk)
        //visual.DefaultInstance.SetRegion("region")
        //visual.DefaultInstance.SetHost("host")

        //请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
        reqBody := map[string]interface{}{
                "req_key":     ""
                // ...
        }

        resp, status, err := visual.DefaultInstance.CVSubmitTask(reqBody)
        fmt.Println(status, err)
        b, _ := json.Marshal(resp)
        fmt.Println(string(b))
}
```

<span id="ee0748a4"></span>
## 异步查询任务(返回结果) Action=CVGetResult
<span id="2c116142"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVGetResult.go](https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVGetResult.go)

```Go
package main

import (
        "encoding/json"
        "fmt"

        "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
        testAk := "your ak"
        testSk := "your sk"

        visual.DefaultInstance.Client.SetAccessKey(testAk)
        visual.DefaultInstance.Client.SetSecretKey(testSk)
        //visual.DefaultInstance.SetRegion("region")
        //visual.DefaultInstance.SetHost("host")

        //请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
        reqBody := map[string]interface{}{
                "req_key": "",
                "task_id": ""
        }

        resp, status, err := visual.DefaultInstance.CVGetResult(reqBody)
        fmt.Println(status, err)
        b, _ := json.Marshal(resp)
        fmt.Println(string(b))
}
```

<span id="458df93c"></span>
## 同步转异步提交任务(返回taskId) Action=CVSync2AsyncSubmitTask
<span id="6f0a342d"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSync2AsyncSubmitTask.go](https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSync2AsyncSubmitTask.go)

```Go
package main

import (
        "encoding/json"
        "fmt"

        "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
        testAk := "your ak"
        testSk := "your sk"

        visual.DefaultInstance.Client.SetAccessKey(testAk)
        visual.DefaultInstance.Client.SetSecretKey(testSk)
        //visual.DefaultInstance.SetRegion("region")
        //visual.DefaultInstance.SetHost("host")

        //请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
        reqBody := map[string]interface{}{
                "req_key": ""
                //...
        }

        resp, status, err := visual.DefaultInstance.CVSync2AsyncSubmitTask(reqBody)
        fmt.Println(status, err)
        b, _ := json.Marshal(resp)
        fmt.Println(string(b))
}
```

<span id="88e035fe"></span>
## 同步转异步查询任务(返回结果) Action=CVSync2AsyncGetResult
<span id="94a662d5"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSync2AsyncGetResult.go](https://github.com/volcengine/volc-sdk-golang/blob/main/example/visual/CVSync2AsyncGetResult.go)

```Go
package main

import (
        "encoding/json"
        "fmt"

        "github.com/volcengine/volc-sdk-golang/service/visual"
)

func main() {
        testAk := "your ak"
        testSk := "your sk"

        visual.DefaultInstance.Client.SetAccessKey(testAk)
        visual.DefaultInstance.Client.SetSecretKey(testSk)
        //visual.DefaultInstance.SetRegion("region")
        //visual.DefaultInstance.SetHost("host")

        //请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
        reqBody := map[string]interface{}{
                "req_key": "",
                "task_id": ""
        }

        resp, status, err := visual.DefaultInstance.CVSync2AsyncGetResult(reqBody)
        fmt.Println(status, err)
        b, _ := json.Marshal(resp)
        fmt.Println(string(b))
}
```

<span id="0f05efc9"></span>
# Python
> SDK地址：[https://github.com/volcengine/volc-sdk-python](https://github.com/volcengine/volc-sdk-python)

<span id="a7bdd3fb"></span>
## 同步接口(直接返回结果) Action=CVProcess
<span id="8ce79e15"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_process.py](https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_process.py)

```Python
# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your ak')
    visual_service.set_sk('your sk')
    
    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": "xxx",
        # ...
    }

    resp = visual_service.cv_process(form)
    print(resp)
```

<span id="ce711edf"></span>
## 异步提交任务(返回taskId) Action=CVSubmitTask
<span id="657632fa"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_submit_task.py](https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_submit_task.py)

```Python
# coding:utf-8
from __future__ import print_function

from volcengine import visual
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your ak')
    visual_service.set_sk('your sk')
    
    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": "xxx",
        # ...
    }
    resp = visual_service.cv_submit_task( form)
    print(resp)
```

<span id="80ec4a47"></span>
## 异步查询任务(返回结果) Action=CVGetResult
<span id="02e99971"></span>
### 调用示例
> 示例在SDK中的路径[：https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_get_result.py](https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_get_result.py)

```Python
# coding:utf-8
from __future__ import print_function

from volcengine import visual
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your ak')
    visual_service.set_sk('your sk')
    
    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": "xxx",
        "task_id": "xxx"
    }
    resp = visual_service.cv_get_result(form)
    print(resp)
```

<span id="893aaebf"></span>
## 同步转异步提交任务(返回taskId)Action=CVSync2AsyncSubmitTask
<span id="cf31777c"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_sync2async_submit_task.py](https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_sync2async_submit_task.py)

```Python
# coding:utf-8
from __future__ import print_function

from volcengine import visual
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your ak')
    visual_service.set_sk('your ak')
    
    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": "xxx",
        # ...

    }
    resp = visual_service.cv_sync2async_submit_task(form)
    print(resp)
```

<span id="387f4ed3"></span>
## 同步转异步查询任务(返回结果)Action=CVSync2AsyncGetResult
<span id="4f281e10"></span>
### 调用示例
> 示例在SDK中的路径：[https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_sync2async_get_result.py](https://github.com/volcengine/volc-sdk-python/blob/main/volcengine/example/visual/cv_sync2async_get_result.py)

```Python
# coding:utf-8
from __future__ import print_function

from volcengine import visual
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your ak')
    visual_service.set_sk('your ak')
    
    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": "xxx",
        "task_id": "xxx",
        "req_json": "{\"logo_info\":{\"add_logo\":true，\"position\":1, \"language\":1,\"opacity\"：0.5}}"
    }
    resp = visual_service.cv_sync2async_get_result(form)
    print(resp)
```