---
layout: damapping
title: DAMapping framework
excerpt: Home page of the DAMapping framework, getting started and documentation.
css: damapping
categories:
 - damapping
comments: false
---

The DAMapping framework is a component of the [DAMapping object mapping stack for Java](http://damapping.javatronic.fr).

The DAMapping framework provides a way to structure object mapping code as fragments isolated in *dedicated classes*.

The framework frees the developer from the interface + class code ceremony required to glue the fragments together and/or with the rest of the application while respecting loose coupling and good testability.

The framework integrates nicely with [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection) frameworks in order to reduce the overhead of writing of object mapping even less.

Installation
============

To use the *DAMapping framework* you only need to add its jar file to your classpath.

For Maven users, you can do so by adding the following dependency:

{% highlight xml %}
<dependency>
    <groupId>fr.phan.damapping</groupId>
    <artifactId>damapping-annotation-processor</artifactId>
    <version>0.5.0</version>
    <!-- scope does not need to be explicitly specified, default scope works just fine -->
    <scope>compile</scope>
</dependency>
{% endhighlight %}

That's it!

Getting started
===============

Checkout the [getting started with DAMapping framework]({{ site.url }}/damapping/framework/getting-started.html) page.

Framework Documentation
=======================

To get extending understanding of how to use the framework, checkout the [documentation of the DAMapping framework]({{ site.url }}/damapping/framework/documentation).

<!--
Annotation processing
=====================

## Java Annotation processing explained

<ul class="post-list">
    <li><article><a href="{% post_url articles/2014-10-08-how_does_annotation_processing_work_in_java %}">How does annotation processing work in Java</a></article></li>
    <li><article><a href="http://localhost:4000/articles/2014/11/05/understanding_the_processor_interface.html">Understanding the Processor interface</a></article></li>
    <li><article><a href="http://localhost:4000/articles/2014/11/05/understanding_the_processingenvironment_and_roundenvironment_interfaces.html">Understanding the ProcessingEnvironment and RoundEnvironment interfaces</a></article></li>
</ul>

## Annotation Processor coding tips

<ul class="post-list">
    <li><article><a href="articles/2014/11/05/how_to_write_a_annotation_processor_in_java.html">How to write a Annotation Processor in Java</a></article></li>
    <li><article><a href="{% post_url articles/2014-09-22-how_to_debug_an_annotation_processor %}">How to debug an Annotation Processor</a></article></li>
    <li><article><a href="{% post_url articles/2014-08-31-how_to_make_sure_javac_is_using_a_specific_annotation_processor %}">How to make sure javac is using an Annotation Processor and troubleshoot when it is not</a></article></li>
</ul>
-->
