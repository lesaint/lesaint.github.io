---
layout: damapping
title: Getting started with the DAMapping framework
excerpt: This page will help you to get started with the *DAMapping framework*. How to install it, understand its principles, get started with basic usage, map object tree, integrate with dependency injection frameworks...
css: damapping
categories:
 - damapping
comments: true
---

This page will help you to get started with the *DAMapping framework*: install it, understand its principles, get started with basic usage and object tree mapping, integrate with dependency injection frameworks...

* Table of Contents
{:toc}

Installation
============

To use the *DAMapping framework* you only need to add its jar file to your classpath.

For Maven users, you can do so by adding the following dependency:

{% highlight xml %}
<dependency>
    <groupId>fr.phan.damapping</groupId>
    <artifactId>damapping-annotation-processor</artifactId>
    <version>0.4.0</version>
    <!-- scope does not need to be explicitly specified, default scope works just fine -->
    <scope>compile</scope>
</dependency>
{% endhighlight %}

That's it!

Structure object mapping code
===========================

When it comes to object mapping, assuming you want it all written in Java, you need to get organized.

The following practices can easily be considered as best practices in the matter:

* use one class for each mapping from one type to another and compose these classes ([SOC](http://en.wikipedia.org/wiki/Separation_of_concerns), [KISS](http://en.wikipedia.org/wiki/KISS_principle), re-usability)
* use an interface and an implementing class for each mapping and do not use static code (better testability)
* integrate with the Inversion-of-control and dependency injection framework already in place within the application if there is one

Unfortunately, to implement these principles, we need a lot of boiler plate code (one class + one interface for each type-to-type mapping?!).

The goal of the *DAMapping framework* is to handle that problem: the developer writes object mapping code in specific classes and only that. Still, he or she gets all the benefits of the principles above.

How it works
============

The *DAMapping framework* achieves that by generating pure Java "glue" code:
* between each object mapping class
* between object mapping class and the rest of the application
* between object mapping class and the dependency injection frameworks

Mind it! The *DAMapping framework* does not generate any object mapping code and it is always **fully statically typed**!

The *DAMapping framework* is implemented as a (volontarily) limited set of [annotations](https://github.com/lesaint/damapping/tree/master/core-parent/annotations/src/main/java/fr/javatronic/damapping/annotation) and an Annotation Processor.

As you will see below, using the *DAMapping framework* is very simple and it enforces little to no constraint at all on the way you should structure your object mapping code.

Basic usage of the framework
============================

The class below is a `Mapper` as per DAMapping framework's definition: it is a class with a method doing object mapping (talk about KISS).

The class is identified by the `@Mapper` annotation.

{% highlight java %}
@Mapper
public class FooToBar {
    public Bar map(Foo foo) {
        // some code returning a Bar instance
        // initialized/populated from the specified Foo instance
    }
}
{% endhighlight %}

Please note that this is a class, not an interface. We are not configuring a tool to do object mapping, we are providing object mapping code to the framework.

A class annotated with `@Mapper` is the atomic component of object mapping code according to DAMapping's object mapping code paradigm. It is also referred to as the "dedicated class".

Although the example above is a dedicated class mapping a single type to another, the DAMapping framework does not enforce such a rule (though it is best to follow it), nor does it enforce any naming convention.

This is done on purpose as the goal of DAMapping is to support the developer, not to constrain her into a single way of coding.

Integrating with the application
================================

When using the DAMapping framework, the developer is supposed to use the MapperImpl class in her/his application code, not the dedicated class directly.

## integrates like regular code

See below an example of using object mapping code with DAMapping framework manually.

{% highlight java %}
public class MyServiceImpl {
    public void doSomething() {
        // instance mapper for the tree roots   
        AcmeToVitenMapper mapper = new AcmeToVitenMapperImpl(new FooToBarMapperImpl());

        // use the mapper
        Acme someAcme = ...,
        Viten viten = mapper.map(someAcme);
    }
}
{% endhighlight %}

## no all-purpose entry point

Note that the entry point to the object mapping code is not some generic class that usually acts as the single point of entry for all code managed by other tools.

Here, it is a fully typed and specific interface, meaningfully named and exposing a method named as the developer feels suits best.

1 class = 1 interface + 1 class
===============================

The first added value of the DAMapping framework is to save the developer from writing an interface and an implementing class for each mapper. They are generated by the framework at compile-time.

In the example above, the framework generates a `FooToBarMapper` interface and a `FooToBarMapperImpl` class (did you identify the naming pattern? ;-p).

The `FooToBarMapper` interface has a single method. Same name, same return type, same parameters and same annotations as the public method of the dedicated class. This interface is referred to as the "Mapper interface".

{% highlight java %}
public interface FooToBarMapper {
    Bar map(Foo foo);
}
{% endhighlight %}


The `FooToBarMapperImpl` class implements this method by instantiating a single instance of the dedicated class and delegating her the implementation of the method defined by `FooToBarMapper`. This class is referred to as the "MapperImpl class".

{% highlight java %}
public class FooToBarMapperImpl implements FooToBarMapper {
    private final FooToBar fooToBar = new FooToBar();
    @Override
    public Bar map(Foo foo) {
        return this.fooToBar.map(foo);
    }
}
{% endhighlight %}

Mapping object trees
====================

The next added value of the DAMapping coding paradigm is to remove all the coding ceremony when mapping a object tree to another thanks to the DAMapping framework.

To map object trees, the developer composes generated Mapper interfaces into dedicated classes.

In the following example, the dedicated class `AcmeToViten` maps the type `Acme` to the type `Viten`. These types are the root of two (very simple) object trees: `Acme` has a property of type `Foo` which must be mapped to the `Viten`'s property of type `Bar`.

{% highlight java %}
@Mapper
public class AcmeToViten {
    private final FooToBarMapper fooToBarMapper;
    public AcmeToViten(FooToBarMapper fooToBarMapper) {
        this.fooToBarMapper = fooToBarMapper;
    }
    public Viten map(Acme acme) {
        // some code instanciating a Viten instance and 
        // populating it from the specified Acme instance
        vilen.setBar(fooToBarMapper.map(acme.getFoo()));
        return vilen;
    }
}
{% endhighlight %}

The Mapper interface generated from this dedicated class has the same content as the `FooToBarMapper` interface.

The generated `AcmeToVitenMapperImpl` class is a little different from `FooToBarMapperImpl` as it defines a constructor with the same parameters and annotations as the dedicated class's constructor.

{% highlight java %}
public class AcmeToVitenMapperImpl implements AcmeToVitenMapper {
    private final AcmeToViten acmeToViten;
    public AcmeToVitenMapperImpl(FooToBarMapper fooToBarMapper) {
        this.acmeToViten = new AcmeToViten(fooToBarMapper);
    }
    @Override
    public Viten map(Acme acme) {
        return this.acmeToViten.map(acme);
    }
}
{% endhighlight %}

Integrating with DI frameworks
==============================

Obviously, few applications will instance concrete class directly. They will rather use a dependency-injection framework (Spring, Guice, Dagger, ...) that will manage object instantiation and injection.

The DAMapping framework supports integrating with those frameworks, but as it is not a core functionality to writing object mapping code, we won't go into too much details here.

The planned idea is to initially provide minimal support through the support of the JSR-330 specification (work in progress).

Next, extensive support for specific dependency-injection frameworks will be provided as plugins of DAMapping annotation processor.

Extensive support for Spring, for example, could be generating Configuration classes or XML configuration files or supporting Spring specific annotations.

Unit testing
============

I said earlier that the developer is not supposed to use the dedicated class directly.

It is exactly the opposite when it comes to unit testing. The developer must write unit tests againt the dedicated class directly. There is no point in testing DAMapping framework itself.

Note that thanks to DAMapping, the developer can write real unitary tests of the mapping from one type to another. Mapping of properties with complex types can be isolated in other dedicated classes and imported into the current one as Mapper interfaces, which can be easily mocked.
