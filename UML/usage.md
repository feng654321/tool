**UML类图**

类图描述系统中类的静态结构，它不仅定义系统中的类，描述类之间的联系，如关联、依赖、聚合等，还包括类的内部结构（类的属性和操作）。

  

类图描述的是静态关系，在系统的整个生命周期中都是有效的。

  

对象图是类图的实例，它们的不同之处在于对象图显示类图的多个对象实例，而不是实际的类。由于对象存在生命周期，所以对象图只能在系统某一时间存在。

  

**UML基本图示法**

虚线箭头指向依赖；

实线箭头指向关联；

虚线三角指向接口；

实线三角指向父类；

空心菱形能分离而独立存在，是聚合；

实心菱形精密关联不可分，是组合；

  

**![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It9PwDf4wb2fcGNKbttYzYJFgsibJPmpGXk0KDnbqibZiaJlnCRIREkwYWw/640?wx_fmt=png)**  

上面是UML的语法，在画类图的时候，清理类和类之间的关系是重点。

  

类的关系有泛化(Generalization)、实现（Realization）、依赖(Dependency)和关联(Association)。

  

其中关联又分为一般关联关系和聚合关系(Aggregation)，合成关系(Composition)。

  

**基本概念**

  

类图（Class Diagram）：类图是面向对象系统建模中最常见和最重要的图，是定义其他图的基础。

  

类图的主要是用来显示系统中的类、接口以及它们之间的静态结构和关系的一种静态模型。

  

类图的3个基本组件：类名、属性、方法。

  

**详细解析**

  

注：下面图片实例中的代码为C#代码，非Java代码！

  

继承关系

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It1YeJxnJcgoUcY7Oia3H5icJQ6mo9kOxUesZaT5yk5DtOf3hBAP7cE22A/640?wx_fmt=png)

  

首先看到上图这个“动物”矩形框，它就代表一个类（Class）。

  

类图分三层

第一层显示类的名称，如果是抽象类，则就用斜体显示。

第二层是类的特性，通常就是字段和属性。

第三层是类的操作，通常是方法或行为。

  

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It4icat5o3AH9HAEia8V4FWY2L7JEzpfhGs5ichuBHeI7JQmBAAPibGul7rA/640?wx_fmt=png)

  

在看到上图中的“飞翔”，它表示一个接口图，与类图的区别主要是顶端有<<interface>>显示。

  

第一行是接口名称，第二行是接口方法。

  

接口还有另一种表示方法，俗称棒棒糖表示法，就是唐老鸭类实现了“讲人话”的接口。

  

鸭子本来也有语言，只不过只有唐老鸭是能讲人话的鸭子。

  

注意动物、鸟、鸭、唐老鸭之间的关系符号，你就会发现它们都是继承的关系。

  

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3Itx6ibRonU1J8ricRzlqbic2KfpJOkeqmUMCRG8WQVziaWFhOAKWIY1KkoeQ/640?wx_fmt=png)

  

继承关系用空心三角形+实现来表示。

  

这里列举的几种鸟中，大雁是最能飞的，我让它实现了飞翔接口。

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3Itj6xe3gRFHmhIa6iaqXHS64d6JuWibFXyqTRUox6jPD07ZgibLzwTrF4qg/640?wx_fmt=png)  

  

实现接口用空心三角形+虚线来表示。

  

在看下图中企鹅和气候两个类，企鹅是很特别的鸟，会游不会飞。更重要的是，它与气候有很大的关联。我们不去讨论为什么北极没有企鹅，为什么它们要每年长途跋涉。

  

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It27NUf3rj5fxDOJkNjfdh0qGsmVkB8PDHkIKp6NFSojib7B7UnvgAdDw/640?wx_fmt=png)  

  

总之，企鹅需要“知道”气候的变化，需要“了解”气候规律。

  

当一个类“知道”另一个类时，可以用关联（association）。

  

关联关系用实现箭头来表示。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/TeYk478W36Ba9cUE7U4f1yJOrEDGA3ItHxVz4ia6qMvNV5Uicib8Gib9SxVOndqZJYYeKbctBIWAI4ZElt6ialPPadg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It53ibr3B3D3P9XPJeXZDowiarzWIH105Z0fkAMnu8zpUdddy4ChHawnWw/640?wx_fmt=jpeg)

我们再来看上图中大眼与雁群这两个类，大雁是群居动物，每只大雁都属于一个雁群，一个雁群可以又很多只大雁。

  

所以它们之间就满足聚合（Aggregation）关系。

  

**聚合表示一种弱的“拥有”关系，体现的是A对象可以包含B对象，但B对象不是A对象的一部分。**

  

聚合关系用实心的菱形+实线箭头来表示。

  

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3ItXMYJmibSiaoHHw7HUA0wWQvBmXTTBxtkBjQo4iazOGCEBkhbufyAiavhXA/640?wx_fmt=png)

  

合成（Composition，也有翻译成“组合”的）是一种强的“拥有”关系，体现了严格的部分和整体的关系，部分和整体的声明周期一样。

  

在这里鸟和其翅膀就是合成（组合）关系，因为它们是部分和整体的关系，并且翅膀和鸟的声明周期是相同的。

  

合成关系用实心的菱形+实现箭头来表示。

  

另外，你会注意到合成关系的连线两端还有一个数字“1”和数字“2”，这被称为基数。表明这一段的类可以有几个实例，很显然，一个鸟应该有两只翅膀。

  

如果一个类可能有无数个实例，则就用“n”来表示。关联关系、聚合关系也可以有基数的。

  

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It8Nv3SSzF6V7aviaicbdiatyEWCd3dJYQ4ngD1768DLib0h73Pria50Kick2w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/TeYk478W36Ba9cUE7U4f1yJOrEDGA3It2S254Bbvib6fDO2fCxBic66geSokrWW5PYAbX6DplJmZaNDEr1FgTYIQ/640?wx_fmt=png)

  

动物几大特征，比如有新陈代谢，能繁殖。而动物要有生命力，需要氧气、水以及食物等。也就是说，动物依赖于氧气和水。

  

他们之间是依赖关系（Dependency），用虚线箭头来表示。

  
