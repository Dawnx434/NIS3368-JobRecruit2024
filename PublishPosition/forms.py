from django import forms

class PublishPositionForm(forms.Form):
    salary_min = forms.DecimalField(required=False, label="最低薪资")
    salary_max = forms.DecimalField(required=False, label="最高薪资")
    job_type = forms.ChoiceField(choices=[
        ('full_time', '全职'),
        ('part_time', '兼职'),
        ('internship', '实习'),
        # 其他岗位类型可以继续添加
    ], required=False, label="岗位类型")
    location = forms.CharField(max_length=100, required=False, label="岗位地点")
    education_requirements = forms.CharField(max_length=100, required=False, label="学历要求")
