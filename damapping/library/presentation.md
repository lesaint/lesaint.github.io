---
layout: damapping
title: Presentation of the DAMapping library
excerpt: TODO excerpt library presentation 
css: damapping
image:
 feature: feature_image_damapping.png
---

# The bean mapping library

The DAMapping's bean mapping library provides utility methods, class and patterns to help write all those recurrent, technical, bean mapping code: null and default value handling, primitive <-> Object mappings, enum mapping, collection mapping, etc... 

The library exposes meaningfully named classes and methods, leveraging the readability of [method chaining](http://en.wikipedia.org/wiki/Method_chaining) and [fluent interface](http://en.wikipedia.org/wiki/Fluent_interface) coding styles.

## anybody can use it, anywhere

The library is obviously used by the code generator. But this implies that the developer will use it too, since the code is generated in the application's source code.

Apart for putting additional pressure on the quality of the documentation, this is good. This is where DAMapping really hands over the reins to the developer and give her all the power to write bean mapping code the way she likes.

A barely hidden wish is that the library will provide powerful enough classes and methods that they will be used by developer in pieces of code far from being bean mapping code.

## modular design

The library should be split in several modules.

The core module will have no dependencies and will be coded exclusively against the Java API.

Other modules will be provided with specific implementations of the classes in the core module or new classes and methods, e.g. a Guava module.

Unless the developer just ignores these questions, how to map those properties from one to the other isn't trivial until... 

...until we can write it with a one-liner with good semantics. In the `String` to `enum` case described above, we could write:

{% highlight java %}
bar.setProp(EnumMapper.from(foo.getProp()).ignoreCase().orElse(SomeEnum.SOME_VALUE));
{% endhighlight %}

It seals it is only a matter of having the right utility methods/classes/API to write that one-liner.
