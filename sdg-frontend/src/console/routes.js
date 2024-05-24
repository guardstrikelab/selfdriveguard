export default [
    {
        path: '/mine/basic',          // 我的 - 基本信息
        component: () => import('./mine/BasicInfo')
    },
    {
        path: '/mine/resetPwd',           // 我的 - 修改密码
        component: () => import('./mine/ResetPwd')
    },

    {
        path: '/op/scene/list',
        component: () => import('./operate/scene/List')
    },
    {
        path: '/op/scene/edit',
        component: () => import('./operate/scene/Edit')
    },
    {
        path: '/op/task/list',
        component: () => import('./operate/task/List')
    },
    {
        path: '/op/task/edit',
        component: () => import('./operate/task/Edit')
    },
    {
        path: '/op/job/list',
        component: () => import('./operate/job/List')
    },
    {
        path: '/op/job/edit',
        component: () => import('./operate/job/Edit')
    },
    {
        path: '/mushroom_order',   // 蘑菇 - 目
        component: () => import('./mushroom/order/List')
    },
    {
        path: '/family',   // 蘑菇 - 科
        component: () => import('./mushroom/family/List')
    },
    {
        path: '/genus',   // 蘑菇 - 属
        component: () => import('./mushroom/genus/List')
    },
    {
        path: '/mushroom',   // 蘑菇 - 种
        component: () => import('./mushroom/mushroom/List')
    },
    {
        path: '/customer',      // 客户 - 客户
        component: () => import('./customer/customer/List')
    },
    {
        path: '/serve_order',   // 客户 - 服务订单
        component: () => import('./customer/serve/List')
    },
    {
        path: '/pay_order',   // 客户 - 支付订单
        component: () => import('./customer/pay/List')
    },
    {
        path: '/agent',      // 代理 - 代理
        component: () => import('./agent/agent/List')
    },
    {
        path: '/withdraw',      // 代理 - 提现记录
        component: () => import('./agent/withdraw/List')
    }
];
