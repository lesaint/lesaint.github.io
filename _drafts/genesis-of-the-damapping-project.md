---
layout: post
title: "Genesis of the DAMapping project"
tags:
 - DAMapping
 - Annotation Processing
 - Java
categories:
 - articles
image:
 feature: feature_image_green.png
---

This article is about going through the genesis of the DAMapping project. It details the path of experience and thoughts I followed (with the help of several dear colleagues) to get to the concepts and design of the DAMapping project and each of its components.


* Table of Contents
{:toc}

# Genesis of a new approach

## experience: not satisfied by existing tools

I have worked for 4 years on a fast growing and evolving project that integrated up to 100+ external services and was made on several layers of software. We had a LOT of bean mapping.

Looking back, I can say that bean mapping as such wasn't a problem, until...

...until we had to maintain it. Until we had to have it change when mapped types changed. Until we had to make sure of what was going on because we had a bug (using a debugger or just reading through the code).

We lost a tremendous amount of time tracking problems at the bean mapping level. Customer was deeply disappointed with the application's quality, we had major bugs in production. They were hard to fix because what happened in the bean mapping library was obscure, required good knowledge of the tool to be fixed (not everyone could dive in), was barely tested and we couldn't used our regular investigation technics (read code through code, use the debugger -- locally or with [jdb](http://docs.oracle.com/javase/7/docs/technotes/tools/windows/jdb.html) on remote servers, ...).

We tried several approaches to bean mapping, to lower the difficulty with this: we conducted experiments and thoroughly studied existing tools, tried coding all by hand...

## best solution: write it all by hand

After a while, all the 10-15 developers were writing bean mapping code by hand, all other solutions had been dropped because of their middle and long term issues (listed earlier). It also was the most efficient solution at runtime and the easiest to customize (obviously, plain Java code = complete customization freedom). All code was there in plain view, we could refactor with IDEA, find usages (is that property set? where? is extremely valuable), code was stable and any modification could be tracked down in Git/Svn.

The general practice was to use Guava's [Function](http://docs.guava-libraries.googlecode.com/git/javadoc/com/google/common/base/Function.html) as an interface implemented by every class mapping one type to another. It had the very convenient side effect of allowing to map collections with Guava's transform operation.

Other than that, every one was pretty much coding the way they liked. Bean mapping code wasn't homogeneous but it was not a problem as anyone could dive into the other's code easily. (of course! it was plain Java code).

## but...

Still, there was room for improvement...

### often tedious and time consuming

Hand written bean mapping could be tedious and time consuming to write.

Sometimes it couldn't be helped. There was some non trivial conversions to do, properties which were not named the same or business specific default values, etc.

But other times, it was just plain and "obvious" and it was frustrating to have to type it all by hand (powerful such as IntelliJ IDEA's were here to lighten the burden). Also we had to rewrite the same technical pieces of code again and again. We did create utility classes and methods but they were hard to share across the whole codebase.

### not always a piece of art

Freedom in code writing is appreciated by the developer but some ways of coding are known to be better than others, at least as far as providing good testability and respect to [SOC](http://en.wikipedia.org/wiki/Separation_of_concerns) and [KISS](http://en.wikipedia.org/wiki/KISS_principle) principles are concerned.

The use of Guava's Function and the legitimate search for the least difficult (and time consuming) way of writing code had driven developers to mostly use [enums singletons](http://en.wikipedia.org/wiki/Singleton_pattern#The_enum_way) as mapper classes and use static references between mappers (ie. `MapperA` calls `MapperB.INSTANCE`). SOC was there (most of the time) but testability was bad.

It could have been improved if each mapper class had been a class implementing a specific interface and the singleton aspect just being the scope of the bean in the Dependency Injection framework.

Unfortunately, it requires some verbose code ceremony and, as coding took quite some time already, it was pretty hard to enforce it.

# Improving hand written bean mapping code

## let's list what the developer needs

Lets sum up what should be done to improve hand written bean mapping code:

1. writing obvious mapping should be automated
2. recurrent technical code should be factorized
3. code ceremony to write better bean mapping code should be removed

>Writing non obvious mapping could have been some point 4. The reason is that hand written bean mapping code can not be beaten for such mappings. We are here talking specifically about improving hand written code, so there is no point 4. It is left in the developer's hand.

Existing bean mapping tools deal with the first element in the list very well. 

On the other hand, they usually solve the other two by just removing hand written bean mapping code all together (except for the extreme corner cases or when providing extensibility) and deal with them internally.

## a single library is not enough

Through out the history of Java bean mapping tools, it is pretty clear that they all took on the target of removing the need for the developer to write bean mapping code.

Some tool aim at taking on the challenge of doing it all, others have a limited scope from the start. The later are actually more lucid, in my opinion. Bean mapping is such a complex and ever evolving matter. The developers needs (or their customers) in this area can never be met.

>As a matter of proof, look at the existing tools issue managers, mailing lists, newsgroups. What you will see is a never ending list of feature requests to support this or that case, to support this new library/framework/tool, etc.

They are all designed as libraries. It's clear enough to me that creating another library will fail all the same. We need to do it differently.

## divide and organize complexity

Acknowledging the complexity of the problem, DAMapping is designed accordingly.

The strategy is to split complexity into smaller problems. Its easier to provide easy to understand solutions when scope is limited.

### sketching the right toolS for the job

We listed earlier [3 axes of improvements](#let's-list-what-the-developer-needs) to make hand written bean mapping code better.

Lets see for each axis what kind of tool would do best:

1. writing "obvious" mapping: this is a job for a code generator
2. recurrent technical code: this is a job for a library of utility classes and methods
3. removing code ceremony: this is a job for a framework

>quick note on the difference between a framework and a library: check out Martin Fowler's widely shared [definition of libraries and frameworks](http://martinfowler.com/bliki/InversionOfControl.html) enlightened me on the matter.

It is quite visible that these tools we identified will work together, making  DAMapping a [stack](http://en.wikipedia.org/wiki/Solution_stack).

# A code generator

## "obvious" mappings, they aren't many

The first tool in the list of a code generator. Its scope of application is defined as generating "obvious" mapping.

Lets try to define "obvious" here.

Something like mapping "properties with the same name and the same type" is what comes to mind first. 

OK, but this definition is quite restrictive so let's try and loosen the "same" parts in it.

For property names, extending the definition is really a matter of "guessing" and implementing some "smart" correlation algorithms but at the end of the day, only the developer knows if the guess is right.

>Example of "smart" correlation: property called `firstname` on source bean is mapped to property `prenom` ("firstname" in French); property `customerList` (camelCase) is mapped to property `customer_list`.

For property types, beside exact match, we could also support mapping from primitive types to boxed types and the other way around, enum to `String` and `String` to enum, `Collection` to `Array`, ...

hey! wait!

What about `null` values? What about `String` value not being a value of the target `enum`? What about precision-loss when mapping number types or primitive number types? What about the choice of implementation when type is an interface (e.g. target property has type `List`, shall we create a `ArrayList`? a Guava's `ImmutableList`?)? What about... what about...

## lets rather go for "guessable" mappings

Well, it seems that for the type as well as for the name, the best we can do is guess. Guess which property should be be mapped to which, guess how this mapping should be done.

So, lets use a new definition of the scope of the code generator: *generating guessable mappings*.

Luckily enough, this definition is very much compatible with generating code as part of the application, since code instantly becomes the developer's property and can be fixed as regular plain Java code.

## and be open to preferences

But guessing is not enough.

Quite often, you just can not guess. Well, yes you can (quote?) but you'll get it wrong anyway. You can know the developer's tastes, you can't know the application's constraints. e.g. when instantiating lists, one can prefer using Guava's `ImmutableList`, Java's `ArrayList` or some other implementation.

To fix that, it's quite simple, we just need a way to let the code generator know about those developer preferences, those application constraints.

## pertinent defaults

Of course, specifying preferences should be completely optional.

Some mapping implementations can be non intrusive (e.g. only require the Java API) and work for the very large majority of people. They are the implementations existing mapping tool usually go for.

So, our code generator should be using these as default mappings and as such being usable without any initial configuration.

Defaults mapping implementations should also be chosen according to safest practices (e.g. null safe). 

>Regarding null-safety, code generator could be smart enough to figure from annotations, such as JSR-305's annotations `@Nonnull` and `@Nullable`, when null-safety is actually required.

## two levels of code generation

The code generator has two levels of code generation:

1. method level: generates the mapping from one type to another directly in code (ie. inside a specific method)
2. class level: generates the class and the code to map a type to another, supporting bean trees (ie. generating multiple classes)

# A bean mapping library

The bean mapping (utility) library is about providing classes and methods to code bean mapping efficiently and in a readable manner.

The library exposes meaningfully named classes and methods, most likely leveraging the readability of [method chaining](http://en.wikipedia.org/wiki/Method_chaining) and [fluent interface](http://en.wikipedia.org/wiki/Fluent_interface) coding styles.

## anybody can use it, anywhere

The library is obviously used by the code generator. But this implies that the developer will use it too, since the code is generated in the application's source code.

Apart for putting additional pressure on the quality of the documentation, this is good. This is where DAMapping really hands over the reins to the developer and give her all the power to write bean mapping code the way she likes.

A barely hidden wish is that the library will provide powerful enough classes and methods that they will be used by developer in pieces of code far from being bean mapping code.

## modular design

The library should be split in several modules.

The core module will have no dependencies and will be coded exclusively against the Java API.

Other modules will be provided which will provide implementations of the classes in the core module and extend them with specific methods, e.g. a Guava module.

# A bean mapping framework

Last but far from least is the bean mapping framework.

This framework provides a solution to organize bean mapping code in the application, respecting best practices such as KISS and SOC, with the least possible overhead, so that the developer can focus on writing bean mapping code and only that.

## as light as possible

In practice, the framework is based on a purposely limited set of annotations (we want to keep it simple) and an annotation processor.

The annotation processor generates classes and interfaces for each class holding bean mapping code (so called "dedicated classes"). The generated classes implement the generated interface and delegate their implementation to the dedicated class.

The generated interface allows to loosely couple dedicated classes with each other and with the application.

## but extensible

Regarding the integration with the application, the framework also supports integration with the Dependency Injection / Inversion of Dependency as most application uses them.

This part of the framework will be developed as separate modules which will be detected by the annotation processor and will extend it.

# the extra tool: IDE plugin



IDE plugins are here both to provide convenience integration of the  the various components with 

IDEA and to improve the developer's experience using them

## mapping framework integration



## code generator integration

### method level generation

### class level generation

### preferences

## generated code support

IDEA does not see generated class or interface until project is built, which can make coding much less fluent

## developer support

early framework error report, missing property mapping, Dependency Integration framework integration


Presented that way, it appears that a User Interface is required. The obvious solution here is to integrate with the User Interface the developer is already using: the IDE.

But we need to acknowledge from the start that there is many IDEs. IDE plugins and the code generator should be separated components, the former leveraging the power of the later though its API.








