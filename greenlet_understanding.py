
Baby_Ape
博客园首页新随笔联系订阅 管理
随笔-117  文章-0  评论-10 
Python——greenlet

目录

　　1. 介绍

　　2. 父greenlet

　　3. 实例化

　　4. 在greenlets间切换

　　5. 垂死的greenlets

　　6. greenlet的方法和属性

　　7. greenlets和Python线程

　　8. 垃圾收集活跃的greenlets

　　9. 追踪支持

　　

Introduction

一、介绍

 

　　A “greenlet” is a small independent pseudo-thread. Think about it as a small stack of frames; the outermost (bottom) frame is the initial function you called, and the innermost frame is the one in which the greenlet is currently paused. You work with greenlets by creating a number of such stacks and jumping execution between them. Jumps are never implicit: a greenlet must choose to jump to another greenlet, which will cause the former to suspend and the latter to resume where it was suspended. Jumping between greenlets is called “switching”.

　　When you create a greenlet, it gets an initially empty stack; when you first switch to it, it starts the run a specified function, which may call other functions, switch out of the greenlet, etc. When eventually the outermost function finishes its execution, the greenlet’s stack becomes empty again and the greenlet is “dead”. Greenlets can also die of an uncaught exception.

　　一个 “greenlet” 是一个小型的独立伪线程。可以把它想像成一些栈帧，栈底是初始调用的函数，而栈顶是当前greenlet的暂停位置。你使用greenlet创建一堆这样的堆栈，然后在他们之间跳转执行。跳转必须显式声明的：一个greenlet必须选择要跳转到的另一个greenlet，这会让前一个挂起，而后一个在此前挂起处恢复执行。不同greenlets之间的跳转称为切换(switching) 。

　　当你创建一个greenlet时，它得到一个开始时为空的栈；当你第一次切换到它时，它会执行指定的函数，这个函数可能会调用其他函数、切换跳出greenlet等等。当最终栈底的函数执行结束出栈时，这个greenlet的栈又变成空的，这个greenlet也就死掉了。greenlet也会因为一个未捕捉的异常死掉。

　　例如：

复制代码
>>> from greenlet import greenlet
>>>
>>> def test1():
...     print 12
...     gr2.switch()
...     print 34
...
>>> def test2():
...     print 56
...     gr1.switch()
...     print 78
...
>>> gr1 = greenlet(test1)
>>> gr2 = greenlet(test2)
>>> gr1.switch()
12
56
34
复制代码
 

　　The last line jumps to test1, which prints 12, jumps to test2, prints 56, jumps back into test1, prints 34; and then test1 finishes and gr1 dies. At this point, the execution comes back to the original gr1.switch()  call. Note that 78 is never printed.

　　最后一行首先跳转到greenlet  gr1 执行其指定的函数  test1 ，这里 test1没有参数，因此 gr1.switch() 也不需要指定参数。 test1打印12，然后跳转到  test2 ，打印56，然后跳转回   test1  ，打印34，最后  test1 结束执行， gr1 死掉。这时执行会回到最初的  gr1.switch()  调用。注意，78是不会被打印的。

 

 补充：

　　该部分关于greenlet和eventlet的介绍摘自《Python几种并发实现方案的性能比较》

　　greenlet不是一种真正的并发机制，而是在同一线程内，在不同函数的执行代码块之间切换，实施“你运行一会、我运行一会”，并且在进行切换时必须指定何时切换以及切换到哪。greenlet的接口是比较简单易用的，但是使用greenlet时的思考方式与其他并发方案存在一定区别。

　　线程/进程模型在大逻辑上通常从并发角度开始考虑，把能够并行处理的并且值得并行处理的任务分离出来，在不同的线程/进程下运行，然后考虑分离过程可能造成哪些互斥、冲突问题，将互斥的资源加锁保护来保证并发处理的正确性。

　　greenlet则是要求从避免阻塞的角度来进行开发，当出现阻塞时，就显式切换到另一段没有被阻塞的代码段执行，直到原先的阻塞状况消失以后，再人工切换回原来的代码段继续处理。因此，greenlet本质是一种合理安排了的串行，实验中greenlet方案能够得到比较好的性能表现，主要也是因为通过合理的代码执行流程切换，完全避免了死锁和阻塞等情况（执行带屏幕输出的ring_greenlet.py我们会看到脚本总是一个一个地处理消息，把一个消息在环上从头传到尾之后，再开始处理下一个消息）。因为greenlet本质是串行，因此在没有进行显式切换时，代码的其他部分是无法被执行到的，如果要避免代码长时间占用运算资源造成程序假死，那么还是要将greenlet与线程/进程机制结合使用（每个线程、进程下都可以建立多个greenlet，但是跨线程/进程时greenlet之间无法切换或通讯）。

　　粗糙来讲，greenlet是“阻塞了我就先干点儿别的，但是程序员得明确告诉greenlet能先干点儿啥以及什么时候回来”；greenlet应该是学习了Stackless的上下文切换机制，但是对底层资源没有进行适合并发的改造。并且实际上greenlet也没有必要改造底层资源的并发性，因为它本质是串行的单线程，不与其他并发模型混合使用的话是无法造成对资源的并发访问的。

　　greenlet 封装后的 eventlet 方案

　　eventlet 是基于 greenlet 实现的面向网络应用的并发处理框架，提供“线程”池、队列等与其他 Python 线程、进程模型非常相似的 api，并且提供了对 Python 发行版自带库及其他模块的超轻量并发适应性调整方法，比直接使用 greenlet 要方便得多。并且这个解决方案源自著名虚拟现实游戏“第二人生”，可以说是久经考验的新兴并发处理模型。其基本原理是调整 Python 的 socket 调用，当发生阻塞时则切换到其他 greenlet 执行，这样来保证资源的有效利用。需要注意的是：

eventlet 提供的函数只能对 Python 代码中的 socket 调用进行处理，而不能对模块的 C 语言部分的 socket 调用进行修改。对后者这类模块，仍然需要把调用模块的代码封装在 Python 标准线程调用中，之后利用 eventlet 提供的适配器实现 eventlet 与标准线程之间的协作。
再有，虽然 eventlet 把 api 封装成了非常类似标准线程库的形式，但两者的实际并发执行流程仍然有明显区别。在没有出现 I/O 阻塞时，除非显式声明，否则当前正在执行的 eventlet 永远不会把 cpu 交给其他的 eventlet，而标准线程则是无论是否出现阻塞，总是由所有线程一起争夺运行资源。所有 eventlet 对 I/O 阻塞无关的大运算量耗时操作基本没有什么帮助。
 

Parents

二、父greenlet

 

　　Let’s see where execution goes when a greenlet dies. Every greenlet has a “parent” greenlet. The parent greenlet is initially the one in which the greenlet was created (this can be changed at any time). The parent is where execution continues when a greenlet dies. This way, greenlets are organized in a tree. Top-level code that doesn’t run in a user-created greenlet runs in the implicit “main” greenlet, which is the root of the tree.

　　In the above example, both gr1 and gr2 have the main greenlet as a parent. Whenever one of them dies, the execution comes back to “main”.

　　Uncaught exceptions are propagated into the parent, too. For example, if the above test2() contained a typo, it would generate a NameError that would kill gr2, and the exception would go back directly into “main”. The traceback would show test2, but not test1. Remember, switches are not calls, but transfer of execution between parallel “stack containers”, and the “parent” defines which stack logically comes “below” the current one.

　　现在看看一个greenlet结束时执行点去哪里。每个greenlet拥有一个父greenlet。每个greenlet最初在其父greenlet中创建(不过可以在任何时候改变)。当子greenlet结束时，执行位置从父greenlet那里继续。这样，greenlets之间就被组织成一棵树，顶级的代码并不在用户创建的 greenlet 中运行，而是运行在一个主greenlet中，也就是所有greenlet关系图的树根。

　　在上面的例子中， gr1 和 gr2 都把主greenlet作为父greenlet。任何一个死掉，执行点都会回到主greenlet。

　　未捕获的异常会传递给父greenlet。如果上面的  test2 包含一个打印错误(typo)，会生成一个  NameError 而杀死 gr2 ，然后异常被传递回主greenlet。traceback会显示  test2 而不是  test1 。记住，切换不是调用，而是执行点在并行的栈容器间交换，而父greenlet定义了这些栈之间的先后关系。

 

Instantiation

三、实例化

 

 greenlet.greenlet 

　　is the greenlet type, which supports the following operations:

　　是一个 greenlet 类型，支持如下操作：

 

 greenlet(run=None, parent=None) 

　　Create a new greenlet object (without running it).  run  is the callable to invoke, and  parent  is the parent greenlet, which defaults to the current greenlet.

　　创建一个greenlet对象，不执行。run是这个greenlet要执行的回调函数，而parent是父greenlet，缺省为当前greenlet。

 

 greenlet.getcurrent() 

　　Returns the current greenlet (i.e. the one which called this function).

　　返回当前greenlet，也就是谁在调用这个函数。

 

 greenlet.GreenletExit 

　　This special exception does not propagate to the parent greenlet; it can be used to kill a single greenlet.

　　这个特定的异常不会波及到父greenlet，它用于干掉一个greenlet。

 

　　The  greenlet  type can be subclassed, too. A greenlet runs by calling its  run  attribute, which is normally set when the greenlet is created; but for subclasses it also makes sense to define a  run  method instead of giving a  run  argument to the constructor.

　　greenlet 类型可以被继承。一个greenlet通过调用其  run  属性执行，就是创建时指定的那个。对于子类，可以定义一个 run() 方法，而不必严格遵守在构造器中给出 run 参数。

 

Switching

四、在greenlets间切换

 

　　Switches between greenlets occur when the method switch() of a greenlet is called, in which case execution jumps to the greenlet whose switch() is called, or when a greenlet dies, in which case execution jumps to the parent greenlet. During a switch, an object or an exception is “sent” to the target greenlet; this can be used as a convenient way to pass information between greenlets. For example:

　　greenlet之间的切换发生在greenlet的  switch 方法被调用时，这会让执行点跳转到greenlet的  switch  被调用处。或者在greenlet死掉时，跳转到父greenlet那里去。在切换时，一个对象或异常被发送到目标greenlet。这可以作为两个greenlet之间传递信息的方便方式。

 

　　例如:

复制代码
>>> def test1(x, y):
...     z = gr2.switch(x+y)
...     print z
...
>>> def test2(u):
...     print u
...     gr1.switch(42)
...
>>> gr1 = greenlet(test1)
>>> gr2 = greenlet(test2)
>>> gr1.switch("hello", " world")
hello world
42
复制代码
 

　　This prints “hello world” and 42, with the same order of execution as the previous example. Note that the arguments of test1() and test2() are not provided when the greenlet is created, but only the first time someone switches to it.

　　Here are the precise rules for sending objects around:

　　这会打印出 “hello world” 和42，跟前面的例子的输出顺序相同。注意 test1() 和 test2() 的参数并不是在 greenlet 创建时指定的，而是在第一次切换到这里时传递的。

　　这里是精确的调用方式:

 

 g.switch(*args, **kwargs) 

　　Switches execution to the greenlet  g , sending it the given arguments. As a special case, if  g did not start yet, then it will start to run now.

　　切换到执行点greenlet  g，将这里指定的参数发送这个greenlet。在特殊情况下，如果g还没有启动，就会让它启动；

 

Dying greenlet

五、垂死的greenlet

 

　　If a greenlet’s  run()  finishes, its return value is the object sent to its parent. If  run()  terminates with an exception, the exception is propagated to its parent (unless it is a  greenlet.GreenletExit  exception, in which case the exception object is caught and returned to the parent).

　　如果一个greenlet的 run()结束了，他会返回值是返回给父greenlet的对象。如果 run()是异常终止的，异常会传播到父greenlet(除非是  greenlet.GreenletExit  异常，这种情况下异常会被捕捉并返回到父greenlet)。

 

　　Apart from the cases described above, the target greenlet normally receives the object as the return value of the call to switch() in which it was previously suspended. Indeed, although a call to switch() does not return immediately, it will still return at some point in the future, when some other greenlet switches back. When this occurs, then execution resumes just after the switch() where it was suspended, and the switch() itself appears to return the object that was just sent. This means that x = g.switch(y) will send the object y to g, and will later put the (unrelated) object that some (unrelated) greenlet passes back to us into x.

　　Note that any attempt to switch to a dead greenlet actually goes to the dead greenlet’s parent, or its parent’s parent, and so on. (The final parent is the “main” greenlet, which is never dead.)

　　除了上面的情况外，目标greenlet会接收到发送来的对象作为 switch() 的返回值。虽然 switch() 并不会立即返回，但是它仍然会在未来某一点上返回，当其他greenlet切换回来时。当这发生时，执行点恢复到 switch() 之后，而 switch() 返回刚才调用者发送来的对象。这意味着 x=g.switch(y) 会发送对象y到g，然后等着一个不知道是谁发来的对象，并在这里返回给x。

　　注意，任何尝试切换到死掉的greenlet的行为都会切换到死掉greenlet的父greenlet，或者父greenlet的父greenlet，等等。最终的父greenlet就是main greenlet，main greenlet永远不会死掉的。

 

Methods and attributes of greenlets

六、greenlet的方法和属性

 

 g.switch(*args, **kwargs) 

　　Switches execution to the greenlet  g .

　　切换执行点到greenlet  g。

 

 g.run 

　　The callable that  g will run when it starts. After  g started, this attribute no longer exists.

　　调用可执行的g，并启动。在g启动后，这个属性就不再存在了。

 

 g.parent 

　　The parent greenlet. This is writeable, but it is not allowed to create cycles of parents.

　　greenlet的父greenlet。这是可写的，但是不允许创建循环的父关系。

 

 g.gr_frame 

　　The current top frame, or None.

　　当前顶级帧，或者None。

 

 g.dead 

　　True if  g  is dead (i.e. it finished its execution).

　　判断greenlet是否已经死掉了。

 

 bool(g) 

　　True if  g is active, False if it is dead or not yet started.

　　如果g是活跃的则返回True，在尚未启动或者结束后返回False。

 

 g.throw([typ, [val, [tb]]]) 

　　Switches execution to the greenlet  g, but immediately raises the given exception in  g. If no argument is provided, the exception defaults to  greenlet.GreenletExit . The normal exception propagation rules apply, as described above. Note that calling this method is almost equivalent to the following:

　　切换执行点到greenlet  g ，但是立即在g中抛出指定的异常。如果没有提供参数，异常缺省就是  greenlet.GreenletExit 。异常传播规则如上文描述。注意调用这个方法等同于如下:

 

def raiser():
    raise typ, val, tb
g_raiser = greenlet(raiser, parent=g)
g_raiser.switch()
　　except that this trick does not work for the  greenlet.GreenletExit  exception, which would not propagate from  g_raiser  to  g .

　　注意这一招对于异常 greenlet.GreenletExit并不适用，因为这个异常不会从 g_raiser 传播到 g 。

 

greenlets and python 

七、greenlets和Python线程

 

　　Greenlets can be combined with Python threads; in this case, each thread contains an independent “main” greenlet with a tree of sub-greenlets. It is not possible to mix or switch between greenlets belonging to different threads.

　　greenlets可以与Python线程一起使用；在这种情况下，每个线程包含一个独立的 main greenlet，并拥有自己的greenlet树。不同线程之间不可以互相切换greenlet。

 

Garbage-collecting live greenlets

八、垃圾收集活跃的greenlets


　　If all the references to a greenlet object go away (including the references from the parent attribute of other greenlets), then there is no way to ever switch back to this greenlet. In this case, a GreenletExit exception is generated into the greenlet. This is the only case where a greenlet receives the execution asynchronously. This gives try:finally: blocks a chance to clean up resources held by the greenlet. This feature also enables a programming style in which greenlets are infinite loops waiting for data and processing it. Such loops are automatically interrupted when the last reference to the greenlet goes away.

　　The greenlet is expected to either die or be resurrected by having a new reference to it stored somewhere; just catching and ignoring the GreenletExit is likely to lead to an infinite loop.

　　Greenlets do not participate in garbage collection; cycles involving data that is present in a greenlet’s frames will not be detected. Storing references to other greenlets cyclically may lead to leaks.

　　如果不再有对greenlet对象的引用时(包括其他greenlet的parent)，还是没有办法切换回greenlet。这种情况下会生成一个 GreenletExit 异常到greenlet。这是greenlet收到异步异常的唯一情况。应该给出一个 try .. finally 用于清理greenlet内的资源。这个功能同时允许greenlet中无限循环的编程风格。这样循环可以在最后一个引用消失时自动中断。

　　如果不希望greenlet死掉或者把引用放到别处，只需要捕捉和忽略 GreenletExit 异常即可。

　　greenlet不参与垃圾收集；greenlet帧的循环引用数据会被检测到。将引用传递到其他的循环greenlet会引起内存泄露。

 

Tracing support

九、追踪支持


　　Standard Python tracing and profiling doesn’t work as expected when used with greenlet since stack and frame switching happens on the same Python thread. It is difficult to detect greenlet switching reliably with conventional methods, so to improve support for debugging, tracing and profiling greenlet based code there are new functions in the greenlet module:

 

 greenlet.gettrace() 
　　Returns a previously set tracing function, or None.

 

 greenlet.settrace(callback) 

　　Sets a new tracing function and returns a previous tracing function, or None. The callback is called on various events and is expected to have the following signature:

 

复制代码
def callback(event, args):
    if event == 'switch':
        origin, target = args
        # Handle a switch from origin to target.
        # Note that callback is running in the context of target
        # greenlet and any exceptions will be passed as if
        # target.throw() was used instead of a switch.
        return
    if event == 'throw':
        origin, target = args
        # Handle a throw from origin to target.
        # Note that callback is running in the context of target
        # greenlet and any exceptions will replace the original, as
        # if target.throw() was used with the replacing exception.
        return
复制代码
　　For compatibility it is very important to unpack args tuple only when event is either 'switch' or 'throw' and not when event is potentially something else. This way API can be extended to new events similar to sys.settrace().

 

标签: python, greenlet


最新评论
1. Re:（原）数据结构——线索二叉树
  ，我的这篇更详细
--刘毅（Limer）
2. Re:（原）数据结构——线索二叉树
求C++完整代码    数据结构作业题目是 根据用户输入的先序遍历和中序遍历构建一个二叉树，并将此二叉树进行后序遍历，打印出来，并把二叉树打印出来
求大神帮帮忙  在线等，很急！谢谢
--计算机菜鸟一只
3. Re:（原）数据结构——线索二叉树
如何根据用户输入的先序遍历和中序遍历构建一个二叉树    求C++代码
--计算机菜鸟一只
4. Re:使用openstackclient调用Keystone v3 API
好文章，收益匪浅
--doscho
5. Re:Python——eventlet
“多次孵化绿色线程会并行地执行任务”，不应该是并发的执行吗？
--彭玉松
阅读排行榜
1. Python——eventlet(4382)
2. Linux系统排查2——CPU负载篇(3993)
3. Python装饰器、metaclass、abc模块学习笔记(3652)
4. （原创）Python字符串系列（1）——str对象(3644)
5. （实用）Linux下安装JDK和Eclipse(2696)
评论排行榜
1. （原创）OpenStack服务如何使用Keystone (二)---部署和配置Keystone中间件(3)
2. （原）数据结构——线索二叉树(3)
3. Python——eventlet(1)
4. 使用openstackclient调用Keystone v3 API(1)
5. Juno 版 Keystone 主配置文件 keystone.conf 详解(1)
推荐排行榜
1. （实用）Linux下安装JDK和Eclipse(1)
2. Ubuntu 14.04 安装 DevStack与遇到的的问题记录(1)
3. Python——hashlib(1)
4. 使用OpenSSL创建自己的CA root certificate(1)
5. Linux系统排查4——网络篇(1)
Copyright ©2017 王智愚
