---
layout: damapping
title: Presentation of the DAMapping library
excerpt: TODO excerpt library presentation 
css: damapping
categories:
 - damapping
---

* Table of Contents
{:toc}

# The bean mapping library

The DAMapping's bean mapping library provides utility methods, class and patterns to help write all those recurrent, technical, bean mapping code: null and default value handling, Object to primitives mappings, enum mapping, collection mapping, etc... 

## anybody can use it, anywhere

The library is obviously used by the code generator. But this implies that the developer will use it too, since the code is generated in the application's source code.

Apart for putting additional pressure on the quality of the documentation, this is good. This is where DAMapping really hands over the reins to the developer and give her all the power to write bean mapping code the way she likes.

A barely hidden wish is that the library will provide powerful enough classes and methods that they will be used by the developer in pieces of code far from being bean mapping code.

## modular design

The library should be split in several modules.

The core module will have no dependencies and will be coded exclusively against the Java API.

Other modules will be provided with specific implementations of the classes in the core module or new classes and methods, e.g. a Guava module.

# Foundations

## 1: expressiveness

Using the DAMapping library classes and methods should lead to bean mapping being as expressive as possible.

For example, the following concepts should be easily understood by just reading the code: 

* `null` or unknown values handling, default values
* type conversions (which is the source type, which is the target type)
* precision loss or change of data structure
* ...

The library should use a combination of [method chaining](http://en.wikipedia.org/wiki/Method_chaining), [fluent interface](http://en.wikipedia.org/wiki/Fluent_interface) and static imports to achieve a near bean mapping DSL for Java.

## 2: clean stacktraces

This should be a side-effect of the first principle but it could also be a deal breaker: stacktraces must be kept readable and meaningful.

This means that some coding pattern which would otherwise be great for expressiveness will have to be discard because they introduce too many methods calls only related to configuration instead of processing.

## 3: performance

Last by not least, the DAMapping library must aim at providing the best performance (non exhaustive list):

* avoid copies of data
* non blocking, thread-safe unless otherwise explicitly stated

