# MessagePassing Class in PyTorch Geometric

## Message Passing GNN 的泛式

![image-20211208211243269](https://cdn.jsdelivr.net/gh/Zhangxin98/Note@main/img/202112082112436.png)



- xi(k−1)∈RF表示神经网络的(k−1)层中节点i的节点表征
- ej,i∈RD 表示从节点j到节点i的边的属性信息。
- ◻表示**可微分**的、具有排列不变性（**函数输出结果与输入参数的排列无关**）的函数, 比如aggregation 函数。比如sum， mean, min等函数和输入的参数顺序无关的函数。
- γ : **可微分可导**的update 函数，比如MLPs（多层感知器）
- ϕ: **可微分可导**的message 函数，比如MLPs（多层感知器）和 linear Projection等
- **Note:**
    1. 神经网络的生成节点表征的操作称为节点嵌入（Node Embedding），节点表征也可以称为节点嵌入。**这里考虑节点嵌入只代指神经网络生成节点表征的操作**。
    2. 未经过训练的图神经网络生成的节点表征还不是好的节点表征，好的节点表征可用于衡量节点之间的相似性。通过监督学习对图神经网络做很好的训练，图神经网络才可以生成好的节点表征。我们将在[第5节](https://notebooks.githubusercontent.com/view/5-基于图神经网络的节点表征学习.md)介绍此部分内容。
    3. 节点表征与节点属性的区分：遵循被广泛使用的约定，此次组队学习我们也约定，节点属性`data.x`是节点的第0层(GNN输入层)节点表征，第h层的节点表征经过一次的节点间信息传递产生第h+1层的节点表征。不过，节点属性不单指`data.x`，广义上它就指节点的属性，如节点的度(in-degree, out-degree)等。

## MessagePassing 的Base Class 函数

Pytorch Geometric(PyG)提供了MessagePassing基类，它封装了“消息传递”的运行流程。通过继承MessagePassing基类，可以方便地构造消息传递图神经网络。构造一个最简单的消息传递图神经网络类，我们只需定义message()方法（ 𝜙(..) ）、update()方法（ 𝛾(..) ），以及使用的消息聚合方案（aggr=”add”、aggr=”mean”或aggr=”max”。**MessagePassing Base Class中这里最重要的3个函数是：**

- `MessagePassing.aggregate(...)`：用于处理聚集到节点的信息的函数
- `MessagePassing.message(...)`：用于搭建传送到 node i的节点消息，相对于𝜙(..)函数
- `MessagePassing.update(aggr_out, ...)`: 用于更新节点的信息，相对于𝛾(..)

**以下是一些常用函数的解释:**

- `MessagePassing(aggr="add", flow="source_to_target", node_dim=-2)`:
    - `aggr`: aggregation function聚合函数的选项, 可以用 (“add”, “mean” or “max”)
    - `flow`: 信息传递方向 (either “source_to_target” or “target_to_source”)
    - `node_dim`：定义沿着哪个维度传播，默认值为-2，也就是节点表征张量（data.x, Tensor）的哪一个维度是节点维度。节点表征张量x形状为[num_nodes, num_features]，其第0维度/columns（也是第-2维度）是节点维度(节点的个数)，其第1维度（也是第-1维度）是节点表征维度，所以我们可以设置node_dim=-2。
- `MessagePassing.propagate(edge_index, size=None, **kwargs)`:
    - `edge_index`: 一个matrix存放每条edge 的索引信息(起始和终止的node的index)
    - `size`: 基于非对称的邻接矩阵进行消息传递（当图为二部图时），需要传递参数size=(N, M)。如果size=None, 默认邻接矩阵是对称的
    - `**kwargs`：图的其他特征
- `MessagePassing.message(...)`：
    - 首先确定要给节点$i$传递消息的边的集合：
        - 如果`flow="source_to_target"`，则是$(j,i)∈E$的边的集合；
        - 如果`flow="target_to_source"`，则是$(i,j)∈E$的边的集合。
    - 接着为各条边创建要传递给节点ii的消息，即实现$ϕ$函数。
    - `MessagePassing.message(...)`方法可以接收传递给`MessagePassing.propagate(edge_index, size=None, **kwargs)`方法的所有参数，我们在`message()`方法的参数列表里定义要接收的参数，例如我们要接收`x,y,z`参数，则我们应定义`message(x,y,z)`方法。
    - 传递给`propagate()`方法的参数，如果是节点的属性的话，可以被拆分成属于中心节点的部分和属于邻接节点的部分，只需在变量名后面加上`_i`或`_j`。例如，我们自己定义的`meassage`方法包含参数`x_i`，那么首先`propagate()`方法将节点表征拆分成中心节点表征和邻接节点表征，接着`propagate()`方法调用`message`方法并传递中心节点表征给参数`x_i`。而如果我们自己定义的`meassage`方法包含参数`x_j`，那么`propagate()`方法会传递邻接节点表征给参数`x_j`。
    - 我们用ii表示“消息传递”中的中心节点，用jj表示“消息传递”中的邻接节点。
- `MessagePassing.aggregate(...)`：
    - 将从源节点传递过来的消息聚合在目标节点上，一般可选的聚合方式有`sum`, `mean`和`max`。
- `MessagePassing.message_and_aggregate(...)`：
    - 在一些场景里，邻接节点信息变换和邻接节点信息聚合这两项操作可以融合在一起，那么我们可以在此方法里定义这两项操作，从而让程序运行更加高效。
- `MessagePassing.update(aggr_out, ...)`:
    - 为每个节点i∈Vi∈V更新节点表征，即实现γγ函数。此方法以`aggregate`方法的输出为第一个参数，并接收所有传递给`propagate()`方法的参数。

## MessagePassing 的Base Class 函数

### propagate 函数的输入

propagate 函数的输入 有edge_index, x (node embedding matrix), 以及其他自定义的输入参数(degree, norm之类的)。其中edge_index的储存形式如下

$$Edgeindex = \begin{matrix}[[0&0&1&4]\\\ [0&1&4&1]]\end{matrix}$$

其中Edge_index的shape = [2, amount of edge]. Edge_index[0]第一行是source node的index， Edge_index[1]第二行是target node的index.

**Note**

1. 如果edge_index 用 torch tensor来储存，那么propagate函数会分别调用message, aggregate的函数
2. 如果edge_index 用 torch_sparse的SparseTensor类来储存，那么propagate函数会调用message_and_aggregate的函数而不是两个单独的函数
3. 当edge_index, x(node embedding)输入到propagate后，它会自动通过 __collect__()函数 把输入解析得到以下参数:
    - 如果self.flow=”source_to_target”:
        - **x_i**: edge_index的target node的index列表(edge_index[1])对应的node embedding向量列表。
            比如 edge_index的target node列表是 edge_index[1], length = E, 而node embedding的维度为dim, 那么 x_i =x[edge_index[1]]是edge_index[1]所对应的embedding列表， x_i的shape= [E, dim]。
            举个例子就是 target node 的索引列表是 edge_index[1] = [0, 1, 2]而 E=3, dim=2, 那么 x_i = [[0.5,0.6],[0.1,0.22],[0.2,0.3]]。x_i里面的每一行分别对应target node 0, 1,2的node embedding向量
        - **deg_i**: edge_index的target node的index列表对应的degree列表。这个和x_i同理
        - **x_j**：edge_index的source node的edge_index[0]列表对应的node embedding向量列表。
        - **deg_j**: edge_index的source node的edge_index[0]列表对应的degree列表。这个和x_j同理
    - **如果flow=”target_to_source” 那么有_ i后缀代表source, _ j后缀代表target node**
4. 在得到target node的edge_index和 对应的source node的node embedding vectors之后，我们就可以把每个target node对应的所有node embedding向量聚合一起得到target node的信息集合用于搭建 message了

### message函数的输入

message 函数输入一般包括: x_i, x_j, deg_i, deg_j, edge_index以及其他自定义的参数输入

### aggregate函数的输入

aggregate 函数输入除了有 **inputs (来自message函数的输入)** 外 一般还包括: inputs, x_i, x_j, deg_i, deg_j, edge_index以及其他自定义的参数输入。

### message_and_aggregate 函数的输入

message_and_aggregate 函数输入 一般还包括: x_i, x_j, deg_i, deg_j, edge_index以及其他自定义的参数输入。

### update 函数的输入

update 函数输入包括inputs以及其他自定义的参数输入。

