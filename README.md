# 失心王游戏

黑化的国王打算杀死另外3位国王。扮演黑桃K，消灭另外三个K以获胜。

## 游戏规则

1. **游戏开始**：玩家拥有黑桃K和另外4张随机牌（共5张手牌）
2. **敌人**：翻开牌堆顶的4张牌作为敌人
3. **攻击规则**：
   - 玩家需用手上的牌结合四则运算计算出对面的其中一个点数
   - J、Q、K视为11、12、13
   - 大王的点数始终视为另外三张牌里最大的一个（无论在敌人一侧还是在己方）
   - 小王视为最小
   - **除黑桃K之外的牌必须全部用到，黑桃K可用可不用**
4. **战斗流程**：
   - 每战胜一个敌人，玩家需要：
     - 抛弃4张手牌之一（不能丢弃黑桃K）
     - 将刚刚消灭的敌人加入手牌
     - 翻开新的牌直到有4个敌人
5. **胜利条件**：消灭其余3个K（红心K、方块K、梅花K）即为胜利

## 运行方法

### 命令行版本

```bash
python main.py
```

### 网页版本

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动Flask服务器：
```bash
python app.py
```

3. 在浏览器中打开：
```
http://localhost:5000
```

## 游戏操作

1. 查看当前手牌和敌人牌
2. 选择要攻击的敌人（输入敌人编号）
3. 如果可以用手牌计算出敌人的点数，游戏会显示解决方案
4. 确认攻击后，选择要丢弃的手牌
5. 重复以上步骤，直到击败所有三个K

## 文件说明

- `card.py`: 扑克牌类定义，处理点数计算（包括JQK和大小王）
- `solver.py`: 四则运算求解器，找到能用给定牌计算出目标值的方法
- `game.py`: 游戏主逻辑，管理游戏状态和流程
- `main.py`: 主程序入口，提供命令行用户交互界面
- `app.py`: Flask Web应用，提供网页版游戏API
- `streamlit_app.py`: Streamlit Web应用，可用于部署到 Streamlit Community Cloud
- `templates/index.html`: Flask版本网页游戏前端HTML
- `static/style.css`: Flask版本网页游戏样式
- `static/script.js`: Flask版本网页游戏前端逻辑
- `requirements.txt`: Python依赖包列表
- `.streamlit/config.toml`: Streamlit配置文件

## 技术实现

- 使用递归算法求解四则运算组合
- 支持大小王的动态点数计算（根据上下文确定）
- 完整的游戏状态管理和流程控制

## 在线部署

### 使用Streamlit Community Cloud部署（推荐）

Streamlit Community Cloud 是部署 Streamlit 应用最简单的方式，完全免费！

1. **准备代码**：
   - 确保项目已推送到 GitHub 仓库
   - 确保 `streamlit_app.py` 文件存在（已创建）

2. **部署步骤**：
   - 访问 [Streamlit Community Cloud](https://streamlit.io/)
   - 使用 GitHub 账号登录
   - 点击 "Deploy an app"
   - 选择你的 GitHub 仓库
   - 选择分支（通常是 `main` 或 `master`）
   - 设置主文件路径为 `streamlit_app.py`
   - 点击 "Deploy"

3. **访问应用**：
   - 部署完成后，你会得到一个类似 `https://your-app-name.streamlit.app` 的链接
   - 应用会自动部署，每次推送到 GitHub 都会自动更新

**本地运行 Streamlit 版本**：
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### 使用Docker部署

1. 构建Docker镜像：
```bash
docker build -t heartbreaker .
```

2. 运行容器：
```bash
docker run -p 5000:5000 heartbreaker
```

3. 访问应用：
```
http://localhost:5000
```

### 使用Heroku部署

1. 安装Heroku CLI并登录
2. 创建Heroku应用：
```bash
heroku create your-app-name
```

3. 部署：
```bash
git push heroku master
```

4. 打开应用：
```bash
heroku open
```

### 使用Gunicorn本地运行（生产模式）

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 使用Gunicorn运行：
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 120 app:app
```

### 环境变量配置

可以通过环境变量配置应用：

- `FLASK_DEBUG`: 是否启用调试模式（默认：False）
- `HOST`: 绑定主机（默认：0.0.0.0）
- `PORT`: 监听端口（默认：5000）

示例：
```bash
export FLASK_DEBUG=False
export PORT=8080
python app.py
```

