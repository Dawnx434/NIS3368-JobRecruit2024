## PublishPosition模块功能说明

### 支持的URL

#### `/position/list`

返回存在的职位列表。只展示处于已发布状态的职位列表。

#### `/position/view/<position_id>`

查看id为`position_id`的岗位的详细信息。只能查看处于已发布状态的岗位的详细信息。

#### `/position/publish/`

发布新职位。只有具有HR身份的用户才可以发布职位。

#### `/position/modify/<position_id>`

修改id为`position_id`的岗位的信息。只有具有HR身份的发布者才能对岗位信息进行更改。
