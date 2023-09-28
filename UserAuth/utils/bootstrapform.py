class BootStrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环每个字段为其插件进行设置
        for name, field in self.fields.items():
            # 字段中有属性，则增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入" + field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    # 还可以添加其他的标签，例如placeholder
                    "placeholder": field.label
                }