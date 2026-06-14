## importの仕方
importとは、簡潔に言えば、外部のツールや処理を取り込むことである。

理論上はimportというのが無くてもプログラミングはできるが、実務的には不可欠と言ってよく、責務の分離に強く関わる。

### ライブラリのimport

初心者が目にすることが多いimportはライブラリのimportである。<br>
ライブラリとは、狭義のパッケージあるいはモジュールあるいはバイナリとそのラッパーのことであるが、そこの区別をしなくても済むように(しなくてもいい場合が多いため)ライブラリという用語が使われることが多い。<br>
(このあとパッケージとモジュールの違いについて説明する。)

ライブラリのimportの実務的な意味としては、「標準のそのプログラミング言語にはない機能を提供する」というものである。

例えば、プログラミング言語をデフォルトで高機能にしすぎると使わない機能も読み込んで動作が重くなる。<br>
また、プログラミング言語の開発者ではない人が「こういう機能を作ったから他の人にも使えるようにしたいな」と思うこともある。

こういう場合にプログラミング言語の標準外の機能をライブラリとして公開して、その中で欲しいものを各人が取り込んで使えるようにする処理が`import`である。

下のはPythonのimportの最もシンプルな例である。下の`requests`, `pandas`, `pathlib`の3つのライブラリはそれぞれAPI, データ処理, パスの処理に用いるライブラリである。

```python
import requests
import pandas as pd # pandasパッケージはこのファイルではpdとして表記される
from pathlib import Path
```
`requests`, `pandas`はパッケージである。<br>
一方で`pathlib`ライブラリに関してはパッケージではなくモジュールである。`Pathlib`モジュールのうち`Path`クラスのみを`import`している。

`import`の最も基本的な使い方はライブラリ全体を`import`するか、`from`を使ってライブラリ内の特定のクラスや関数を`import`するやり方である。

### パッケージ(`dir/`)→モジュール(`.py`)→関数, クラス(`function()`, `Class`)

自分で作成したコード（パッケージやモジュール）を`import`する場合、ライブラリのimportよりもやや複雑になる。1つの`.py`の中を考えるだけでなく、`.py`自体や、それらの集合にまで階層を上げて考える必要性が出てくる。

Pythonのコードはパッケージ, モジュール, 関数・クラスという、3段階の階層を持つ。

- パッケージは狭義では`.py`が集合したディレクトリ（`dir/`）である。任意のディレクトリがパッケージとして認識されるためには、そのディレクトリに`__init__.py`というファイルを置く必要がある。<br><br>

広義の(or 別の意味の)パッケージはバイナリとそれを呼び出す`.py`が入った`dir`である。例えば`pandas`は`.py`の集合ではないが、一般的にパッケージと呼ばれる。<br>
C言語で実装してコンパイルしてバイナリにしたものを`.py`が呼び出す形式にしているため高速に動作する。

- モジュールは1つ1つの`.py`ファイルである。

- 関数やクラスはモジュール、すなわち`.py`ファイル内に定義され、`.py`インスタンスに紐づいたインスタンス属性である。厳密には違うが、`.py`をインスタンスとしたときに、モジュール内の関数はメソッドのような使用感になる。

例としては下のようになる。
```
# math モジュールのimport
import math 

# モジュールの関数
math.sqrt(16)      # → 4.0
math.floor(3.7)    # → 3

# クラスのメソッド
greeding = "hello"
greeding.upper()          # → "HELLO"
greeding.replace("h", "H") # → "Hello"
```

##### 厳密にはモジュール内関数はメソッドではない

上の説明ではモジュール内の関数はメソッドのような使用感だと述べたが、実際使用感が似ているだけでメソッドではない。<br>
それは以下の2点から説明できる。

- メソッドはインスタンス属性ではなく、クラス属性である。(インスタンス属性はインスタンスによって値が決まるが、メソッドの動作はインスタンスに依らず、クラス全体で共通である。)
- モジュールというインスタンスは`ModuleType`クラスのインスタンスだが、`ModuleType`クラスにユーザーがモジュール内で定義した関数はメソッドとして登録されていない。
- クラスを呼び出すことはメソッドとは言わない。

例えば`mymodule.py`があったとき、実際にはモジュール内の`func()`という関数へのアクセスは`mymodule.__dict__["func"]()`が内部的には起きていて、メソッド属性というよりはデータ属性である。

### パッケージ内の関数の呼び出し方
`import`するときは、パッケージ, モジュール, メソッドの階層構造に沿ってパッケージからモジュールまで指定する必要がある。重要なのは、**importはモジュール（`.py`ファイル）の階層まで到達させる**ということである。一度モジュールをimportすれば、そのモジュール内の関数やクラスは`モジュール.関数()`という形でアクセスできる。


以下のようなディレクトリ構造であったとする。
```
main_dir/
├─ main.py
└─ mypackage/                 # パッケージ（ディレクトリ）
   ├─ __init__.py             # パッケージ初期化（公開APIの取りまとめにも使える）
   ├─ A.py           # モジュール（.pyファイル）
   │  ├─ function_A_C()                # 関数
   │  └─ function_A_D()                # 関数
   └─ pakage_sub_dir
      └─ B.py             # モジュール
         ├─ function_B_E()           # 関数
         └─ function_B_F()           # 関数

```

ここで、`main.py`で`function_A_C()`と`function_B_E()`を呼び出す方法を述べる。

とりあえず、重要なのは **`import`では`.py`まで届かせる** ということである。
例えば、上のディレクトリ構造で`main.py`で

```
from mypackage import A
from mypackage.package_sub_dir import B

A.function_A_C()
B.function_B_E()
```

あるいは

```
import mypackage.A
import mypackage.package_sub_dir.B

mypackage.A.function_A_C()
mypackage.package_sub_dir.B.function_B_E()
```

などと書く。

また、`numpy`は`import`のときに`from`もオブジェクトの連続参照もせずに`import numpy`のみであらゆるモジュールを用いることができる。
これは`__init__.py`内でも`import`を行うことで実現できる。例えば

```
---
__init__.py
---

from . import A # .は__init__.pyが含まれるディレクトリ(mypackage/)を指す。
from .package_sub_dir import B
```

とすることで

```
---
main.py
---

import mypackage

mypackage.A.function_A_C()
mypackage.B.function_B_E() # 注意 package_sub_dir は入れない
```

などのようにオブジェクト(属性)の参照を連続で行う形式で呼び出しを行うことができる。
さらに、`__init__.py`に途中の階層から末端の階層の`import`をしておくことでオブジェクトの連続参照における途中の部分を省略して、パッケージから直接関数を呼び出せる。
例えば
```
---
__init__.py
---

from .A import function_A_C, function_A_D
from .package_sub_dir.B import function_B_E, function_B_E
```

のようにすると、

```
---
main.py
---

import mypackage

mypackage.function_A_C()
mypackage.function_B_E()
```

のように書ける。

**注意**
- `from import`の形式で`import`の対象が複数個ある場合、`from`側でオブジェクト参照で深くまで潜ることはよいが、`import`側ではオブジェクト参照はできない。
- from側のオブジェクト参照ではパスの指定のときの`/`は用いない。つまり、ディレクトリ→ディレクトリ, ディレクトリ→ファイル, ファイル→関数 は全て等しく.のみで表す。


### 12.3.3. 属性(attribute)という概念
`A.B`はAがBという属性を呼び出すことを意味する。属性はクラス属性とインスタンス属性に分かれる。<br>

#### クラス属性
クラス属性はクラス、つまり設計図自体が値を決めていてる属性である。つまり、「インスタンスごとにここは変わるけど、これは共通だな」という部分がクラス属性である。クラス属性にはクラスデータ属性とメソッド属性がある。<br>
(クラスデータ属性は筆者の造語であり、メソッド属性と区別して作った。クラスデータ属性のことをクラス属性と呼ぶ人もいる。)

| 属性 | 書き方, 例 | 意味 |
| --- | --- | --- |
| クラスデータ属性 | MyClass.name | クラス全体で共通の値 |
| メソッド属性 | MyClass.strip() | クラス共通の関数 |

メソッド属性はインスタンスごとに処理が変わってはいけないためクラス属性だが、実際にプログラミングをするときにはインスタンス属性のようにアクセスする。

#### インスタンス属性
インスタンス属性はインスタンスごとに値が変わる属性である。インスタンス属性はデータ属性を持ち、データ属性の中にモジュール内関数がある。

| 属性 | 書き方, 例 | 意味 |
| --- | --- | --- |
| データ属性 | `myinstance.name` | インスタンスごとに異なる値 |
| モジュール内関数 | `re.sub(str)` | 厳密にはデータ属性の一種 |

```python
class Product:
    tax_rate = 0.1  # クラスデータ属性：消費税率（全商品共通）

    def __init__(self, name, price):
        self.name  = name   # インスタンス属性：商品ごとに異なる
        self.price = price

    def price_with_tax(self):  # メソッド属性
        return self.price * (1 + Product.tax_rate)

apple  = Product("apple",  200)
banana = Product("banana", 150)

print(apple.price_with_tax())   # 220.0
print(banana.price_with_tax())  # 165.0

# 税率が変わったらクラス側だけ変えれば全商品に反映
Product.tax_rate = 0.15
print(apple.price_with_tax())   # 230.0
print(banana.price_with_tax())  # 172.5
```

dataclassを使うと型が明示されてより明確に書ける。`ClassVar`でクラスデータ属性であることを型として明示する。

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Product:
    tax_rate: ClassVar[float] = 0.1  # クラスデータ属性：ClassVarで明示

    name: str
    price: float

    def price_with_tax(self) -> float:
        return self.price * (1 + Product.tax_rate)

apple  = Product("apple",  200)
banana = Product("banana", 150)

print(apple.price_with_tax())   # 220.0
print(banana.price_with_tax())  # 165.0

Product.tax_rate = 0.15
print(apple.price_with_tax())   # 230.0
print(banana.price_with_tax())  # 172.5
```
