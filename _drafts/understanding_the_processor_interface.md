---
layout: post
title: "Understanding the Processor interface"
tags:
 - Annotation Processor 
 - Javac
 - Java
categories:
 - articles
image:
 feature: feature_image_green.png
---

This article describes the ```Processor``` interface that must be implemented to do Annotation Processing in ```Java``` and as such covers almost all the ```Java``` Annotation Processing API. Also, it specifically discusses how ```Javac``` implements the Annotation Processing API with some surprising behaviors.


This articles assumes that the reader is familliar with the general Annotation Processing mechanics in ```Java```. If not, please read [How does annotation processing work in Java]({% post_url articles/2014-10-08-how_does_annotation_processing_work_in_java %}).

The ```Processor``` interface is the interface an Annotation Processor class must implement. It defines 7 methods.

## descriptive methods

Using the 3 following methods, an Annotation Processor describes what annotations it supports, what ```Java``` source code it supports and what options passed to the compiler itself it supports.

### getSupportedAnnotationTypes

```java
Set<String> getSupportedAnnotationTypes()
```

The [getSupportedAnnotationTypes](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedAnnotationTypes()) method returns a ```Set``` of ```String``` which can be:

* the full qualified name of an annotation type
* a String in the form ```name.*``` which represents all annotation types which qualified name starts with ```name.```
* ```*``` which represents all annotation types

#### an empty ```Set``` is the same as ```*```

When experimenting with Annotation Processor implementations, I noticed that, if I implement a ```getSupportedAnnotationTypes``` method that returns an empty ```Set```, the way ```Javac``` treats the Annotation Processor is exactly the same as when I return ```*```: the Annotation Processor is feed all the annotations found in source and generated files.

Initially I though it was a specific behavior of ```Javac``` but the following quote from the [getSupportedAnnotationTypes](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedAnnotationTypes()) method javadoc may say that it is the expected behavior:

>Finally, "*" by itself represents the set of all annotation types, including the empty set. 

Personnaly, I would have expected an Annotation Processor with an empty ```Set``` of supported annotation types to be ignored. But, this approach kind of makes sens too, you just need to be aware of it.

### getSupportedSourceVersion

```java
SourceVersion getSupportedSourceVersion()
```

The [getSupportedSourceVersion](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedSourceVersion()) method returns the latest version of ```Java``` supported by the compiler represented by a value of the enum ```SourceVersion```.

This method is used to avoid calling an Annotation Processor when compiling with a source code version later that the one it was written for.

Note that it implicitly means that Annotation Processors are supposed to support one version of ```Java``` and all the previous ones. This is usually not a problem.

#### ```getSupportedVersion()``` is useless with ```Javac```

As far as I could experiment, the value returned by ```getSupportedVersion()``` is ignored by ```Javac```.

##### version older than the current one

If one specifies a version (lets say ```SourceVersion.RELEASE_6```) older than the version of ```Java``` used to compile (lets say ```JDK``` 1.8), the Annotation Processor is called anyway.

The value seems to be purely ignored but what may be going here is that ```Java``` source code is fully backward compatible so supporting any lower version means supported any upper one.

##### version more recent than the current one

If one specifies a version (lets say ```SourceVersion.RELEASE_8```) more recent than the latest source version supported by the compiler (lets say we use ```JDK``` 1.7), then the compilation will fail with an exception such as the following because the enum value ```RELEASE_8``` does not exist in ```Java``` 1.7.

```java
java.lang.EnumConstantNotPresentException: javax.lang.model.SourceVersion.RELEASE_8
```

##### best strategy when targeting ```Javac```

As we discussed above, specifying a recent version may limit the use of your Annotation Processor and specifying a older version is practically useless.

So, if your Annotation Processor does not have any java-version-specific code, the best strategy in my opinion is to implement ```getSupportedSourceVersion``` and return [SourceVersion.latestSupported()](http://docs.oracle.com/javase/7/docs/api/javax/lang/model/SourceVersion.html#latestSupported()) as it guarantess compatibility with any version of Java.

### getSupportedOptions

```java
Set<String> getSupportedOptions()
```

The [getSupportedOptions](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getSupportedOptions()) method declares the options that could be passed to the compiler and that the compiler should forward to the Annotation Processor.

Each string returned in the set must be a period separated sequence of identifiers as defined by the [SourceVersion#isIdentifier](http://docs.oracle.com/javase/7/docs/api/javax/lang/model/SourceVersion.html#isIdentifier(java.lang.CharSequence)) method.

Options can be used to alter the Annotation Processor's behavior from the compilation command line. For example, the Annotation Processor could be told to disable itself (a convenient practice), to enable/disable one functionnality or another, etc.

#### how to pass Annotation Processor options with ```Javac```

With the ```Javac``` compiler, command lines arguments starting with ```-A``` must be used to pass options to an Annotation Processor.

* ```-Acom.acme.Processor.enable``` to pass an option without a value
* ```-A``` is an invalid argument, ```Javac``` will fail and show an error
* ```-Acom.acme.Processor.logLevel=2``` to pass an option with a value
* ```-Afoo=``` is valid and treated the same as ```-Afoo``` (ie. an option without a value)

#### ```Javac``` ignores ```getSupportedOptions```

As I investigated use of Annotation Processor options with ```Javac```, I found out that the compiler exposes the same ```Map``` of options to all the Annotation Processor: the complete ```Map``` of options it received to pass to the Annotation Processors.

The returned value of getSupportedOptions is just ignored and even if it returns an empty ```Set```, an Annotation Processor will have access to all the options passed to the compiler in ```ProcessingEnvironment#getOptions()```.

>The project used to identify this behavior is available on GitHub, check out the [README](https://github.com/lesaint/annotation-processing-explained#experimentations-on-annotation-processor-options)

## annotation completion

### getCompletions

```java
Iterable<? extends Completion> getCompletions(Element element, AnnotationMirror annotation, ExecutableElement member, String userText)
```

My understanding it that the [getCompletions](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#getCompletions(javax.lang.model.element.Element,%20javax.lang.model.element.AnnotationMirror,%20javax.lang.model.element.ExecutableElement,%20java.lang.String)) method is used to provide completion when writing Annotations in source code. But I haven't used it yet so I can not provide experimental details about it.

## lifecycle methods

2 methods, beside the default constructor of the class, are involved in the lifecycle of the Annotation Processor.

### init

```java
void init(ProcessingEnvironment processingEnv)
```

The [init](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#init(javax.annotation.processing.ProcessingEnvironment)) method is used to initialize a Annotation Processor instance after the compiler has created it with the default constructor of the class.

This method is guaranteed to be called once and only once and before any call to the [process](#process) method.

#### first argument

The ```ProcessingEnvironment``` argument is never ```null```. It is described in details [below](#the-processingenvironment-object).

### process

```java
boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv)
```

The [process](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html#process(java.util.Set,%20javax.annotation.processing.RoundEnvironment)) method is called once for every annotation processing round the Annotation Processor is part of.

#### first argument

The first argument is a ```Set``` of the TypeElement representing the Annotations the Annotation Processor registered to process via the [getSupportedAnnotationTypes](#getsupportedannotationtypes) method which are effectively available in the current round.

In other words:

* this ```Set``` may be empty
    - it is always empty during the last round (because there is no input file during the last round, more details [here]({% post_url articles/2014-10-08-how_does_annotation_processing_work_in_java %}#the-last-round))
    - it may be empty during a round but non empty during the next. This means some file with Annotation(s) supported by the current Annotation Processor were generated during the previous round
    - it is always empty if the wildcard ```*``` was used as a return value of [getSupportedAnnotationTypes](#getsupportedannotationtypes)
* when partial wildcard were specified (such as ```com.acme.*```) in the return value of [getSupportedAnnotationTypes](#getsupportedannotationtypes), this ```Set``` lets the Annotation Processor know which concrete annotations were matched for the current round

The ```Set``` is never ```null```.

#### second argument

The second argument is a ```RoundEnvironment``` and is never ```null```. It is detailed [below](#the-roundenvironment-object).

#### returned value

The ```process``` method returns a ```boolean``` which indicates to the compiler whether the Annotation Processor "claims" the Annotations passed in as the first argument.

Quoting the Javadoc:

> If ```true``` is returned, the annotations are claimed and subsequent processors will not be asked to process them; if ```false``` is returned, the annotations are unclaimed and subsequent processors may be asked to process them. A processor may always return the same ```boolean``` value or may vary the result based on chosen criteria.

Returning ```true``` must be used carefully, as it will prevent other Annotation Processor to process these annotations during the current round.
More specifically, when using the ```*``` wildcard, it means that no other Annotation Processor will be able to process any Annotation during the current round.

## the ```ProcessingEnvironment``` object

The roles of the [ProcessingEnvironment](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/ProcessingEnvironment.html) object passed to the Annotation Processor as an argument of the ```init``` method is to give access to (quoting from the Javadoc):

>facilities provided by the framework to write new files, report error messages, and find other utilities

### environnement methods

#### getSourceVersion

This value identifies the version of the source code, which can be specified to ```Javac``` using the ```-source``` argument. It does not identify the Java version the code is beeing compiled to (which is specified by the ```-target``` argument).

#### getOptions

#### getLocale

### utilities methods

#### getElementUtils

#### getTypeUtils

### facilities methods

#### getFilter

#### getMessager

```java
  private void investigatingLogging(Set<? extends TypeElement> typeElements, RoundEnvironment roundEnv) {
    // Diagnostic.Kind.WARNING and NOTE ne sont pas affichés dans la console maven, il faut utiliser
    // Diagnostic.Kind.MADATORY_WARNING pour être sûr d'afficher un message visible lorsque le compilateur
    // est lancé avec ses options par défaut. Le message est prefixé d'un "[WARNING] "
    // D'autre part, System.out.println fonctionne sous maven (et forcément System.err aussi) et affiche un message
    // lors du lancement du compilateur sans option particulière. Le message n'a pas de prefix.
    // passer le javac en debug ou verbose ne semble pas permettre l'affichage des Kind.NOTE ou WARNING

    System.out.println("System.out.println message");
    System.err.println("System.err.println message");
    Messager messager = processingEnv.getMessager();

    messager.printMessage(Diagnostic.Kind.NOTE, "Note level message");
    for (TypeElement te : typeElements) {
//            messager.printMessage(Diagnostic.Kind.MANDATORY_WARNING, "Traitement annotation " + te.getQualifiedName
// ());
      System.err.println("Traitement annotation " + te.getQualifiedName());

      for (Element element : roundEnv.getElementsAnnotatedWith(te)) {
//                messager.printMessage(Diagnostic.Kind.MANDATORY_WARNING, "  Traitement element " + element
// .getSimpleName());
        System.err.println("  Traitement element " + element.getSimpleName());
      }
    }
  }
```


## the ```RoundEnvironment``` object

### status methods

#### processingOver

#### errorRaised

### methods to access round Element objects

#### getRootElements

The [getRootElements](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/RoundEnvironment.html#getRootElements()) method basically returns the Element for each file in the round. It could be a Package Element or a Class/Interface/Enum Element.

Note that root Element are not necessarily annotated themself dfmkjhfmjdshfmdfh sdqjmfh mqdkjfh mkjdqf hmkjds m 

#### getElementsAnnotatedWith

Two versions of the ```getElementsAnnotatedWith``` method are provided. The first one allow to retrieve elements annotated with a specific annotation [using its class](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/RoundEnvironment.html#getElementsAnnotatedWith(java.lang.Class)), the seond one, using [a TypeElement representing the annotation](http://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/RoundEnvironment.html#getElementsAnnotatedWith(javax.lang.model.element.TypeElement)).
