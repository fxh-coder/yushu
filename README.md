# python flask

## 学习python，很重要的一点就是一定要明白其中的循环导入问题！！！
   解决办法：1. 放到最后导入
            2. 哪里使用哪里导入

## 注册视图的两种方法
1. @app.route('/hello)
   def hello():
       return 'hello world'
2. app.add_url_rule('/hello', view_func=hello)

## 指定端口号和ip
   app.run(host='0.0.0.0', port=81)

## 配置文件的读取与使用
1. 读取
   app.config.from_object('config')
   config是一个py文件，注意与项目的路径关系
2. 使用
   app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)
   也就是app.config['name']

## python自带的json与flask的jsonify
   自带的：return json.dumps(result), 200, {'content-type':'application/json'}
   
   flask的jsonify：return jsonify(result)
   
### json.dumps(books, default=lambda o: o.__dict__) 可已将非字典型数据转 化传给前端页面使用

## 自己指定静态文件夹的位置
   在app文件夹下的__init__.py文件里
   app = Flask(__name__, static_folder='路径')
   路径是相对路径，相对于应用程序根目录，也就是__name__
   所指向的目录，这里是app

## 访问系统默认的静态文件夹，是放在app文件夹里面的
   原因是：app = Flask(__name__) __name__决定的

## 模板语言使用的是flask官方推荐的jinja2
   1. 使用的基础样例是：{{ data }}
   2. 对于对象或者字典的数据，使用语法是：{{ data.age }} 或者 {{ data['age'] }}
   3. 在模板里面进行注释的语法是：{# data #}
   4. 简单的流程控制语句的语法是：{% if %} 或者 {% for ... in ... %}
      但是这个语句的使用必须要闭合，即 {% endif %} {% endfor %}
   5. jinja2使用和java的thymeleaf相似，可以定义一个基础模板
      {% block head %}
        <div>this is head</div>
      {% endblock %}
      由于基础模板里面有最基本的html标签，所以使用基础模板的其他html就不用
      这些元素标签了，就像html，head，body这些
   6. 使用基础模板的html要有{% extends 'layout.html' %}指明要使用哪个
      并且使用{% block name %} 指明要将数据填充到哪个块下面
   7. 如果原本的基础模板里面的块下面写的有文本，你不仅想要将数据填充到对应
      区域，还想要原本的文本也显示，就可以在对应文件里使用{% super() %}
## jinja2里面的过滤器
   1. default这个是用来判断对象或者字典里面某个属性是否存在，不存在就会
      使用default里面的自定义数据
   2. { data | length() } 这个可以求长度

## 为了避免应用开发与上线之后静态文件比如css路径问题，反向构建url
   href="{{ url_for('static, filename='test.css') }}"
   
## flask的消息闪现flash，使用这个需要配置secret_key
   1. flash('hello', 'fxh')，可以多次调用
      模板接收：{% set messages = get_flashed_messages() %}
               {{ messages }}
   2. 消息闪现可以指定分类
      flash('hello', category='error')
      flash('fxh', category='warning')
      模板接收：{% with errors = get_flashed_messages(category_filter=["error"]) %}  .... {% endwith %} 一般都是这样 end... 闭合 set不用
      with指定了作用域，即接收到的消息只能在闭合标签之内使用

## flask用到的模板注释方法，不能用原来的html注释方法，一定要用{# #}进行注释

## 对于模板里面的form请求，由于search是挂载在蓝图上的，不在应用程序上，所以要用url_for=(web.search)，统一写在action里面

## 使用python的lambda表达式和filter处理可能为空的数据
   使用lambda表达式，如果有值为空，表达式返回False，就会被从数组中剔除
   filter(lambda  x: True if x else False,
                        [self.author, self.publisher, self.price])

## 两个模型之间的关联使用relationship('User'), 外键绑定uid = Column(Integer, ForeignKey('user.id'))

## 如果只是想创建一个基类，不想创建对应的表，就使用__abstract__ = True

## 如果不想使用类名作为表名，可以：__tablename__ = 'name', 也可以Column('name') 改写字段名


## from werkzeug.security import generate_password_hash 不是 from werkzeug import generate_password_hash

## 使用login_user的问题，Missing user_loader or request_loader.
   解决： 在app的__init__.py文件里
      @login_manager.user_loader
      def load_user(userid):
         return User.get(userid)

## 快速定义对象的方法
   from collections import namedtuple
   EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])

   使用方法：
      count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
      w 是元组
      
## 使用flask-mail的基本方法
   import flask_mail import Message
   msg = Message('测试邮件', sender='xxxx@qq.com',
               body='测试邮件的内容', recipients=['xxxx@qq.com','xssss@qq.com'])
   mail.send(msg)
