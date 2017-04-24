# SensorTile Pocket Watch

# 开源的 SensorTile 智能怀表

使用ST SensorTile开发板做的智能怀表，可以通过

本项目的创新在于完全使用了MicroPython进行软件开发，并将SensorTile安装到了怀表中，可以实现完整的怀表功能。

使用前需要先通过接口板将MicroPython固件下载到SensorTile中，然后才可以通过MicroPython编程。因为MicroPython官方还没有支持SensorTile，所以SenSorTile的MicroPython固件需要自己移植，可以使用我移植好的，也可以自己编译源码。下载固件时，需要注意不能使用dfu方式，因为目前的dfu工具对于STM32L476存在问题，下载后的程序不完整，不能运行。目前可以通过STLink和STM32 ST-LINK Utility进行下载。

https://github.com/shaoziyang/MicroPython_firmware/tree/master/SensorTile

## 原理图

![sch](sch.jpg)

MicroPython中文社区
http://www.micropython.org.cn


