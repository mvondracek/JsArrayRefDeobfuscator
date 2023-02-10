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
var _0x01ff=["foo",0,1,"context aware \"_0x01ff[0]\""];function f(){return _0x01ff[3]}var a=_0x01ff[0];
a=[_0x01ff[1]+1,_0x01ff[1]?_0x01ff[_0x01ff[_0x01ff[2]]]:_0x01ff[2]];switch(f(_0x01ff[0])){case _0x01ff[0]:
a=_0x01ff[0];break;default:a=_0x01ff[2];break;}
~~~

can be deobfusated to a more understandable version below.
~~~js
var _0x01ff = ["foo",0,1,"context aware \"_0x01ff[0]\""];
function f() {
  return "context aware \"_0x01ff[0]\"";
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


## Publication

This software was developed during research on
[Rise of the Metaverse's Immersive Virtual Reality Malware and the Man-in-the-Room Attack & Defenses](https://www.sciencedirect.com/science/article/pii/S0167404822003157).
Please see the paper for more details and use following citation.

~~~BibTeX
@article{Vondracek-2023-102923,
    title = {Rise of the Metaverse’s Immersive Virtual Reality Malware and the Man-in-the-Room Attack & Defenses},
    journal = {Computers \& Security},
    volume = {127},
    pages = {102923},
    year = {2023},
    issn = {0167-4048},
    doi = {https://doi.org/10.1016/j.cose.2022.102923},
    url = {https://www.sciencedirect.com/science/article/pii/S0167404822003157},
    author = {Martin Vondráček and Ibrahim Baggili and Peter Casey and Mehdi Mekni}
}
~~~


## Links

- [UNHcFREG, *BigScreen and Unity Virtual Reality Attacks and the Man in The Room Attack*](https://www.unhcfreg.com/single-post/2019/02/19/bigscreen-and-unity-virtual-reality-attacks)
- [University of New Haven, *University of New Haven Researchers Discover Critical Vulnerabilities in Popular Virtual Reality Application*](https://www.newhaven.edu/news/releases/2019/discover-vulnerabilities-virtual-reality-app.php)
- Martin Vondráček, Ibrahim Baggili, Peter Casey, and Mehdi Mekni.
  *Rise of the Metaverse's Immersive Virtual Reality Malware and
  the Man-in-the-Room Attack & Defenses*. Computers \& Security.
  vol. 127. p. 102923. 2023. Online.
  https://www.sciencedirect.com/science/article/pii/S0167404822003157
