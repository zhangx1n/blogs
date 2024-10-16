[TorchMetrics：PyTorch的指标度量库_ronghuaiyang的博客-CSDN博客](https://blog.csdn.net/u011984148/article/details/115541306)

虽然TorchMetrics被构建为与原生的PyTorch一起使用，但TorchMetrics与Lightning一起使用提供了额外的好处：

- 当在LightningModule中正确定义模块metrics 时，模块metrics会自动放置在正确的设备上。这意味着你的数据将始终与你的metrics 放在相同的设备上。
- 在Lightning中支持使用原生的`self.log`，Lightning会根据`on_step` 和`on_epoch`标志来记录metric，如果`on_epoch=True`，logger 会在epoch结束的时候自动调用`.compute()`。
- metric 的`.reset()`方法的度量在一个epoch结束后自动被调用。