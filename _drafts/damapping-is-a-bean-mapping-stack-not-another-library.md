---
layout: post
title: "DAMapping is a bean mapping stack, not another library"
tags:
 - DAMapping
 - Annotation Processing
 - Java
categories:
 - articles
image:
 feature: feature_image_green.png
---

Recently, Gunnar Morling commented on my article [Java bean mapping is wrong, lets fix it](http://www.javatronic.fr/articles/2014/05/21/java_bean_mapping_is_wrong_lets_fix_it.html) and asked for my opinion on [MapStruct](http://mapstruct.org/). MapStruct is a bean mapping library from RedHat that generates bean mapping code using an Annotation Processor and Gunner is working on it.

I wrote a [response](http://www.javatronic.fr/articles/2014/05/21/java_bean_mapping_is_wrong_lets_fix_it.html#comment-1663100604) to his comment which turned out to be mostly a comparison between MapStruct and DAMapping. They have a troubling lot of things in common.

That's when I realized what makes DAMapping so peculiar: it's a new approach to bean mapping by design and principles.

DAMapping is a bean mapping *lightweight coding paradigm* and a *stack of components* to power the developer who writes bean mapping code. It is not another technical implementation of a bean mapping library as all bean mapping tools have been until now.


# What is DAMapping

DAMapping is a set of complementary elements, hence it should rather be considered as a stack or a project:

* a set of annotations and an Annotation Processor to help wire bean mapping code together and with the rest of the application: the `DAMapping framework`
* a bean mapping code generator: the `DAMapping code generator`
* IDE plugin(s), to invoke the later and integrate the former with the IDE
* bean mapping utilities used by the code generator but which can also be used directly: the `DAMapping toolkit`

<pre class="center">
---------------------------------
|          IDE plugins          |
---------------------------------
|         code generator        |
---------------------------------
|   framework    |    toolkit   |
---------------------------------
</pre>

Technical architecture and design principles of DAMapping come from the study of the existing bean mapping tools and from a high level analysis of their common points and weaknesses. They also come from the experience of professionally doing bean mapping on large projects and over a respectably long period of time.

>related articles on the origin of DAMapping: [genesis of the DAMapping project](TODO link genesis) and [Java Bean Mapping is wrong, let's fix it!]({% post_url articles/2014-05-21-java_bean_mapping_is_wrong_lets_fix_it %})

# Principles of DAMapping

DAMapping has a more humble goal than other tools: *help the developer write* bean mapping code, instead of doing bean mapping in his or her place. 

In other words, DAMapping _does not do_ bean mapping (yes, that may come as a surprise), it _provides ways to write_ bean mapping code better, faster and stronger (some may see a quote here ;-) ).

## pure Java bean mapping code

One thing bean mapping tools have in common is that bean mapping logic quickly ends up being spread across over various places in the application: configuration files, annotations elements, specific classes and methods to extend/customize the tool, etc.

DAMapping avoid this pitfall by taking as a principle that *all* bean mapping logic must be plain Java code.

## the developer owns it

Second principle which is direct consequence of DAMapping being a little invasive tool, is that all bean mapping code will be the property of the developer and as such must be in the source code of the application as any other piece of business code.

## no limitations

A direct consequence of the first two principles is that DAMapping does not force any limitation upon the developer with it comes to coding bean mapping logic.

Worst case scenario, DAMapping won't provide the developer with the utility method/class to save her from writing that technical code again and again but that's only until it is implemented.

In any case, never will the developer be limited in how bean mapping logic is implemented. This is a design decision.

## use it all... or not

Much like the Spring framework, DAMapping provides complementary components which form a global solution to do bean mapping in Java but the developer is not constrained to use the whole stack.

If the developer thinks using all of them is the perfect solution for her, then let her do so.

Otherwise, the developer can use only some of the components:

* using only the framework and write all code by hand
* using only the toolkit and neither the framework nor the code generator
* using the IDE plugin without the framework
* etc.

# Foundation component: the bean mapping framework

Freedom in code writing is good but some ways of coding are known to be better than others, at least as far as providing good testability and respect to [SOC](http://en.wikipedia.org/wiki/Separation_of_concerns) and [KISS](http://en.wikipedia.org/wiki/KISS_principle) principles are concerned.

## introduction to the DAMapping framework

The following practices can easily be considered as good practices when it comes to writing bean mapping code (I am open to challenge on this subject).

* use one class for each mapping from one type to another and compose these classes (SOC, KISS, re-usability)
* use an interface and an implementing class for each mapping and do not use static code (better testability)
* leverage the Inversion-of-control and dependency injection framework in place within the application if there is any (optional but obviously a good practice)

To help the developer implements them as easily as possible, DAMapping provides a set of [annotations](https://github.com/lesaint/damapping/tree/master/core-parent/annotations/src/main/java/fr/javatronic/damapping/annotation) and an Annotation Processor. They compose the foundation element of the DAMapping stack. It is called the `DAMapping framework`.

>the term "framework" is fundamental here as a difference between DAMapping and existing tools. Look at Martin Fowler's widely shared [definition of libraries and frameworks](http://martinfowler.com/bliki/InversionOfControl.html).

## basic usage of the framework

The class below is a `Mapper` as per DAMapping framework's definition: it is a class with a method doing bean mapping (talk about KISS).

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

Please note that this is a class, not an interface. We are not configuring a tool to do bean mapping, we are providing bean mapping code to the framework.

A class annotated with `@Mapper` is the atomic component of bean mapping code according to DAMapping's bean mapping code paradigm. It is also referred to as the "dedicated class".

Although the example above is a dedicated class mapping a single type to another, the DAMapping framework does not enforce such a rule (though it is best to follow it), nor does it enforce any naming convention.

This is done on purpose as the goal of DAMapping is to support the developer, not to constrain her into a single way of coding.

## 1 class = 1 interface + 1 class

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

## mapping bean trees

The next added value of the DAMapping coding paradigm is to remove all the coding ceremony when mapping a bean tree to another thanks to the DAMapping framework.

To map bean trees, the developer composes generated Mapper interfaces into dedicated classes.

In the following example, the dedicated class `AcmeToViten` maps the type `Acme` to the type `Viten`. These types are the root of two (very simple) bean trees: `Acme` has a property of type `Foo` which must be mapped to the `Viten`'s property of type `Bar`.

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

## integrating with the application

When using the DAMapping framework, the developer is supposed to use the MapperImpl class in her application code, not the dedicated class directly. 

See below an example of using bean mapping code with DAMapping framework manually.

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

>Note that the entry point to the bean mapping code is not some generic class that usually acts as the single point of entry for all code managed by other tools. Here, it is a fully typed and specific interface, meaningfully named and exposing a method named as the developer feels suits best.

## integrating with dependency injection frameworks

Obviously, few applications will instance concrete class directly. They will rather use a dependency-injection framework (Spring, Guice, Dagger, ...) that will manage object instantiation and injection.

The DAMapping framework supports integrating with those frameworks, but as it is not a core functionality to writing bean mapping code, we won't go into too much details here.

The planned idea is to initially provide minimal support through the support of the JSR-330 specification (work in progress).

Next, extensive support for specific dependency-injection frameworks will be provided as plugins of DAMapping annotation processor.

Extensive support for Spring, for example, could be generating Configuration classes or XML configuration files or supporting Spring specific annotations.

## unit testing bean mapping code

I said earlier that the developer is not supposed to use the dedicated class directly.

It is exactly the opposite when it comes to unit testing. The developer must write unit tests againt the dedicated class directly. There is no point in testing DAMapping framework itself.

Note that thanks to DAMapping, the developer can write real unitary tests of the mapping from one type to another. Mapping of properties with complex types can be isolated in other dedicated classes and imported into the current one as Mapper interfaces, which can be easily mocked.

# Second component: the bean mapping code generator

Writing the obvious bean mapping code is the cause of lots of frustration and time waste for the developer.

This is where DAMapping bean mapping code generator comes in.

The code generator will be invoked by the IDE plugin but it is designed as a library so that it may be integrated in other tool than DAMapping.

## principles of DAMapping code generator

The DAMapping code generator works at two levels:

1. at the "method level": it generates code to map one type to another
    * leverages the power of DAMapping's bean mapping toolkit
2. at the "class level": it generates dedicated classes to map one bean tree to another and their code content
    * leverages the power of the DAMapping's bean mapping framework
    * using this level, the developer will be able to save herself from writing any line of bean mapping code (at least when the generator is advanced enough)

## the common point with other tools

Generating bean mapping code is what every other bean mapping tools based on source code generation is doing already.

This is good for DAMapping. It means that, with collaboration, the development of this component can benefit from the experience of other tools.

# Third component: the IDE plugins

The IDE plugins are the frontend of the DAMapping stack. They have two roles:

## integrate with the DAMapping framework

The DAMapping framework has a very simple and open definition of what a dedicated class is. Yet, an IDE plugin could provide early feedback on errors which would otherwise end up as compiling errors (such as defining two public methods in a dedicated class).

In addition, the plugin could provide helpful shortcuts such as a convenient way of creating a dedicated class with a generated name and implementing Guava's [Function](http://docs.guava-libraries.googlecode.com/git/javadoc/com/google/common/base/Function.html) interface, adding a dependency to an existing Mapper interface, ...

Finally, IDEs such as IntelliJ IDEA require a little help to flawlessly (ie. without building the project) being aware of content generated by an Annotation Processor.

## integrate with the DAMapping code generator

Since DAMapping's code generator has two levels of functionality, both would be integrated within the IDE thanks to the plugin. Integration would obviously take the form of GUI actions or menus.

### method level code generation

For the first level of code generation, think about inline actions inside the code editor.

For example: "right click on instance variable" > choose "populate from..." > "select other variable" in scope > done

### class level code generation

For the second level of code generation, a wizard would be more appropriate. 

For example: select "generate bean mapping" in menu > select "source and target types" > select "target package" > "validate per class operations" > done

# Fourth component: the bean mapping toolkit

The DAMapping's bean mapping toolkit provides utility methods, class and patterns to help write bean mapping code.

The DAMapping code generator will leverage the power of this toolkit to factorize code and most effectively handle the recurrent technical challenges of bean mapping in Java: null value handling, common mapping, enum mapping, collection mapping, etc...

The point of making all this code a separate component is to allow the developer to use it independently from DAMapping code generator and framework if she wants.

MapStruct and other already have such a toolkit but it is hidden. DAMapping could very well use what's already been done.

# Status of the project

DAMapping is an ambitious project.

Currently, the DAMapping framework gets most of the development power (me, on my private time). The foundations are almost there. Checkout the [issues](https://github.com/lesaint/damapping/issues) and look at the planned [milestones](https://github.com/lesaint/damapping/milestones) to get an idea.

The [DAMapping IDE plugin for IntelliJ IDEA](https://github.com/lesaint/damapping-idea) has also been started but is at alpha stage and not yet released. It currently offers integration of the generated classes and interfaces without building the project.

Development of the other two components, the code generator and the toolkit, has not yet started.

Help in the form of feedback or contributions is welcome :)
