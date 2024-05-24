export default {
    mobile: [
        {required: true, message: '请输入手机号', trigger: "blur"},
        {pattern: /^1[34578]\d{9}$/, message: '请输入正确的手机号', trigger: "blur"}
    ],
    phone: [
        {required: true, message: '请输入电话号码', trigger: "blur"},
        {pattern: /^(\d{3,4}-?)?\d{7,8}$|^1[34578]\d{9}$/, message: '请输入正确的电话号码', trigger: "blur"}
    ],
    email: [
        {required: true, message: '请输入邮箱地址', trigger: "blur"},
        {pattern:/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/, message: '请输入正确的邮箱地址', trigger: "blur"}
    ],
    idNumber: [
        {required: true, message: '请输入身份证号', trigger: "blur"},
        {pattern: /^[A-Za-z\d]{18,20}$/, message: '请输入正确的身份证号', trigger: "blur"}
    ],
    captcha: [
        {required: true, message: '请输入验证码', trigger: "blur"},
        {pattern: /^[A-Za-z\d]{4}$/, message: '请输入正确的验证码', trigger: "blur"}
    ],
    verifyCode: [
        {required: true, message: '请输入验证码', trigger: "blur"},
        {pattern: /^\d{4}$/, message: '请输入正确的验证码', trigger: "blur"}
    ],
    password: [
        {required: true, message: '请输入密码', trigger: "blur"},
        {pattern: /^.{6,16}$/, message: '请输入6-16位密码', trigger: "blur"},
        {pattern: /^([A-Za-z\d]|[`\-=[\]\\;',./~!@#$%^&*()_+{}|:"<>?])+$/, message: '请输入英文字母、数字或英文符号', trigger: "blur"}
    ],
    fullName: [
        {required: true, message: '请填写', trigger: "blur"},
        {pattern: /^[_0-9a-zA-Z\u3400-\u4DB5\u4E00-\u9FA5\u9FA6-\u9FBB\uF900-\uFA2D\uFA30-\uFA6A\uFA70-\uFAD9]{1,8}$/, message: '请输入汉字数字或英文字母', trigger: "blur"}
    ],
    name: [
        {required: true, message: '请填写名称', trigger: "blur"},
        {pattern: /^[_0-9a-zA-Z\u3400-\u4DB5\u4E00-\u9FA5\u9FA6-\u9FBB\uF900-\uFA2D\uFA30-\uFA6A\uFA70-\uFAD9]{1,30}$/, message: '请输入汉字数字或英文字母', trigger: "blur"}
    ],
    address: [
        {required: true, message: '请填写地址', trigger: "blur"}
    ],
    repeatPwd(compareTo) {
        return [
            {required: true, message: '请输入密码'},
            {
                validator: (rule, value, callback)=>{
                    let target = this;
                    let keys = compareTo.split('.');
                    keys.forEach((key)=>{
                        target = target[key];
                    });
                    if (target != value) {
                        callback(new Error('两次输入不一致'));
                    } else {
                        callback();
                    }
                }, trigger: 'blur'
            }
        ]
    },
    price: [
        {required: true, message: '请填写价格', trigger: "blur"},
        {pattern: /^\d{1,5}(\.\d{1,2})?$/, message: '请输入整数或2位小数，整数部分最多5位', trigger: "blur"}
    ],
    score: [
        {required: true, message: '请填写降分分数', trigger: "blur"},
        {pattern: /^\d{1}(\.\d{1})?$/, message: '请输入整数或1位小数，整数部分最多1位', trigger: "blur"}
    ]
}