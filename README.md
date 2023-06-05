# flybird
使用pygame实现的一个复古小游戏

# pygame的使用
sys中用到用来退出游戏的函数
```python
import pygame,sys
```
# 初始化主窗口
```python
size = width, height = 600,600    #窗口大小
screen = pygame.display.set_mode(size)
pygame.display.set_caption("flybird")
```
# 游戏机制

设计机制是游戏处于一个循环体内，不断刷新窗口内的像素位置，形成动画。以下循环展示了进入游戏的初始界面，首先是第一个for循环内的pygame.event.get()，所有的监听器处于这个消息队列中，每次循环都对其进行一次遍历。在我们的游戏中一个是要监听游戏关闭事件pygame.QUIT，另一个就是鼠标点击事件pygame.MOUSEBUTTONDOWN，通过返回鼠标的点击位置来判断是否开始游戏，或是对游戏内小鸟的控制。
```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        exit()          #游戏的退出
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            loc = pygame.mouse.get_pos()
            if (loc[0] > width / 2 -90) and (loc[0] < width / 2 +90) and (loc[1] > height / 2 -80) and (loc [1] < height / 2 +80):
                start_fly(screen #进入start_fly表示进入开始游戏之后的循环体
```

# 设计思路

这个项目没有使用任何的图片素材，因此游戏画面内所有的元素由pygame.draw模块绘制完成，并且为了达到这种像素风，仅仅使用了pygame.draw.rect来完成基本矩形的绘制。以下谈到的像素均为自己定义的像素，而非实际像素。

游戏画面采取的是笛卡尔坐标系，以窗口左上角为坐标原点，x轴正方向往屏幕右侧，y轴正方向往屏幕下侧。

- class Pixel: 像素类，用来对定义的像素点做基本的绘制，移动操作。
  ```python3
  import pygame
  class Pixel:
      """游戏内容均为像素点,实质上为固定大小的矩形"""
      scale = 0,0
      location = 0,0
      color = 0,0,0
      #构造方法 需要的参数有像素的长宽，起始位置，颜色，均由元组表示。
      def __init__(self, scale , location, color):
          self.scale = scale
          self.location = location
          self.color = color

      def move(self,target):
          self.location = target

      def ncolor(self,color):
          self.color = color

      def draw(self,screen):
          pygame.draw.rect(screen,self.color,(self.location,self.scale))
  ```
- class element: 这个类通过使用class Pixel:的实例化对象来绘制获得游戏内容。通过改变成员变量 shift[ x, y] 的值来控制图像外接矩形左上角的坐标，改变 speed[ x, y] 来控制图像在x轴及y轴上的平移速度。而该类提供了 move(location) 和 setSpeed(speed) 两个成员方法来改变上述两个量。图片的绘制信息位于 build_BIRD，build_CLOUD ，build_SWITCH ，build_OBSTACLE， LETTER几个变量中。
  ```python
  import pygame
  from pixel import Pixel
  class Element:
      pixelScale = [0,0]
      #此处的长宽代表像素点的个数
      scale = [0,0]
      mes = []
      shifting = [0,0]
      speed = [1,1]
  #构造方法，传入欲绘制图像的像素点长宽（元组），整个图像外接矩形的长宽（元组），图片的绘制信息格式为((x,y),color)，以此类元组形成的列表传入构造函数
      def __init__(self,pixelScale,scale,mes):
          self.pixelScale = pixelScale
          self.scale = scale
          self.mes = mes
  #将图像绘制到指定的surface对象上
      def draw(self,screen):
          for _ in range(len(self.mes)):
              location = [(self.mes[_][0][0]-1) * self.pixelScale[0] + self.shifting[0], (self.mes[_][0][1]) * self.pixelScale[1] + self.shifting[1]]
              color = self.mes[_][1]
              pixel = Pixel(self.pixelScale,location,color)
              pixel.draw(screen)

      def move(self,location):
          self.shifting = location

      def setSpeed(self,speed):
          self.speed = speed
  ```
## 构造
- 开始按钮：
  ```python
  switch = Element((10, 10),(13, 18), build_SWITCH)
  switch.move((width / 2 - 90,height / 2 - 80))
  ```
- 小鸟
  ```python
  # 鸟
  bird = Element((3, 3), (11, 17), build_BIRD)
  bird.move((size[0] / 2 - 60, size[1] / 4))
  bird.draw(screen)
  bird.speed = [0,0]
  ```
- 云
  ```python
  cloud_1 = Element((5, 5), (15, 19), build_CLOUD)
  cloud_1.move((size[0] / 6, size[1] / 5))
  cloud_1.setSpeed((-0.7, 0))

  cloud_2 = Element((7, 7), (15, 19), build_CLOUD)
  cloud_2.move((size[0] / 1.2, size[1] / 3))
  cloud_2.setSpeed((-1.5, 0))

  cloud_3 = Element((10, 10), (15, 19), build_CLOUD)
  cloud_3.move((size[0] / 2, size[1] / 1.5))
  cloud_3.setSpeed((-2, 0))
  ```
- 障碍物
  ```python
  obstacle_1_1 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_1_1.move((size[0], -size[1] / 3.5))
  obstacle_1_2 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_1_2.move((size[0], 1.3*size[1] - obstacle_1_2.scale[0]*obstacle_1_2.pixelScale[0]))

  obstacle_2_1 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_2_1.move((size[0] *1.4 , -size[1] / 3.5))
  obstacle_2_2 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_2_2.move((size[0] *1.4, 1.3*size[1] - obstacle_2_2.scale[0]*obstacle_2_2.pixelScale[0]))

  obstacle_3_1 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_3_1.move((size[0] *1.7 , -size[1] / 3.5))
  obstacle_3_2 = Element((5, 5), (75, 21), build_OBSTACLE)
  obstacle_3_2.move((size[0] *1.7, 1.3*size[1] - obstacle_3_2.scale[0]*obstacle_3_2.pixelScale[0]))
  ```
- 分数
  score 用来存储当前分数，游戏结束的时候返回游戏分数这个参数至主界面并显示
  ```python
  #每过一个障碍物加一分，显示分数
  score_ten = Element( (10,10),(5,5), LETTER[ int (score / 10) ] )
  score_one = Element( (10,10),(5,5), LETTER[ score % 10] )
  score_ten.move((10,0))
  score_one.move((60,0))
  score_ten.draw(screen)
  score_one.draw(screen)
  ```
# 游戏元素的动画
所有的游戏动画均为平移，因此使用 class Element: 里的 move(location) 和 setSpeed(speed) 足以完成所有的动画效果。小鸟处于确定x坐标的竖直区域运动，云和障碍物不断的左移即可。

## 开始游戏
在遍历消息队列中。
```python
if pygame.mouse.get_pressed()[0]:
	loc = pygame.mouse.get_pos()
                 #开始新游戏
       if (loc[0] > width / 2 - 90) and (loc[0] < width / 2 + 90) and (loc[1] > height / 2 - 80) and (loc[1] < height / 2 + 80):
       	score = start_fly(screen)
```

## 云的左移
```python
def cloud_animation(cloud):
#若云的整体位置已越过窗口左侧，设置云的外接矩形左上角位于窗口最右侧。
    if cloud.shifting[0] < - (cloud.scale[1] * cloud.pixelScale[1]):
        cloud.move((size[0], cloud.shifting[1]))
    cloud.move(( cloud.shifting[0] + cloud.speed[0], cloud.shifting[1] ))
    cloud.draw(screen)
```

## 小鸟的向下匀加速直线运动
```python
bird.move((bird.shifting[0], bird.shifting[1] + bird.speed[1]))
bird.speed[1] += 1
bird.draw(screen)
```
监听鼠标右键点击事件对小鸟提供极大的瞬时向上的加速度，达到缓冲小鸟下落的效果，在遍历消息队列中。
```python
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pressed()
        if mouse[2]:
bird.speed[1] -= 25
```
## 障碍物的移动以及判断小鸟是否与障碍物相撞
（由于一开始游戏难度过大， 我将障碍物设置为空心，即小鸟不会和障碍物的正下方或正上方相撞，但会和障碍物的侧边相撞）
通过传入一定范围内的随机参数ran控制障碍物从最右端开始向左平移的初始位置。在每个障碍物对象经过小鸟的位置令分数+1，便可完成分数的记录。
```python
def obstacle_animation(obstacle,ran,bird_height):
    if obstacle.shifting[0] < - (obstacle.scale[1] * obstacle.pixelScale[1]):
        obstacle.move((size[0], obstacle.shifting[1] + ran * (obstacle.scale[1] * obstacle.pixelScale[1]) ))
    obstacle.move(( obstacle.shifting[0] - 1, obstacle.shifting[1] ))
    obstacle.draw(screen)
    if (obstacle.shifting[0] < size[0] / 2) and (obstacle.shifting[0] > size[0] / 2 - 60):   #可能发生碰撞的矩形区域
        if obstacle.shifting[1] < 0:  #和上管道相撞的区域
            if obstacle.shifting[1] + 375 >= bird_height: #和上管道右侧相撞的区域
                if obstacle.shifting[0] < size[0] / 2:
                    return True
                else: return False
            elif obstacle.shifting[0] < size[0] / 2:
                if obstacle.shifting[1] + 375 >=bird_height:
                    return  True
                else: return False
        elif obstacle.shifting[1] < bird_height:
            if obstacle.shifting[0] < size[0] / 2:
                return True
            else: return False
        elif obstacle.shifting[0] < size[0] / 2:
            if obstacle.shifting[1] < bird_height:
                return True
            else: return False
```

# 打包
(已安装pyinstaller)
在命令行窗口，进入到游戏入口文件的路径下输入命令
```shell
pyinstaller -w -F 文件名.py 文件名.py...
```
打包完成之后可执行文件处于dist目录下。
