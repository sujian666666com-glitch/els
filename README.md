# 俄罗斯方块游戏 - Web版本

这是一个基于HTML5、CSS3和JavaScript开发的俄罗斯方块游戏，可以直接在浏览器中运行。

## 文件说明

- `index.html` - 游戏主页面
- `tetris.css` - 游戏样式文件
- `tetris.js` - 游戏逻辑文件
- `tetris.py` - Python桌面版本（需要pygame）

## 本地运行

1. 直接双击 `index.html` 文件，在浏览器中打开即可
2. 或者使用本地服务器：
   ```bash
   # 使用Python
   python -m http.server 8000
   
   # 使用Node.js
   npx http-server
   ```
3. 在浏览器中访问 `http://localhost:8000`

## 部署到域名

### 方法一：使用静态网站托管服务

1. **GitHub Pages**
   - 创建GitHub仓库
   - 上传 `index.html`、`tetris.css`、`tetris.js` 文件
   - 在仓库设置中启用GitHub Pages
   - 通过 `https://yourname.github.io/repo-name` 访问

2. **Vercel**
   - 安装Vercel CLI: `npm i -g vercel`
   - 在项目目录运行: `vercel`
   - 按提示完成部署

3. **Netlify**
   - 访问 [netlify.com](https://www.netlify.com)
   - 拖拽项目文件夹到网站即可部署

### 方法二：使用自己的服务器

1. **使用Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           root /path/to/game;
           index index.html;
       }
   }
   ```

2. **使用Apache**
   ```apache
   <VirtualHost *:80>
       ServerName yourdomain.com
       DocumentRoot /path/to/game
       
       <Directory /path/to/game>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

3. **使用云服务器（阿里云/腾讯云等）**
   - 将文件上传到服务器
   - 配置Web服务器（Nginx/Apache）
   - 绑定域名

## 游戏功能

- 三种难度选择（简单、中等、困难）
- 最高分记录（保存在浏览器本地存储）
- 下一个方块预览
- 游戏结束提示
- 响应式设计，支持移动端

## 操作说明

- **← →**：左右移动
- **↑**：旋转方块
- **↓**：加速下落
- **空格**：直接落到底部
- **ESC**：返回菜单

## 技术栈

- HTML5 Canvas
- CSS3（渐变、动画、响应式）
- JavaScript（ES6+）
- LocalStorage（本地数据存储）

## 浏览器兼容性

支持所有现代浏览器：
- Chrome/Edge 60+
- Firefox 55+
- Safari 11+
- Opera 47+
