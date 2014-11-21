---
layout: damapping
title: Principles of DAMapping
css: damapping
---

DAMapping is based on several principles: show the logic and hide the implementation, use only Java code, logic belongs to source, be flexible and open, TOOD finish excerpt


* Table of Contents
{:toc}

# Show the logic, hide the implementation

Bean mapping is actually two separate things: the bean mapping logic and the bean mapping implementation.

The former is about *deciding* how to map one bean to another. The latter, is about *implementing* these decisions.

The former should be clearly expressed and easy to modify. The latter is what the developer wants to avoid dealing with.

The developer wants to read code that says: call `bar.setName` with the value of `foo.getNom` and when the value is `null` use `NO_NAME` constant. This is the bean mapping logic. It should be expressed as code in short and comprehensive way.

But he or she doesn't want to write that code testing for `null` again and over again. This is the bean mapping implementation, it should be hidden. Same goes for mapping a `String` to an `enum` value, or an array to a Collection, ...

# Pure Java code

Bean mapping must be coded in pure Java because:

* you get fully statically typed bean mapping and leverage the power of the compiler
* you get clean and comprehensive stack traces when errors occur
* you can easily debug it and follow the code flow
* anyone can understand it, there is no need to learn some tool syntax

# Bean mapping logic in source

**Bean mapping is important** to your application, your library, it is part of it. If it is important, then the bean mapping logic should be in source code because:

* its stable: it doesn't change unless you want it
* it's in your VCS: if it changes, you can find out when and (hopefully) why it did
* you own it: its in source, you can change or complete what DAMapping generated for you (if you even used the generator in the first place)
* you can refactor it like any other piece of code

# Be flexible

## a flexible stack

DAMapping is a stack of components. Those components can be used as a whole or as many combination of them:

* **framework + library + generator + IDE plugin**: use the *DAMapping generator* from the *DAMapping IDE plugin* and leverage the power of the *DAMapping framework* and *DAMapping library*
* **library + generator + IDE plugin**: use the *DAMapping generator* and the *DAMapping IDE plugin* but not the *DAMapping framework* by generating code inside your own methods
* **framework + library**: use the *DAMapping framework* to structure your bean mapping code, maybe use he *DAMapping library* too, but that's it
* **library alone**: use the *DAMapping library* anywhere, maybe not even to do bean mapping as such

## flexible components

Each component of DAMapping is designed to be flexible.

|:--------|:-------:|--------:|
| *framework*   | offers a highly versatile way of structuring bean mapping code. It is flexible and has little, almost no, constraint |
| *library*   | aims at providing comprehensive and powerful utility classes and methods for any type of bean mapping operation|
| *code generator*   | provides pertinent defaults by can be customized to suit the developer or the application preferences |
| *IDE plugins*   | support preferences for the *DAMapping code generator* and the *DAMapping framework*|
{: rules="groups"}
