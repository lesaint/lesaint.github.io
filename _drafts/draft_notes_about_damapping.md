---
layout: post
title: "draft notes about DAMapping"
tags:
 - 
categories:
 - articles
image:
 feature: feature_image_green.png
---


# draft text, code generator

## identifying properties

When the developer writes bean mapping code by hand, she can only used code to read and set state of the source and target beans which are accessible to the method where she writes that bean mapping code.

The same restrictions apply to a bean mapping source code generator.

>the developer could consider using reflection, byte-code manipulation to read or modify the state of beans (e.g. when dealing with legacy/incorrectly designed beans). A code generator could also do that. Let's consider this as not being in the scope of DAMapping's code generator. It could be developed as a future extension of he code generator though.

#### on the target bean

For the target bean, identifying properties is a matter of which ways are available to define the state of the target bean and their accessibility.

Defining state can be done through:

1. static factory methods
2. constructors
3. properties
4. "setters" as per the JavaBean definition at least
5. other methods

#### on the source bean

As a property is barely defined by more than its name and type, these are the criteria on which we will math one property from source bean to a property of target bean. 

The third criteria could be identified: the property accessibility, ie. the exposed methods.


work around the problem. Let's say that we do not define the scope of the code generator at all.

Let's isn't defined in term of code difficulty. mapping alone but as how easy it is to code that mapping.

For example, let's take the example of the mapping of property `Foo.prop` of type `String` to property `Bar.prop` of some `enum` type.

This mapping can not be defined as "obvious". The input String could be `null`, its value non existent in the target `enum` type or use a different case, etc.

Unless the developer just ignores these questions, how to map those properties from one to the other isn't trivial until... 

...until we can write it with a one-liner with good semantics. In the `String` to `enum` case described above, we could write:

{% highlight java %}
bar.setProp(EnumMapper.from(foo.getProp()).ignoreCase().orElse(SomeEnum.SOME_VALUE));
{% endhighlight %}

It seals it is only a matter of having the right utility methods/classes/API to write that one-liner.

When we listed the [right tools for the job](#sketching-the-right-tools-for-the-job) earlier we said that we needed a library to provide utility code (the second point in the list). The first point relied in the definition of "obvious" mapping which we just said was really just a matter of tooling.

Excellent! It means that the code generator will improve as the bean mapping library improves! And in the meantime, the library can be used independently since we separated it.

## notion de "mapping implementation"

So, the best path here, is just to let the developer choose between implementations suggested by the code generator or, even better, specify her own.

If we consider the tool and the developer implementations to be just implementations coming from a different source, then a design is sketching before our eyes.

## the design

1. identify properties on source bean (name and type)
2. identify properties on target bean (name and type)
3. match source properties with target properties according to available or selected matching algorithms
4. for each mapping
    1. list applicable mapping implementations
    2. preselect mapping by default or according to user preferences

The keys here, to make an efficient tool, will be to be "smart" at the first 3 levels. At the 4th level, it will be a matter of providing a relevant and extensible set of mapping implementations and also implement smart algorithms to select them.

# Benefits of plain Java code

## logic is all the same

Elements in the above list are in the order we experience need for them when writing bean mapping code by hand.

The most important point is the third one, as the other two should be built on top of it: a way of writing bean mapping code respecting the best practices.

## bean mapping tools are all the same: libraries

Until I realized it, I was myself calling all bean mapping solutions I've tested or looked at bean mapping "frameworks".

But, actually, none is a "framework".

They are just tools, invoked and configured from the application's code.

And  make those tools be a perfect fit to be called "libraries".




What I see when looking at bean mapping tools one after the other, is new technical implementations and/or new priority decisions in the bean mapping cases supported and/or new feature unrelated to bean mapping as such.

What I also see is that underneath a promise of simplicity for the developer lie very complex pieces of software, solving complex technical problems.

It is too bad though, that this complexity more often than not shows up at the surface as a large, ever extending set of parametrization options resulting into a large (if not also complex) API.


it has the most benefits in the long run (see list of [defects of existing bean mapping solutions in Java](www.javatronic.fr/articles/2014/05/21/java_bean_mapping_is_wrong_lets_fix_it.html#the-practical-problems-of-hidden-mapping-code) in a previous article).

Obviously, a tool is needed to fix these imperfections. But there is none out there which is designed to 

What we need is a tool to **help** the developer write:

1. what is boring/tedious
2. what is too much ceremony but the best practice

Here is the catch: that is **not** what bean mapping frameworks offer today.

What they offer is to do the bean mapping **for** the developer, not to help her do it.

And they all do that...

# Bean mapping frameworks are all the same



# DAMapping is different

[TODO reformuler]As I try to point in my response to your comment, there is deep difference in philosophy between the two frameworks, not necessarily that much of a difference on the technical level.


## links to several Java bean mapping frameworks




But they miss a point: bean mapping code _is_ business code, it _is not_ technical code.

Yes, there is some extreme cases where it is hard to see the business value, such as pure software layering with strictly identical bean trees which must be mapped from one to the other.

But that's not what the developer needs, she needs help to write it. She need to remove the "tedious and time consuming" from writing the bean mapping code.

## unstable across versions



# opinion of bean mapping forged by experience

Depending on your experience, it is there, right there where your opinion on bean mapping is born: when you had bean mapping to do.

Did you encounter bean mappings which for the very most part where plain and obvious ?
Then, you believe that bean mapping code is low value and can be automated and you just need an mechanism to deal with exceptions.

Did you encounter bean mappings which were made of a significant share of non trivial mappings ?
Then, you are not satisfied with bean mapping tools out there because they all take bean mapping as being dumb.

>note: I am aware these are bold generic statements



# No good tool on the market

Yes, I am saying that bean mapping tools out there are all the same.

## magic + optional customization

They may provide various technical implementations but they all get on the bean mapping issue the same way: "I do magic, you can optionally customize me".

Take a look at their documentation, you can easily spot a pattern there:
1. "Hey, just do this and it works !"
2. "Here is how to customize"

## they arent' frameworks but libraries



### limited by design

Look at the frameworks forum, news groups or issue lists. What you will see most are posts about "bean mapping" cases not supported by the code generator (or runtime mapper). 

Look at their new "features" at each release:
* support for XXX (put any framework or new version here) !
* new corner case customization !

How do you think the developer can use the framework until these new "features" are out ?

She can't.

By design, she cannot do any mapping that is not already implemented by the framework.

We are far from the hand written code here, very far, isn't?






## a single library is not enough

Through out the history of Java bean mapping tools, it is pretty clear that they all took on the target of removing the need for the developer to write bean mapping code.

Some tool aim at taking on the challenge of doing it all, others have a limited scope from the start. The later are actually more lucid, in my opinion. Bean mapping is such a complex and ever evolving matter. The developers needs (or their customers) in this area can never be met.

>As a matter of proof, look at the existing tools issue managers, mailing lists, newsgroups. What you will see is a never ending list of feature requests to support this or that case, to support this new library/framework/tool, etc.

They are all designed as libraries. It's clear enough to me that creating another library will fail all the same. We need to do it differently.
