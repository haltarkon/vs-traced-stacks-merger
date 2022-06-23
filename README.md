# vs-traced-stacks-merger

Simple script for merging text outputs of [Visual Studio Tracepoints](https://docs.microsoft.com/en-us/visualstudio/debugger/using-tracepoints) with specific format into textual chronological call tree representation. It can be useful to visualize at what points in time and with what data the program passes some execution points.

## Recording stacks

In visual studio we can add [tracepoints](https://docs.microsoft.com/en-us/visualstudio/debugger/using-tracepoints). Tracepoints allow us to log information to the Output window under configurable conditions without modifying or stopping your code. We can add new tracepoint in the same way as breakpoint in settings we should select `Actions` and write our message into text box. Message format allows to use som additional variables such as `$CALLSTACK`, `$TICK`, `$ADDRESS`.

In order to record information in the required format, you must specify the following message:
```c++
{"\t",s8b}...,Time:$TICK{"\n",s8b}$CALLSTACK
```
Where:
+ `{"\t",s8b}` - tabulation symbol;
+ `...` - a single-line optional message of your choice, fell free to use some variables;
+ `$TICK` - a varible with current timer value;
+ `{"\n",s8b}` - a line feed;
+ `$CALLSTACK` - a variable with current callstack list.

Each output portion in Output window for each tracepoint will be inseparable, but it may happen that the order is not true. To do deal with it, we use `$TICK`. Also, unfortunately, `$CALLSTACK` displays only function names, no signatures. In case of functions and methods overloading, the result will be combined as if the function is only one.

Once the points are placed, follow the necessary steps on your test program. In the Output window you will see the content with format like this:
```c++
Some unrelated line.
Some unrelated line.
	1, First,Time:0x00000001
	libB.dll!ClassA1::methodA1
	libA.dll!funcA2
	libA.dll!funcA1
	app.exe!f0
	app.exe!main
	
	3, Third,Time:0x00000003
	libB.dll!ClassA2::methodA1
	libA.dll!funcA2
	libA.dll!funcA1
	app.exe!f0
	app.exe!main
	
	2, Second,Time:0x00000002
	libB.dll!ClassA2::methodA1
	libA.dll!funcA2
	libA.dll!funcA1
	app.exe!f0
	app.exe!main
	
Some unrelated line.
	4, Fourth,Time:0x00000004
	libB.dll!ClassA1::methodA1
	libA.dll!funcA3
	libA.dll!funcA1
	app.exe!f0
	app.exe!main

Some unrelated line.
```

Then you can manually copy text or select VS Output window and use `File` -> `Save Output As...`. Now you have some `Output-Debug.txt` file.

## Merging

To make the conclusion clearer, you can use [this script](vs-traced-stacks-merger.py):
```console
$ ./vs-traced-stacks-merger.py -i example/Output-Debug.txt -o example/Output-Debug_tree.txt -t '\t'
```

In the Output-Debug_tree.txt file, you will get the result as follows:
```c++
app.exe!main
app.exe!f0
libA.dll!funcA1
libA.dll!funcA2
	libB.dll!ClassA1::methodA1
		1, First
	libB.dll!ClassA2::methodA1
		2, Second
		3, Third
libA.dll!funcA3
	libB.dll!ClassA1::methodA1
		4, Fourth
```

