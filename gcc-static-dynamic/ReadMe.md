## 静态链接和动态链接

链接命令
```shell
g++ -o main main.o -Lmydir/ -ltarget
```

+ 当同一路径下既存在 libtarget.a 和 libtarget.so 时，默认链接的是动态库
+ 可以使用 `-static` 参数来指定使用静态库

```shell
g++ -static -o main main.o -Lmydir/ -ltarget
```
