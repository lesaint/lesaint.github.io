---
layout: post
title: Introduction to a Bean Mapping Wiring Framework implementation
tags:
 - Java
 - Bean Mapping
image:
 feature: feature_image_green.png
---

I talked in an previous [article]() of the need of doing Bean Mapping in Java a new way and how that involves designing and developing a Bean Mapping Wiring Framework.

In this article, I will try and go deeper into the design of such framework:

* goal and scope
* hypothesis of design
* technical patterns
* ...


# Goal and scope of a Bean Mapping Wiring Framework

The primary goal of a Bean Mapping Wiring Framework is to make easier/more fluent/less repetitive the use of Bean Mapping code whereever it is needed.

I identified two major use cases of Bean Mapping code integration:

1. Bean Mapping code is called from the application code
    * this may happen in any part of the application
2. Bean Mapping code is called from another piece of Bean Mappping code
    * this happens when one need to map the property of a bean which is itself a bean (aka mapping tree of beans)

## DI/IOC frameworks integration

Remember, the Bean Mapping Wiring Framework does not do Bean Mapping by itself.

In fact, it doesn't even do actual wiring (what?!).

What it does is either give every options to the developer to do the wiring by hand, her way, or integrate with the wiring framework the application already uses. The application's wiring framwork could be Spring, Guice, Dagger, [[TODO find name of Java's specification for Dependency Injection and IOC]], ... or any other Dependency Injection (`DI`) and/or Inversion Of Control (`IOC`) framework.

This integration could take the form of annotations added to the generated classes and/or generated configuration files (XML or other) and/or generated configuration classes, etc...

In the end, this integration will be a big part of the framework and the goal is to create a pluggable architecture for any framework integration (I'm thinking about a solution as simple as adding a jar to the classpath).

## Bean Mapping specific patterns

The scope of the Bean Mapping Wiring Framework also includes technical solutions to problems specific to Bean Mapping problems such as:

* mapping tree of beans
* mapping multiple source beans to a single bean
* mapping immutable bean (in fact, the framework should push for user to use immutable beans, we will talk about that in details later)
* mapping beans back and force
* mapping collection of beans
* ...

We will go over these solutions later in this article or in future articles.

# Hypothesis of design

We will now discuss the fondamental technical choices behind DAMapping, an initial implementation of a Bean Mapping Wiring Framework.

## everything will be compiled

I think the number one tool of the Java developer is the compiler. This is the strongest process giving garanties of a working program.

So, this new framework must make use of the compiler and must be typesafe.

Obviously, typesafety will end wherever it ends when integrating with other tools.

## developer writes barely more than Bean Mapping code

The fondamental principal behind this new Bean Mapping paradigm is that the developer writes the Bean Mapping code.

And we should ask for barely more than that.

Our goal is that the developer writes some method implementing some Bean Mapping behavior and uses annotations let the framework know about it and do its wiring job.

And that should be it.

## but we need interfaces

Obviously, we can't wire the developer's concret classes directly into the rest of the application or other Bean Mapping classes. We need interfaces:

* to enforce loose coupling
    - between the application and the Bean Mapping code
    - between multiple pieces of Bean Mapping code
* and promote unit testing as each piece of Bean Mapping code will be mockable
* which, combined with the power of the framework, will favor Separation Of Concern
    - there will be a lot less pain into multiplying smaller classes
* and overall Bean Mapping code will be very well tested and exactly as the developer wants it

Since it is not an option to make the developer's concret class implement this interface (technically borderline and too much intrusive), we will need a concrete class implementing it and acting as a proxy (or facade) to the developer's class.

## so we will generate them using an Annotation Processor

Since Java 7 (and latest Java 6 versions), annotation processing is fully part of the compiler (annotation processing used to be implemented through a separate tool : APT).

`javax.annotation.processing.Processor` is the type which can be implemented to perform annotation processing and will be instanced and called directly by the compiler.

The compiler fully supports classes and interfaces generated by the Annotation Processors. Generated classes and interfaces are also compiled and can declare annotations which are in turn processed if necessary, generating classes if it applies, which are then compiled, and so on...

We will use annotation processing to generate the interfaces (and their implementations) the developer would have otherwise written to integrate its Bean Mapping code as cleanly as possible.

# Core technical concepts

## Core class pattern

The core pattern to which the points above lead to is the following:

![Core Pattern](/resources/java_bean_mapping_is_wrong_lets_fix_it/core_pattern.png)

> class `FooToBar` is written in the application code by the developer. This class exposes one method called `apply` which will implement the mapping from an instanceo of type `Foo` to a new instance of type `Bar`
> 
> The Bean Mapping Wiring Framework will generate the interface `FooToBarMapper` which exposes a method `apply` with exact same signature as the one in class `FooToBar`.
> 
> The framework will also generate a class `FooToBarMapperImpl` which implements `FooToBar` and is associated with type `FooToBar` to delegate the implementation of method `apply` inherited from the interface `FooToBar`. 
> 
> The `FooToBarMapper` interface and the `FooToBarMapperImpl` class will be generated in the same package as `FooToBar`.

## how to identify the Bean Mapping method

We have two options:

1. using a class annotation as the first and only requirement
    - the developer annotates the class with a `@Mapper` annotation
    - the Bean Mapping Wiring framework then identifies the Bean Mapping method either automatically or with an optional method annotation
2. using a method annotation as the first and only requirement
    - the developer annotates any method on any class doing Bean Mapping with a `@MapperMethod` annotation

Both solutions are valid but I prefer the first one as it favours class specialisation.

Class specialisation is important because the class name will be used as the base name of generated classes and interfaces. I would better be meaningfull.

Still, I forsee that this is subject to discussion and the second solution may be implemented later.

## How to reference the Bean Mapping method

The only techical challenge in generating the code of the core pattern is referencing the method which implements the Bean Mapping code.

Which kind of method can be referenced will depend on the method itself and most importantly on the class it belongs to.

## method modifiers

<table>
    <thead>
        <tr>
            <td>class modifier</td>
            <td>can be referenced ?</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>private</td>
            <td>no</td>
        </tr>
        <tr>
            <td>public</td>
            <td>yes</td>
        </tr>
        <tr>
            <td>protected ou package protected</td>
            <td>yes *</td>
        </tr>
        <tr>
            <td>final</td>
            <td>n/a</td>
        </tr>
        <tr>
            <td>static</td>
            <td>yes</td>
        </tr>
    </tbody>
</table>

## class modifiers

<table>
    <thead>
        <tr>
            <td>class modifier</td>
            <td>static method</td>
            <td>no static method</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>private</td>
            <td>no</td>
            <td>no</td>
        </tr>
        <tr>
            <td>public</td>
            <td>yes</td>
            <td>yes</td>
        </tr>
        <tr>
            <td>protected</td>
            <td>yes *</td>
            <td>yes *</td>
        </tr>
        <tr>
            <td>package protected</td>
            <td>yes *</td>
            <td>yes *</td>
        </tr>
        <tr>
            <td>final</td>
            <td>n/a</td>
            <td>n/a</td>
        </tr>
        <tr>
            <td>abstract</td>
            <td>yes</td>
            <td>no</td>
        </tr>
    </tbody>
</table>

> *: because `MapperImpl` class is generated in the same package as the developer's class

## the various types of class

### inner class

Inner classes can be referenced as long as they are at least `default protected` and `static`.

### class with default constructor

This kind of class can simply be instanced with the `new` operator. Association is actually a composition.

{% highlight java %}
class FooToBarMapperImpl implements FooToBarMapper {
    private final FooToBar instance = new FooToBar();

    public static Bar apply(Foo foo) {
        return instance.apply(foo);
    }

}
{% endhighlight %}

### class without a default constructor

This class can not be instanced with the `new` operator without some extra information from the developer about which value(s) to pass as argument(s).

Since we want to have the least possible configuration, it is not an option to ask the developer for this information. In addition, finding a way of describing how to instance such class would be a complexe challenge.

Since it is DI frameworks job to deal with that specific problem and that's we are planning on integrating them, there is not point in reinventing the wheel.

Also, as we will see later, a class with a no default constructor could be a `MapperFactory`, and we will deal specifically with that.

### class with multiple constructors

Same problem as above (we do not know how to use the `new` operator) and same solution.

### Singleton enum

Singleton enum are very easy to associate with. We can have use a direct static reference to the method. We know the qualified name of the developer's class and finding out the name of the single enum value is easy.

{% highlight java %}
class FooToBarMapperImpl implements FooToBarMapper {

    public static Bar apply(Foo foo) {
        return FooToBar.INSTANCE.apply(foo);
    }

}
{% endhighlight %}

### singleton with static instanciation method

As long as the static factory method for the singleton has no argument, it is easy to use in `MapperImpl` class, otherwise, the problem will be the same as a constructor with arguments.

This pattern can be detected with certainty only if the `FooToBar` class is `final`, has only `private` constructors and a no `private` `static` method returning a `FooToBar` type.

{% highlight java %}
public final class FooToBar {
    private static final FooToBar INSTANCE = new FooToBar();

    private FooToBar() {  /* prevents instantiation out of the static method instance() */ }

    public FooToBar instance() {
        return INSTANCE;
    }
}
{% endhighlight %}

The `MapperImpl` source code will then look like that:

{% highlight java %}
class FooToBarMapperImpl implements FooToBarMapper {

    public static Bar apply(Foo foo) {
        return FooToBar.instance().apply(foo);
    }

}
{% endhighlight %}

# Pattern for mapping trees of Beans

Assuming that the developer has written a `Mapper` for each one-to-one Bean Mapping, mapping tree of beans is just a matter of using another `Mapper`

# Pattern for mapping multiple beans to one

I refer to this pattern as the `MapperFactory` pattern.

# Java 8 method references and lambdas

I don't have enough practical knowledge of lambdas and method references as of today to be sure of the impact of the Bean Mapping Wiring framework implementation.

Theorically, I can forsee that method references and lamdas will most be usefull with the `MapperFactory` pattern since it will avoid creating inner or anonymous classes.



# DI Framework integration

Several type of classes above can not be composed directly without extra information from the developer.

However. if the application is using a DI framework, the composition issue can be solved very easily by having the generated `MapperImpl` class injected with an instance.

## MappingImpl integration with the application
