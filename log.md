- 开启 **CSRF保护** 的前提下使用**corsheaders**和**axios**进行前后端通信。 CSRF（Cross-Site Request Forgery，跨站请求伪造）是一种Web攻击， 攻击者通过欺骗用户在已经通过身份验证的情况下执行非预期的操作。Django中的CSRF（Cross-Site Request Forgery）保护是一种防范CSRF攻击的机制。（暂时不开，开启需要在前端进行token的验证）
- 接口测试 Postman
```json
{
   "user_password":"1",
   "user_nickname":"testt",
   "user_email":"123123@qq.com",
   "user_auth":"admin"
}
```
- favicon.icon 未解决 **solved**：backEnd.urls中进行 favicon.ico 的get 方法的转发至 dist下(哈哈 又捏吗给我搞无语了 网上博客什么b玩意儿)
- 😫 对路由的理解：**/#/sign-up**显示的页面，方法为 get **/api/sign-up**提供数据传输， 方法为 post
- `@login_required` `LOGIN_URL` 
- `@permission_required`
- `@authentication_classes`
- 安全性保证：JSON Web Token（JWT），user_password加密以及不返回；导入方便的加密分支
- 报nm的错呢 ![Alt text](image.png)
- simpleJwt用不了
- 