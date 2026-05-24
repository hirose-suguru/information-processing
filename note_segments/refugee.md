<a id="zero-zero-zero-zero-one"></a>
##### 0.0.0.0.1. 実は奥が深いprint関数
```
print(
	*values: Any,
    sep: str = " ",
    end: str = "\n",
    file: IO[str] | None = None,
    flush: bool = False,
    )
-> NoneType:
```

<a id="zero-zero-one"></a>
### 0.0.1. データ属性が返り値を持てる
メソッド属性`A.B()`は`B()`が関数なため返り値を持つことは理解しやすいが、実は`A.C`のようにデータ値属性も返り値を返すことがある。

例えば
``` python
df_year = df_day["date"].dt.year
```
という処理は、
①`df_day`という`DataFrame`が`"date"`というラベルの数値群を持っている
②その数値群は全て日付形式であり、それを全て年の情報だけに変換する
③そうしてできた新しい数値群に対して`"year"`というラベルをつけ、新しい数値群とともに`year`という名前の`Series`クラスのオブジェクトとして`DataFrame`に登録する
という流れになっている。

`=`という文の性質上、右辺はなんらかのオブジェクトになっているはずで、すなわち`.dt.year`というデータ値属性がなんらかのオブジェクトを返しているということを示している。実際に今回は`Series`クラスのオブジェクトを返している。
