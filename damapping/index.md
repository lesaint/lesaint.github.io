---
layout: damapping
title: The object mapping stack for Java
excerpt: DAMapping is the Object Mapping Stack for Java. It is a new approach to object mapping, by design and principles. Ground rule, object mapping must be pure Java code and this code belongs to the developer. DAMapping is fully statically typed, make debug and refactoring prime citizens, is little intrusive and highly customizable. It can be used as a whole to fully automate object mapping code writing or components can be used individually.
css: damapping
categories:
 - damapping
comments: true
---

DAMapping is structured as **stack of components**, complementary and yet individually usable, designed to **power the developer** who writes or maintain object mapping code in Java.

![DAMapping stack schema]({{ site.url }}/images/damapping/damapping-stack-schema.png)
{: .center}

Based on [the principles]({{ site.url }}/damapping/principles.html) that **object mapping should be code** and that the **developer should own** it, DAMapping provides a way of doing object mapping in **pure Java** inside your own code.

>more details on the principles on DAMapping [here]({{ site.url }}/damapping/principles.html)

# With DAMapping

![use damapping and map it your way]({{ site.url }}/images/damapping/use-damapping-and-map-it-your-way.png){: .pull-right}

* structure your object mapping code with the ultra light and flexible **DAMapping framework**
* write efficient, readable and good-looking object mapping code with the **DAMapping library**
* generate type-to-type and object-tree to object-tree mappings with the **DAMapping code generator**
* use all these components in a few clicks directly in your IDE with the **DAMapping IDE plugins**

# Short-term benefits of DAMapping

* DAMapping can do it all for you but then hand it over to you: **you own the code**
* **DAMapping is fully statically typed**: it's pure Java code everywhere (no property names as String!), if it compiles, you know it runs
* **DAMapping does not limit** how object mapping is done: it creates object mapping code or gives you utilities to write it, in both cases the code is yours, you can handle any case, just write it
* **DAMapping is open**: it does not enforce any vision of how object mapping should be done, even the DAMapping generator can be configured, but it does provide good defaults
* **DAMapping is flexible**: you can use the whole stack (much like any other object mapping tool) or you can use any combination of its components

# Long-term benefits of DAMapping

Where DAMapping definitely stands out is on the long term.

Doing pure Java object mapping code and as part of the developer's code has many benefits.

* **it's stable**: it's in your VCS, it won't change (even if you update DAMapping) unless you say it should and anyway will know when and (hopefully) why
* **it's safe** because it is really fully statically typed
* there is **no need to know DAMapping** to understand and maintain your object mappings, it's plain Java code!
* **you can refactor** your classes (rename properties, methods, types, ...), your object mapping code will stay up-to-date (depending on your IDE -- use IntelliJ IDEA -- free ad) and if there is something wrong, the compiler will tell you
* **you can inspect** the code, you know when and how things are mapped, there is no magic
* you get comprehensive stack traces and **you can debug** it all

# Documentation

Check out the documentation to get a better understanding of DAMapping, how it works and how to use it:

* DAMapping
    - [principles of DAMapping]({{ site.url }}/damapping/principles.html)
* DAMapping framework
    - [the DAMapping framework home page]({{ site.url }}/damapping/framework/)
    - [getting started with the DAMapping framework]({{ site.url }}/damapping/framework/)
    - [documentation of the DAMapping framework]({{ site.url }}/damapping/framework/documentation/)

<!--
* DAMapping library
    - [presentation of the DAMapping library]({{ site.url }}/damapping/library/presentation.html)
* [principles of a new code generator]({{ site.url }}/damapping/generator/principles.html)
* [presentation of the IntelliJ IDEA plugin]({{ site.url }}/damapping/ide-plugin/for-intellij-idea.html)
-->

# License

DAMapping is open source, licensed under Apache Licence 2.0, and all sources are available on GitHub.

Contributors are welcome, any feedback as well

# Development status

| Component | Status | Source |
|:--------|:-------:|--------:|
| *framework*   | beta release is almost there: object tree mapping support, CDI integration | [[Github](https://github.com/lesaint/damapping)] [![Build Status](https://travis-ci.org/lesaint/damapping.svg?branch=master)](https://travis-ci.org/lesaint/damapping) |
| *library*   | dev will start soon, working on the road map for now | [[Github](https://github.com/lesaint/damapping-library)] [![Build Status](https://travis-ci.org/lesaint/damapping-library.svg?branch=master)](https://travis-ci.org/lesaint/damapping-library) |
| *code generator*   | dev has not started yet, working on high level specifications | |
| *IntelliJ IDEA plugin*   |  plugin is in alpha stage (not released yet), it supports generated class integration | [[Github](https://github.com/lesaint/damapping-idea)] |
| other *plugins* | dev not started | |
{: rules="groups"}


<!--
# DAMapping foundation articles

<ul class="post-list">
    <li><article><a href="{% post_url articles/2014-05-21-java_bean_mapping_is_wrong_lets_fix_it %}">Java Object Mapping is wrong, let's fix it! <span class="entry-date"><time datetime="2014-05-21T00:00:00+02:00">May 21, 2014</time></span></a></article></li>
    <li><article><a href="http://localhost:4000/articles/2014/11/04/damapping-is-a-bean-mapping-stack-not-another-library.html">DAMapping is a object mapping stack, not another library</a></article></li>
    <li><article><a href="http://localhost:4000/articles/2014/11/04/genesis-of-the-damapping-project.html">Genesis of the DAMapping project</a> <span class="entry-date"><time datetime="2014-05-21T00:00:00+02:00">May 21, 2014</time></span></article></li>
</ul>

-->
