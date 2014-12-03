---
layout: damapping
title: Principles of DAMapping
css: damapping
categories:
 - damapping
comments: true
---

DAMapping is based on several principles: show the logic and hide the implementation, use only Java code, logic belongs to source, be flexible and open, TOOD finish excerpt


* Table of Contents
{:toc}

# Show the logic, hide the implementation

Object mapping is actually two separate things: the object mapping logic and the object mapping implementation.

The former is about *deciding* how to map one object to another. The latter, is about *implementing* these decisions.

The former should be clearly expressed and easy to modify. The latter is what the developer wants to avoid dealing with.

The developer wants to read code that says: call `bar.setName` with the value of `foo.getNom` and when the value is `null` use `NO_NAME` constant. This is the object mapping logic. It should be expressed as code in short and comprehensive way.

But he or she doesn't want to write that code testing for `null` again and over again. This is the object mapping implementation, it should be hidden. Same goes for mapping a `String` to an `enum` value, or an array to a Collection, ...

# Pure Java code

Object mapping must be coded in pure Java because:

* you get fully statically typed object mapping and leverage the power of the compiler
* you get clean and comprehensive stack traces when errors occur
* you can easily debug it and follow the code flow
* anyone can understand it, there is no need to learn some tool syntax

# Object mapping, not bean mapping

Most existing tools are bean mapping tools. They assume that they will be used to map Java beans. But, as [Stephen Colebourne](https://twitter.com/jodastephen) pointed out in a [recent article](http://blog.joda.org/2014/11/the-javabeans-specification.html), JavaBean is a specification from 1997 which is quite specific (and outdated now) and hardly what most people think of Java Beans are: mutable data objects with getter and setters.

The fact is that this specification from old times is not even clear on what getters and setters are (recall the ever happening discussion on how getters for `boolean` types should be named?).

In addition, our real coding life is rarely made of true Java Beans (if that even exists), not even talking about immutability getting more and more adopters and totally out of the JavaBean scope.

For all this reasons, DAMapping is based the foundamental hypothesis that it will NOT be used on beans, but more generally on objects.

# Object mapping logic in source

**Object mapping is important** to your application, your library, it is part of it. If it is important, then the object mapping logic should be in source code because:

* its stable: it doesn't change unless you want it
* it's in your VCS: if it changes, you can find out when and (hopefully) why it did
* you own it: its in source, you can change or complete what DAMapping generated for you (if you even used the generator in the first place)
* you can refactor it like any other piece of code

# Be flexible

## a flexible stack

DAMapping is a stack of components. Those components can be used as a whole or as many combination of them:

* **framework + library + generator + IDE plugin**: use the *DAMapping generator* from the *DAMapping IDE plugin* and leverage the power of the *DAMapping framework* and *DAMapping library*
* **library + generator + IDE plugin**: use the *DAMapping generator* and the *DAMapping IDE plugin* but not the *DAMapping framework* by generating code inside your own methods
* **framework + library**: use the *DAMapping framework* to structure your object mapping code, maybe use he *DAMapping library* too, but that's it
* **library alone**: use the *DAMapping library* anywhere, maybe not even to do object mapping as such

## flexible components

Each component of DAMapping is designed to be flexible.

|:--------|:-------:|--------:|
| *framework*   | offers a highly versatile way of structuring object mapping code. It is flexible and has little, almost no, constraint |
| *library*   | aims at providing comprehensive and powerful utility classes and methods for any type of object mapping operation|
| *code generator*   | provides pertinent defaults by can be customized to suit the developer or the application preferences |
| *IDE plugins*   | support preferences for the *DAMapping code generator* and the *DAMapping framework*|
{: rules="groups"}
