---
layout: post
title: "How to write a Annotation Processor in Java"
tags:
 - Annotation Processor
 - Javac
 - Java
categories:
 - articles
image:
 feature: feature_image_green.png
---



### the ```AbstractProcessor``` abstract class

The [AbstractProcessor](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/AbstractProcessor.html) class is meant to be the super class of most ```Processor``` implementations.

#### annotation based descriptions

The ```AbstractProcessor``` conveniently provides a way to specify the returned values of the [descriptives methods](TODO link to previous article) of the ```Processor``` interface using annotations on the Annotation Processor class:

* ```@SupportedAnnotationTypes``` for method [getSupportedAnnotationTypes](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedAnnotationTypes())
    - this annotation can be omited, in which case a warning will be displayed in the compiler logs and an empty ```Set``` is returned
    - note that doing so implies that the Annotation Processor will never be invoked as it does not register to any annotation
* ```@SupportedSourceVersion``` for method [getSupportedSourceVersion](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedSourceVersion())
    - this annotation is optional, in which case a warning will be displayed in the compiler logs and ```SourceVersion.RELEASE_6``` returned
    - note that using this annotation, you can not use the convenient ```SourceVersion#latestSupported()``` method. The workaround is to not use the annotation and override the ```getSupportedSourceVersion``` method from ```AbstractProcessor```
* ```@SupportedOptions``` for method [getSupportedOptions](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedOptions())
    - this annotation is optional and not warning will be issued if it is missing
    - Note that the value returned by [the method ```getSupportedOptions``` is ignored by ```Javac```](TODO link to other article)

#### init method implementation

The [init](TODO link to previous article) method implementation stores the [ProcessingEnvironment](TODO link to previous article) in a property called ```processingEnv``` and performs sanity and contracts checks:

* raise a IllegalStateException if the method is called more than once for a specific instance
* raise a NullPointerException if the ```ProcessingEnvironment``` argument is ```null```

#### almost an ```Adapter``` for the ```Processor``` interface

Since it provides non final implementations for all methods of ```Processor``` but ```init```, which is ```abstract```, it works as an [Adapter](http://en.wikipedia.org/wiki/Adapter_pattern). As such, any of these methods can be override to extends or modify the default implementation.


TODO: give an example, a 

### compiling the Annotation Processor

TODO: Javac Annotation Processing must be explicitly disabled

### setting up for discovery

TODO : give an example of a Maven project

#### life-cycle of a ```Processor``` instance


## Good practices

### guidelines to write a robust Annotation Processor

TODO add this is a quote from Processor Javadoc

To be robust when running in different tool implementations, an annotation processor should have the following properties:

* The result of processing a given input is not a function of the presence or absence of other inputs (orthogonality).
* Processing the same input produces the same output (consistency).
* Processing input A followed by processing input B is equivalent to processing B then A (commutativity)
* Processing an input does not rely on the presence of the output of other annotation processors (independence) 

### Annotation Processors work in a collaborative environement

#### exceptions and errors
Do not throw exceptions

#### claiming annotations

Do not claim annotations (by having the ```init``` method returning ```true``` ) unless they really are your own.

And even if they are your own, think about extensibility. 

For example, one could write an Annotation Processor based on your annotation to complete your Annotation Processor's behavior.
But if any of the two Annotation Processors claims the annotation and if they don't declare any other annotation, only the first Annotation Processor will have its ```init``` method called and there is no guarantee which one it will be.

### logging

use [ProcessingEnvironment#getMessager](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/ProcessingEnvironment.html#getMessager())

expliquer que les logs ERROR arrète (ou pas) la compilation mais/et passe (ou pas) le flag RoundEnvironement#errorRaised() à true

expliquer les niveau de logs, leur visibilité via Javac en ligne de commande et via Maven

expliquer les arguments, où trouver les valeurs à passer pour indiquer la bonne ligne et le bon fichier


## how to generate source code

## how to 

