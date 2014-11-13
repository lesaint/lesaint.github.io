---
layout: post
title: "Understanding the ProcessingEnvironment and RoundEnvironment interfaces"
tags:
 - Annotation Processing
 - Javac
 - Java
categories:
 - articles
image:
 feature: feature_image_green.png
---

This article follows the [Understanding the Processor interface]() article and details the `ProcessingEnvironment` and `RoundEnvironment` interfaces. This interfaces are essential when processing annotation in `Java` as they provide tools to process the source code model of the compiler (represented by the `java.lang.model.element` and `java.lang.model.type` APIs), produce source/class files, log messages, etc.



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

{% highlight java %}
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
{% endhighlight %}


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
