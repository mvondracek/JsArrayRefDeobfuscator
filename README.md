# JavaScript Array Ref Deobfuscator

[![Python version](https://img.shields.io/badge/Python-3-blue.svg?style=flat-square)](https://www.python.org/)
![Python application](https://github.com/mvondracek/JsArrayRefDeobfuscator/workflows/Python%20application/badge.svg)

JavaScript deobfuscator which can revert *Array Ref* obfuscation format. This
format is characteristic by global array in the beginning of the file containing
all values and method names used in the original source code. Obfuscated code
then uses references to this global array instead of literals and methods. This
makes manual analysis of the code more time-consuming, as production code can
easily contain thousands of items in mentioned global obfuscation array.

For an easy example, following obfuscated code
~~~js
var _0x01ff=["foo",0,1,"bar"];function f(){return _0x01ff[3]}var a=_0x01ff[0];a=[_0x01ff[1]+1,_0x01ff[1]?
_0x01ff[_0x01ff[_0x01ff[2]]]:_0x01ff[2]];switch(f(_0x01ff[0])){case _0x01ff[0]:a=_0x01ff[0];break;
default:a=_0x01ff[2];break;}
~~~

can be deobfusated to mode understandable version below.
~~~js
var _0x01ff = ["foo",0,1,"bar"];
function f() {
  return "bar";
}
var a = "foo";
a = [0 + 1,0 ? "foo" : 1];
switch (f("foo")) {
  case "foo":
    a = "foo";
    break;
  default:
    a = 1;
    break;
}
~~~

For more short examples, please see implemented unit tests ([`/tests`](/tests)).

## Help

```bash
$ ./jsardcli.py --help
```
