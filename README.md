## 前言

貌似替代方法一大堆？但我就想自己写。

如你所见，这是一个汇集**编译**、**运行**、**测大样例**、**对拍**等功能为一体的集大成OI工具（不过只支持 windows）

## 功能介绍

先说明一下个工具的功能：

1. 编译代码，编译指令是从洛谷改的，有默认 std=c++14 和 std=c++17 的两个版本
2. 可以看到显示**运行时间**、**内存**和返回值，较为美观（可能吧。。。）
3. **自动测大样例**
4. **自动对拍**
5. 在本地编译时对源代码进行一些处理，如去掉 freopen，添加 ```#define LOCAL``` 等，修改通过创建一个 process.cpp 进行，不会直接修改源代码
6. 本地测样例的时候用的临时文件输入输出（不改代码，而是在运行的时候使用管道传输）
7. 非常舒服的文件管理（写这个的主要原因）
8. 即使在控制台输入输出，快读模板也不用改，输入样例的时间也不算在运行时间里

## 文件管理

文件夹的组织结构是这样：

1. 源代码可以随便放
2. 样例、special judge 的 checker、对拍的 std 和 sol 都放到 test/ 目录下
3. 编译完的文件放在 bin/ 目录下

## 使用方法

包含很多的子应用

### compile

用于编译源代码（默认开 -O2 和 -g 选项，栈空间设为 512MB，其他选项和洛谷保持一致），在编译的时候会自动去掉代码中的 freopen，自动在第一行加一个 ```#define LOCAL``` ，使用时这样调用：

``` powershell
mars-oi compile [源代码路径（不要.cpp）]
# 例如：
mars-oi compile P1000         # 会编译当前目录的 P1000.cpp　文件
mars-oi compile match/abc/A   # 会编译 match/abc/A.cpp 文件
# 使用 -f 或 --with-freopen 指定不去掉 freopen 编译
mars-oi compile -f match/abc/B   # 即使存在 freopen 也不去掉，适用于一些神奇题目，如 P10397
```

### run

用于运行代码，可以指定文件输入输出。

* 注意：如果要用控制台输入输出，输入用空行表示结束，这里脚本实际上会把控制台的输入保存到 test/input.txt ，输出保存到 test/output.txt ，所以不应该使用这两个文件保存任何需要保持的数据

对于普通的运行，可以这样调用，会自动运行上一次编译的代码，如果 RE 给出返回值，默认如果运行超过 5 秒直接结束给出 TLE，否则给出运行输出、时间和内存占用：

* 注意：给出 TLE 后很有可能由于神奇的原因无法正确结束进程，导致以后编译报错，此时可以用资源管理器直接结束进程，还有有时候 RE 会变成 TLE，windows 的锅

``` powershell
mars-oi run
```

如果要加文件输入输出，可以这样调用：

``` powershell
mars-oi run -i [inputfile] -o [outputfile]
# 不加读入或不加输出也是可以的，会自动加上test/的目录名和.in/.out的扩展名，例如：

mars-oi run -i bargain -o bargain
# 读入 test/bargain.in 输出 test/bargain.out

mars-oi run -i bargain
# 读入 test/bargain.in 输出到控制台

mars-oi run -o bargain
# 读入控制台 输出到 test/bargain.out

mars-oi run -i bargain -o
# 特殊用法：out后不接任何东西会输出到 test/output.txt
```

如果是 RE 或 TLE 很有可能无法正常的看到出错前输出的内容，这种情况下使用 ```-c``` 或 ```--console``` 解决

```powershell
mars-oi run -c  # 这样即使 RE 或 TLE 也可以看到出错前输出的内容了
```

如果是一些运行时间比较长的毒瘤题，可以使用 ```-t``` 或 ```--timeout``` 指定超时的时长

```powershell
mars-oi run -t 10000   # 这样运行 10s 才会爆出 TLE （注意指定的时间不要爆 long long 哦）
```

### test

测大样例

* 超过 5 秒给出 TLE，但是 ```-t``` 和 ```-timeout``` 仍然有效。
* 默认的比较使用 fc.exe，使用 -c check 可以使用 test/check.exe 进行 check，调用格式为 ```test/check.exe <input-file> <output-file> <ans-file>```

``` powershell
mars-oi test [样例名的共同前缀]
# 例如：
mars-oi test bargain
# 会在 test/ 目录下匹配以 bargain 开头的后缀为 .in/.out/.ans 的文件
# 如 bargain1.in bargain1.ans bargain2.in bargain2.ans 等。
# 自动执行文件输入输出，代码中无需 freopen（即使加了 freopen 也会在编译的时候自动去掉）
# 可以识别到AC和WA和RE，并给出相应的颜色
# WA的时候会给出差异，RE的时候会给出返回值
# 可以看到时间和内存消耗。
# 执行完后给出分数（100 * AC测试点 / 所有测试点）
```

### check

对拍

* ```-c check``` 的使用与 test 相同

```powershell
mars-oi check
# 默认会编译 test/gen.cpp 和 test/sol.cpp 作为生成和正解
```
